source ~/.bashrc
conda activate covdock
export RECEPTOR='fixed0'
export CYSSPECIFER='A:CYS150'
export FLEXINDEXFILE='flex.list'
export LIGAND='angl0'
export LIGANDINDICES='24,11'
bash /home/fuqiuyu/Software/miniconda3/envs/covdock/share/covdock/share/scripts/run_covalent_dock.sh 

