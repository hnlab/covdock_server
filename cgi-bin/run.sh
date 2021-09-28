#$ -S /bin/bash
#$ -cwd
#$ -q cuda 
#$ -pe cuda 4


export CUDA_VISIBLE_DEVICES=0,1
source ~/.bashrc

grep -v CRYST1 shift_in_box.pdb > no_cryst1.pdb
../py/addter.py no_cryst1.pdb addter.pdb

echo 1

mkdir em_rec
cp addter.pdb em_rec/init.pdb
cd em_rec
../../py/openmm_minim.py init.pdb
cd ..

echo 2
 
mkdir add_solvent
cp em_rec/minimize.pdb add_solvent/init.pdb
cd add_solvent
../../py/openmm_addsolvent.py init.pdb
cd ..

echo 3 

mkdir em
cp add_solvent/minimize_addsolvent.pdb em/init.pdb
cd em
../../py/em.py init.pdb
cd ..

mkdir heat
cp em/minimize.pdb heat
cd heat
../../py/heat.py minimize.pdb
cd ..

mkdir eq
cp heat/finished.pdb eq/init.pdb
cd eq
../../py/eq.py init.pdb
cd ..

mkdir prod
cp eq/finished.pdb prod/init.pdb
cd prod
../../py/prod.py init.pdb
cd ..

echo 'Done'


