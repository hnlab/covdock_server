#!/usr/bin/env python
import sys,os
import pandas as pd
import json
from urllib import request

infile  = 'all.xlsx'
mapfile = 'uniprot_2_pdb.list'

df = pd.read_excel( infile ) 


# def mapping function
u2p = dict()
for line in open(mapfile):
    if line.split()[0]!="From":
        key = line.split()[0]
        value = line.strip().split()[1]
        u2p[key] = value

def uniprot_2_pdb(a):
    try:
        return u2p[a]
    except:
        return None

df["PDB"] = df['uniprot'].map( uniprot_2_pdb,na_action=None )

df.to_excel("output.xlsx")




