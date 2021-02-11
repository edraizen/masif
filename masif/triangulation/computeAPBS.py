import os
import numpy
from subprocess import Popen, PIPE

from masif.default_config.global_vars import apbs_bin, pdb2pqr_bin, multivalue_bin
import random

"""
computeAPBS.py: Wrapper function to compute the Poisson Boltzmann electrostatics for a surface using APBS.
Pablo Gainza - LPDI STI EPFL 2019
This file is part of MaSIF.
Released under an Apache License 2.0
"""

def computeAPBS(vertices, pdb_file, tmp_file_base):
    """
        Calls APBS, pdb2pqr, and multivalue and returns the charges per vertex
    """
    fields = tmp_file_base.split("/")[0:-1]
    directory = "/".join(fields) + "/"
    filename_base = tmp_file_base.split("/")[-1]
    pdbname = pdb_file.split("/")[-1]
    args = pdb2pqr_bin+[
        "--ff=parse",
        "--whitespace",
        "--noopt",
        "--apbs-input",
        pdbname,
        filename_base,
    ]
    p2 = Popen(args, stdout=PIPE, stderr=PIPE, cwd=directory)
    stdout, stderr = p2.communicate()

    with open(f"{directory}/{filename_base}.in") as old, open(f"{directory}/{filename_base}.in.real", "w") as new:
        for line in old:
            if "write pot dx pot" in line:
                line = line.replace("write pot dx pot", f"write pot dx {filename_base}")
            print(line.rstrip(), file=new)

    args = apbs_bin+[filename_base + ".in.real"]
    p2 = Popen(args, stdout=PIPE, stderr=PIPE, cwd=directory)
    stdout, stderr = p2.communicate()

    vertfile = open(directory + "/" + filename_base + ".csv", "w")
    for vert in vertices:
        vertfile.write("{},{},{}\n".format(vert[0], vert[1], vert[2]))
    vertfile.close()

    args = multivalue_bin+[
        filename_base + ".csv",
        filename_base + ".dx",
        filename_base + "_out.csv",
    ]
    p2 = Popen(args, stdout=PIPE, stderr=PIPE, cwd=directory)
    stdout, stderr = p2.communicate()

    # Read the charge file
    chargefile = open(tmp_file_base + "_out.csv")
    charges = numpy.array([0.0] * len(vertices))
    for ix, line in enumerate(chargefile.readlines()):
        charges[ix] = float(line.split(",")[3])

    return charges
