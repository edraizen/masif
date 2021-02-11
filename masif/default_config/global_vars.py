# global_vars.py: Global variables used by MaSIF -- mainly pointing to environment variables of programs used by MaSIF.
# Pablo Gainza - LPDI STI EPFL 2018-2019
# Released under an Apache License 2.0

import os, sys
from IPython.core.debugger import set_trace
import subprocess

epsilon = 1.0e-6

use_singularity = os.environ.get("MASIF_SINGULARITY", "f").lower()[0]=="t"
use_docker = os.environ.get("MASIF_DOCKER", "f").lower()[0]=="t"

use_contianer = False
if not use_singularity and not use_docker:
    try:
        o = subprocess.check_output(["which", "singularity"])
        BINARY_START = lambda program: ["singularity", "run", f"docker://edraizen/{program}"]
        use_singularity = True
        use_contianer = True
    except FileNotFoundError:
        try:
            subprocess.check_output(["which", "docker"])
            BINARY_START = lambda program: ["docker", "run", "-v", f"{os.getcwd()}:/home/data", "-w", "/home/data", f"edraizen/{program}"]
            use_docker = True
            use_contianer = True
        except FileNotFoundError:
            pass
            #raise RuntimeError("You must install pymesh to run locally --or-- singularity or docker to run a containrized version")

msms_bin= ""
if 'MSMS_BIN' in os.environ:
    msms_bin = os.environ['MSMS_BIN'].split()
elif use_contianer:
    msms_bin = BINARY_START("msms")
else:
    set_trace()
    print("ERROR: MSMS_BIN not set. Variable should point to MSMS program.")
    sys.exit(1)

pdb2pqr_bin=""
if 'PDB2PQR_BIN' in os.environ:
     pdb2pqr_bin = os.environ['PDB2PQR_BIN'].split()
elif use_contianer:
    pdb2pqr_bin = BINARY_START("pdb2pqr")
else:
    print("ERROR: PDB2PQR_BIN not set. Variable should point to PDB2PQR_BIN program.")
    sys.exit(1)

apbs_bin=""
if 'APBS_BIN' in os.environ:
     apbs_bin = os.environ['APBS_BIN'].split()
elif use_contianer:
     apbs_bin = BINARY_START("apbs")
else:
    print("ERROR: APBS_BIN not set. Variable should point to APBS program.")
    sys.exit(1)

multivalue_bin=""
if 'MULTIVALUE_BIN' in os.environ:
     multivalue_bin = os.environ['MULTIVALUE_BIN'].split()
elif use_contianer:
     multivalue_bin = BINARY_START("multivalue")
else:
    print("ERROR: MULTIVALUE_BIN not set. Variable should point to MULTIVALUE program.")
    sys.exit(1)

reduce_bin=""
if 'REDUCE_BIN' in os.environ:
     reduce_bin = os.environ['REDUCE_BIN'].split()
elif use_contianer:
     reduce_bin = BINARY_START("reduce")
else:
    print("ERROR: REDUCE_BIN not set. Variable should point to REDUCE program.")
    sys.exit(1)

class NoSolutionError(Exception):
    pass
