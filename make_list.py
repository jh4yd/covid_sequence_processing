from itertools import chain
import pandas as pd
import os
import glob
import re
import shutil
from wget import download
from Bio.PDB import *

#change your paths to the relevant locations!
workspace ='covid_sequence_processing'
human_pdbs_dir = 'human_pdbs'
alphafold_dir = 'alphafold_precomputed'
prep_masif = "prep_masif"

workspace = os.getcwd()

human_pdbs_dir = os.path.join(workspace, human_pdbs_dir)
os.chdir(human_pdbs_dir)

prep_masif = os.path.join(workspace, prep_masif)
if not os.path.exists(os.path.join(workspace, prep_masif)):
    os.mkdir(prep_masif)


#get files names
pdb_list = []
err_list =[]

# Walk through all files in the directory that contains the files to copy
for root, dirs, files in os.walk(human_pdbs_dir):
    for filename in files:
        # I use absolute path, case you want to move several dirs.
        old_name = os.path.join( root, filename )

        # Separate base from extension
        base, extension = os.path.splitext(filename)
        # extract PDB_ID
        if extension == '.pdb':
            pdb_id = base[base.find('-')+1 : base.find('F1')-1].upper()

        elif extension == '.ent':
            pdb_id = base[base.find('pdb')+3 : ].upper()

        else:
            continue

        # extract chain information from files
        f = open(filename, "r")
        Lines = f.readlines()
        try:
            for line in Lines:
                    if line.find("CHAIN:") >= 0 :
                        chaines_info = re.findall("[a-zA-Z]+", line)[2:]
                        chains = [char for char in chaines_info]
                        break
            
            pdb_chain = pdb_id
            for letter in chains:
                pdb_chain = pdb_chain + '_' + letter

            pdb_list.append(pdb_chain)
        except:
            err_list.append(base)
        

        # copy files to new folder, after changing names
        # Initial new name
        new_name = os.path.join(prep_masif, pdb_id+'.pdb')

        # If folder basedir/base does not exist... You don't want to create it?


   
        shutil.copy(old_name, new_name)
                 

with open(os.path.join(prep_masif,"human_list.txt"), "w") as output:
    for row in pdb_list:
        output.write(str(row) + '\n')

with open(os.path.join(prep_masif,"error_list.txt"), "w") as output:
    for row in err_list:
        output.write(str(row) + '\n')