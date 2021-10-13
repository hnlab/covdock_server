#!/usr/bin/env python
import sys, os
import pandas as pd
import urllib.request as request
import ssl

ssl._create_default_https_context = ssl._create_unverified_context
from pdbfixer import PDBFixer
from simtk.openmm.app import PDBFile
import fpdb

lig_input = f"{os.environ['HOME']}/work/covdock_server/data/compound2.mol2"
inputfile = f"{os.environ['HOME']}/work/covdock_server/data/output.xlsx"

df = pd.read_excel(inputfile)

af_base = '/home/fuqiuyu/Database/Alpha_Fold_Human_Proteomic'

def runcovdock(dirname):
    index = int(dirname.split(":")[0])
    cys = dirname.split(":")[1]
    cys_index = int( cys.replace("C",'') )
    row = df.iloc[index, :]
    pdbid = row["PDB"].upper()
    uniprot = row["uniprot"]
    print(uniprot)


    if False: #PDB
        # Download pdb
        if True:
            
            with open(f"{pdbid}.pdb.gz", "wb") as ofp:
                ofp.write(
                    request.urlopen(f"https://files.rcsb.org/download/{pdbid}.pdb.gz").read()
                )
            os.system(f"gunzip -f {pdbid}.pdb.gz")

        # Specify chain Identifer
        chain_specifer = "A"

        # Make receptor
        if True:
            filename = f"{pdbid}.pdb"
            fixer = PDBFixer(filename=filename)
            numChains = len(list(fixer.topology.chains()))
            del fixer

            for i in range(numChains):

                fixer = PDBFixer(filename=filename)
                fixer.findMissingResidues()

                chains = list(fixer.topology.chains())

                chainid = list(fixer.topology.chains())[0].id
                if not chainid:
                    chainid = " "
                if chainid != chain_specifer:
                    continue
                else:
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

                    residues = fixer.topology.residues()
                    count = 0
                    for resi in residues:
                        if resi.name in [
                            "ALA", "ASN", "CYS", "GLU", "HIS",
                            "LEU", "MET", "PRO", "THR", "TYR",
                            "ARG", "ASP", "GLN", "GLY", "ILE",
                            "LYS", "PHE", "SER", "TRP", "VAL",
                        ]:
                            count += 1

                    if count <= 50:
                        continue

                    PDBFile.writeFile(fixer.topology, fixer.positions, open(f"tmp.pdb", "w"),keepIds=True)
                    with open(f"fixed.pdb", "w") as ofp:
                        for line in open("tmp.pdb"):
                            if len(line) >= 6 and line[:6] in ("HETATM", "ATOM  "):
                                line = line[:21] + chainid + line[22:]
                            ofp.write(line)
                    os.system("rm tmp.pdb")

    elif True: # Alpha Fold 
        # source = f"{af_base}/AF-{uniprot}-F3-model_v1.pdb.gz"
        # os.system(f"cp {source} ./")
        # os.system(f"gunzip -f -q AF-{uniprot}-F3-model-v1.pdb.gz") 
        # os.system(f"mv AF-{uniprot}-F3-model-v1.pdb fixed.pdb")
        with open("fixed.pdb",'w') as ofp:
            for line in request.urlopen(f"https://alphafold.ebi.ac.uk/files/AF-{uniprot.upper()}-F1-model_v1.pdb"):
                line = line.decode("utf-8")
                if "MODEL" not in line and "ENDMDL" not in line:
                    ofp.write(line)
        
        chain_specifer = "A"

    # Cov dock
    if True:
        with open("flex.list",'w') as ofp:
            ofp.write(f"{chain_specifer}:{cys_index}")
        with open("tmp.sh",'w') as ofp:
            ofp.write("source ~/.bashrc\n")
            ofp.write("conda activate covdock\n")
            ofp.write(f"cov_dock_mol2 -i {lig_input} -r fixed -s {chain_specifer}:CYS{cys_index} -l flex.list -w output \n")
        os.system("bash tmp.sh")
        # os.system("rm tmp.sh")


if __name__ == "__main__":
    runcovdock("48:C891")


