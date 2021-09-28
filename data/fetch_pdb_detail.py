#!/usr/bin/env python
import sys,os
import json
from urllib import request
import ssl

context = ssl._create_unverified_context()

def tree_print(a,indent="\t"):
    if type(a) == dict:
        for key in a :
            print(indent+key)
            tree_print(a[key],indent+"\t")
    elif type(a) == list:
        for b in a :
            print(indent+"> ",end="")
            tree_print(b,indent+"\t")
    else:
        print(indent,a)

        

if True:
    pdbid = "6WJN"
    url = f"https://data.rcsb.org/rest/v1/core/entry/{pdbid}"

    pdb_data = json.loads( request.urlopen(url, context = context).read() )
    #tree_print(pdb_data)

    entity_ids = pdb_data["rcsb_entry_container_identifiers"]["polymer_entity_ids"]
    #chains = pdb_data["rcsb_polymer_entity_container_identifiers"]["_ids"]
    #print(chains)
    #sys.exit()
    #tree_print(pdb_data)


    for entity_id in entity_ids:
        print(entity_id)
        url = f"https://data.rcsb.org/rest/v1/core/polymer_entity/{pdbid}/{entity_id}"
        entity_data = json.loads( request.urlopen(url, context = context).read() )
        chains = entity_data["rcsb_polymer_entity_container_identifiers"]["asym_ids"]
        print(chains)
        if chains == ["32"]:
            tree_print(entity_data)
        #chain_id = chains[int(entity_id)-1]
        #print(chain_id)
        

