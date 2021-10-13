source ~/.bashrc
conda activate covdock
export RECEPTOR='fixed'
export CYSSPECIFER='A:CYS273'
export FLEXINDEXFILE='flex.list'
export LIGAND='compound2'
export LIGANDINDICES='29,13'
bash /home/fuqiuyu/Software/miniconda3/envs/covdock/share/covdock/share/scripts/run_covalent_dock.sh 

