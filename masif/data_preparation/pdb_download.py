#!/usr/bin/python
import os
import sys
import shutil
import importlib

import Bio
from Bio.PDB import *

from masif.default_config.masif_opts import masif_opts
# Local includes
from molmimic.parsers.reduce import Reduce

def pdb_download(pdb, protonate=True, bio=None, file=None):
    if not os.path.exists(masif_opts['raw_pdb_dir']):
        os.makedirs(masif_opts['raw_pdb_dir'])

    if not os.path.exists(masif_opts['tmp_dir']):
        os.mkdir(masif_opts['tmp_dir'])

    in_fields = pdb.split('_')
    pdb_id = in_fields[0]

    if "-bio" in pdb_id:
        bio_fields = pdb_id.split("-bio")
        pdb_id = bio_fields[0]
        bio = bio_fields[1]

    if isinstance(bio, bool) and bio:
        bio = 1

    if file is not None and os.path.isfile(file):
        pdb_filename = file
    elif os.path.isfile(pdb):
        #Used path to pdb
        raise RuntimeError("Must use file argument and use the pdb argument for the name to save files")
    elif len(pdb_id) == 4 and bio is None: #) or (len(pdb_id)==7 and pdb_)
        # Download pdb
        pdbl = PDBList()
        pdb_filename = pdbl.retrieve_pdb_file(pdb_id, pdir=masif_opts['tmp_dir'], file_format='pdb')
    elif len(pdb_id) == 4 and bio is not None:
        import urllib.request as urllib
        import zipfile
        url = f"https://files.rcsb.org/download/{pdb_id.upper()}.pdb{bio}.gz"
        zip_path, _ = urllib.request.urlretrieve(url)
        with zipfile.ZipFile(zip_path, "r") as f:
            f.extractall(masif_opts['tmp_dir'])
        pdb_filename = os.path.join(masif_opts['tmp_dir'], f"{pdb_id.lower()}-bio{bio}.pdb")
        shutil.move(os.path.join(masif_opts['tmp_dir'], f"{pdb_id.lower()}.pdb{bio}", pdb_filename)
        pdb_id += f"-bio{bio}"

    assert os.path.isfile(pdb_filename), f"{pdb_filename} not found"

    if bio is None:
        bio = ""

    if protonate:
        ##### Protonate with reduce, if hydrogens included.
        # - Always protonate as this is useful for charges. If necessary ignore hydrogens later.
        print("Protonate")
        protonated_file = masif_opts['raw_pdb_dir']+"/"+pdb_id+".pdb"

        reducer = Reduce(work_dir=masif_opts['tmp_dir'])
        protonated_file = reducer.reprotonate(in_file=pdb_filename, out_file=protonated_file)

        assert os.path.isfile(protonated_file)

        pdb_filename = protonated_file

    return pdb_id, pdb_filename

if __name__ == "__main__":
    if len(sys.argv) <= 1:
        print("Usage: "+sys.argv[0]+" PDBID_A_B")
        print("A or B are the chains to include in this pdb.")
        sys.exit(1)

    pdb_download(sys.argv[1])
