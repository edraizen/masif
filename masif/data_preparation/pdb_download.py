#!/usr/bin/python
import os
import sys
import importlib

import Bio
from Bio.PDB import *

from masif.default_config.masif_opts import masif_opts
# Local includes
from molmimic.parsers.reduce import Reduce

def download_pdb(pdb, protonate=True):
    if not os.path.exists(masif_opts['raw_pdb_dir']):
        os.makedirs(masif_opts['raw_pdb_dir'])

    if not os.path.exists(masif_opts['tmp_dir']):
        os.mkdir(masif_opts['tmp_dir'])

    in_fields = pdb.split('_')
    pdb_id = in_fields[0]

    print(masif_opts['tmp_dir'])

    # Download pdb
    pdbl = PDBList()
    pdb_filename = pdbl.retrieve_pdb_file(pdb_id, pdir=masif_opts['tmp_dir'], file_format='pdb')

    assert os.path.isfile(pdb_filename), f"{pdb_filename} not found"

    if protonate:
        ##### Protonate with reduce, if hydrogens included.
        # - Always protonate as this is useful for charges. If necessary ignore hydrogens later.
        print("Protonate")
        protonated_file = masif_opts['raw_pdb_dir']+"/"+pdb_id+".pdb"

        reducer = Reduce(work_dir=masif_opts['tmp_dir'])
        protonated_file = reducer.reprotonate(in_file=pdb_filename, out_file=protonated_file)

        assert os.path.isfile(protonated_file)

        pdb_filename = protonated_file

    return pdb_filename

if __name__ == "__main__":
    if len(sys.argv) <= 1:
        print("Usage: "+sys.argv[0]+" PDBID_A_B")
        print("A or B are the chains to include in this pdb.")
        sys.exit(1)

    download_pdb(sys.argv[1])
