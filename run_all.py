#!/usr/bin/env python
import sys, os

if True:
    for input_str in open("all.list"):
        input_str = input_str.strip()
        index = int( input_str.split('|')[0] )
        cys   = input_str.split('|')[1]
        dirname = f"{index}:{cys}"
        if os.path.isdir(f"data/work/{dirname}"):
            pass
        else:
            print(f"{dirname}")
            os.mkdir(f"data/work/{dirname}")
            import module.covdock as covdock
            os.chdir(f"data/work/{dirname}")
            covdock.runcovdock(dirname)
            if os.path.getsize( "output/my_docking.pdbqt" ) > 32:
                os.chdir("../../..")
            else:
                os.chdir("../..")
                os.system("rm -r {dirname}")
                os.chdir("..")

