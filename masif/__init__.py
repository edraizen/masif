import sys
import argparse

def create_parser():
    main_parser = argparse.ArgumentParser()

    ligand_subparsers = main_parser.add_subparsers(title="ligand",
                        dest="ligand_command")
    ligand_parser = service_subparsers.add_parser("first", help="first",
                        parents=[parent_parser])

    site_subparser = service_parser.add_subparsers(title="site",
                        dest="site_command")
    site_parser = action_subparser.add_parser("second", help="second",
                        parents=[parent_parser])
    site_parser.add_argument('--file', default=False, required=False,
                             action='store_true', help='Use PDB file instead of downloaifn from pdb')
    site_parser.add_argument('pdb_pair_id', help='PDBID_CHAIN1[CHAIN2]')
    args = main_parser.parse_args()

if __name__ == "__main__":
    create_parser()
