#!/usr/bin/env python
import sys, os
import fpdb
import argparse

pdbid = sys.argv[1]

pdbid = pdbid.lower()
assert len(pdbid) == 4

os.system(f"mkdir {pdbid}")
os.chdir(f"{pdbid}")

mid = pdbid[1:3]
pdbsource = f"/home/pdb/PDB/{mid}/pdb{pdbid}.ent.gz"

os.system(f"cp {pdbsource} ./")
os.system(f"gunzip -qf pdb{pdbid}.ent.gz")
os.system(f"mv pdb{pdbid}.ent {pdbid}.pdb")

filename = f"{pdbid}.pdb"
fixer = PDBFixer(filename=filename)
fixer.findMissingResidues()
fixer.findNonstandardResidues()
fixer.replaceNonstandardResidues()
fixer.removeHeterogens(True)
fixer.findMissingAtoms()
# fixer.addMissingAtoms()
numChains = len(list(fixer.topology.chains()))

del fixer

for i in range(numChains):

    fixer = PDBFixer(filename=filename)
    fixer.findMissingResidues()

    chains = list(fixer.topology.chains())
    keys = fixer.missingResidues.keys()
    from copy import deepcopy

    for key in list(keys)[:]:
        chain = chains[key[0]]
        if key[1] == 0 or key[1] == len(list(chain.residues())):
            print(f">>>>> Debug info: Remove missing residue list: {key}")
            del fixer.missingResidues[key]

    fixer.removeChains(list(range(i + 1, numChains)))
    fixer.removeChains(list(range(0, i)))

    fixer.findNonstandardResidues()
    fixer.replaceNonstandardResidues()
    fixer.removeHeterogens(True)
    fixer.findMissingAtoms()
    fixer.addMissingAtoms()

    chainid = list(fixer.topology.chains())[0].id
    if not chainid:
        chainid = " "

    PDBFile.writeFile(fixer.topology, fixer.positions, open(f"tmp.pdb", "w"))
    with open(f"fixed{i}.pdb", "w") as ofp:
        for line in open("tmp.pdb"):
            if len(line) >= 6 and line[:6] in ("HETATM", "ATOM  "):
                line = line[:21] + chainid + line[22:]
            ofp.write(line)
    os.system("rm tmp.pdb")

    tmp = PDBFixer(filename=f"fixed{i}.pdb")
    residues = tmp.topology.residues()
    count = 0
    for resi in residues:
        if resi.name in [
            "ALA",
            "ASN",
            "CYS",
            "GLU",
            "HIS",
            "LEU",
            "MET",
            "PRO",
            "THR",
            "TYR",
            "ARG",
            "ASP",
            "GLN",
            "GLY",
            "ILE",
            "LYS",
            "PHE",
            "SER",
            "TRP",
            "VAL",
        ]:
            count += 1

    if count <= 50:
        os.system(f"rm fixed{i}.pdb")
        continue

    # make cavity input
    cavity_str = f"""
########################################################################
#   Include section
########################################################################
#-----------------------------------------------------------------------
#   Detect mode
#   -- 0: whole protein mode
#      1: ligand detection mode
#      2: area detection mode
#-----------------------------------------------------------------------
DETECT_MODE         0
#-----------------------------------------------------------------------
#   Input files
#   -- ligand_file should be assigned if detect_mode = 1
#-----------------------------------------------------------------------
RECEPTOR_FILE           fixed{i}.pdb 
PARAMETER_DIRECTORY     /home/qyfu/Cavity/parameter
########################################################################
#   Parameter section
########################################################################
#-----------------------------------------------------------------------
#   Parameter for vacant/vacant-surface method
#   -- Standard :common cavity
#   -- Peptides :shallow cavity, e.g. piptides 
#            binding site, protein-protein interface
#   -- Large    :complex cavity, e.g. multi function
#            cavity, channel, nucleic acid site 
#   -- Super    :sized cavity
#-----------------------------------------------------------------------
SEPARATE_MIN_DEPTH      8
MAX_ABSTRACT_LIMIT_V        1500
SEPARATE_MAX_LIMIT_V        6000
MIN_ABSTRACT_DEPTH      2

#-----------------------------------------------------------------------
#   Input parameters
#   -- boundary: ligand and area mod boundary justify
#   -- single_ligand 1:only process the largest compoents of ligand
#   -- separate polymolecular to monomer
#      -2 = exclude invalid chain (CHAIN_INVALID)
#      -1 = only valid chain (CHAIN_VALID)
#       0 = operating on all parts
#       n = operating on n parts
#   -- use ligand to decide which monomers will be involved
#      this switch will forbiden all hetatom exclude those around ligand
#   -- locate_distance: locate distance of ligand locate
#   -- hetmetal: metal irons /  hetwater: water molecules
#      1 =allow 0 = forbiden
#-----------------------------------------------------------------------
BOUNDARY            0
SINGLE_LIGAND           1
MONOMER             0
LIGAND_LOCATE           0
LOCATE_DISTANCE         5
HETMETAL            1
HETWATER            0
CHAIN_VALID         ABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890
CHAIN_INVALID           ABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890
#   Output section
########################################################################
#-----------------------------------------------------------------------
#   Output mode
#   -- run_info 1:open 0:close
#   -- visual_output  1:output visual results 0:close
#   -- pdb_output 1:output all atoms 2:output cavity atoms
#-----------------------------------------------------------------------
RUN_INFO            0
VISUAL_OUTPUT           1
PDB_OUTPUT          2
#-----------------------------------------------------------------------
#   Output files
#   -- use the basename of receptor file
#-----------------------------------------------------------------------
#V_SURFACE          default_surface.pdb
#V_CAVITY_VACANT        default_vacant.pdb
#V_CAVITY_ATOM          default_cavity.pdb
#POCKET_ATOM_FILE       default_pocket.txt
#POCKET_CAVITY_FILE     default_cavity.txt
#POCKET_GRID_FILE       default_grid.txt
#KEY_SITE_FILE          default_key_site.pdb
#PHARMACOPHORE_TXT_FILE     default_pharmacophore.txt
#PHARMACOPHORE_PDB_FILE     default_pharmacophore.pdb
#-----------------------------------------------------------------------
#   Output parameters
#   -- distance:output protein atom distance
#   -- v_point_num:lager for smaller visual pdb size
#      smaller for better quality(min=1)
#   -- v_output_mod 0:random point 1:chips
#-----------------------------------------------------------------------
MINIMAL_FEATURE_DISTANCE    3.50
MAXIMAL_FEATURE_NUMBER      12
DISTANCE            5
V_POINT_NUM         1
V_OUTPUT_MOD            0
#-----------------------------------------------------------------------
#   Output filter
#-----------------------------------------------------------------------
OUTPUT_RANK         1.5
RULER_1             100
########################################################################
#   Parameter section
########################################################################
#-----------------------------------------------------------------------
#   Detect method
#   -- judge 0=surface 1=vacant 2=vacant-surface
#   -- eraser shap 0=ball 1=cubic 2=global
#   -- radius_lenth : radius or half lenth [step:1A]
#   -- radius mis [step:1A],  bigger to flat and thick and slow,  
#      smaller to opposite. Use bigger value when radius is bigger
#   -- edge adjust  [step:(+/-)0.5A]
#   -- vacant adjust [step:(+/-)0.5A]
#-----------------------------------------------------------------------
JUDGE               2
ERASER              2
RADIUS_LENTH            10.0
RADIUS_MIS          0.5
EDGE_ADJUST             0
VACANT_ADJUST           0
#-----------------------------------------------------------------------
#   Parameter for surface method
#   -- SCL: skip cavity separate step if surface < limit
#   -- SML, MAL: surface auto separate [step:0.5A]
#-----------------------------------------------------------------------
SEPARATE_CHIP_LIMIT     30
SEPARATE_MAX_LIMIT      3000
MAX_ABSTRACT_LIMIT      1200
#-----------------------------------------------------------------------
#   Parameter for vacant/vacant-surface method
#   -- SCLV: skip cavity separate step if vacant < limit
#   -- SCD: skip cavity fill step if depth < limit
#   -- SMD, MAD, MDV: vacant auto separate [step:0.5A]
#   -- MALV, SMLV, MAD, RL: vacant-surface separate  [step:0.5A]
#-----------------------------------------------------------------------
SEPARATE_CHIP_LIMIT_V       300
SEPARATE_CHIP_DEPTH     1
SEPARATE_MIN_DEPTH      8
MAX_ABSTRACT_DEPTH      20
MAX_DEPTH_VACANT        100
MAX_ABSTRACT_LIMIT_V        1500
SEPARATE_MAX_LIMIT_V        6000
MIN_ABSTRACT_DEPTH      2
RIGID_LIMIT         0
#-----------------------------------------------------------------------
#   Solvent accessible radius
#   -- suggest 1.4A~1.6A
#-----------------------------------------------------------------------
ATOM_RADIUS_ADJUST      1.5
        """
    with open(f"cavity.{i}.input", "w") as ofp:
        ofp.write(cavity_str)
    # run cavity
    os.system(f"/home/qyfu/Cavity/cavity64 cavity.{i}.input")

    # process output
    os.system(f"mkdir fixed{i}")
    os.system(f"mv fixed{i}* fixed{i}")
    os.system(f"mv cavity.{i}.input fixed{i}")
    os.system(f"rm fixed{i}/*vacant* fixed{i}/cavity*input fixed{i}/*cavity*")

os.system(f"rm {pdbid}.pdb")
os.chdir("..")
os.system(f"tar --remove-files -acvf {pdbid}.tar.gz {pdbid}")
