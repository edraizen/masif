import sys
import argparse

def parse_args(args=None):
    main_parser = argparse.ArgumentParser()

    subparsers = main_parser.add_subparsers(title="masif_app", dest="masif_app")

    #parents=[main_parser]
    ligand_parser = subparsers.add_parser("ligand", help="Run masif_ligand",
        description="Run masif_ligand")
    ligand_parser.add_argument("--prep", action="store_true", help="Only preapre files do no training or inference")
    ligand_parser.add_argument('pdb_pair_id', nargs="+", help='PDBID_CHAIN1[CHAIN2]')

    site_parser = subparsers.add_parser("site", help="Run masif_site",
        description="Run masif_site")
    site_parser.add_argument("--prep", action="store_true", help="Only preapre files do no training or inference")
    site_parser.add_argument('pdb_pair_id', nargs="+", help='PDBID_CHAIN1[CHAIN2]')

    ppi_parser = subparsers.add_parser("ppi_search", help="Run masif_ppi_search",
        description="Run masif_ppi_search")
    ppi_parser.add_argument("--prep", action="store_true", help="Only preapre files do no training or inference")
    ppi_parser.add_argument("--nn_model", help="Path to json config files for model or module name",
                            default="masif.nn_models.masif_ppi_search.sc05.all_feat")
    ppi_parser.add_argument('pdb_pair_id', nargs="+", help='PDBID_CHAIN1[CHAIN2]')

    return main_parser.parse_args(args)

def prepare(pdb_chain, masif_app=None, nn_model=None):
    from masif.data_preparation.pdb_download import pdb_download
    from masif.data_preparation.pdb_extract_and_triangulate import pdb_extract_and_triangulate
    from masif.data_preparation.masif_precompute import masif_precompute
    from masif.masif_ppi_search.masif_ppi_search_comp_desc import masif_ppi_search_comp_desc

    pdb_download(pdb_chain)

    pdb_id, chains = pdb_chain.split("_", 1)
    for chain in chains.split("_"):
        pdb_extract_and_triangulate(f"{pdb_id}_{chain}")

    if masif_app == "masif_ligand":
        masif_precompute("masif_ligand", [pdb_chain])
    else:
        masif_precompute("masif_site", [pdb_chain])
        if masif_app=="masif_ppi_search":
            if nn_model is None:
                nn_model = "masif.nn_models.masif_ppi_search.sc05.all_feat"
            masif_precompute("masif_ppi_search", pdb_chain)
            masif_ppi_search_comp_desc(pdb_chain, nn_model=nn_model)

def main(args=None):
    args = parse_args(args=args)

    if args.masif_app == "ligand":
        for pdb_chain in args.pdb_pair_id:
            prepare(pdb_chain, masif_app="ligand")
    elif args.masif_app == "site":
        for pdb_chain in args.pdb_pair_id:
            prepare(pdb_chain, masif_app="site")
    elif args.masif_app == "ppi_search":
        for pdb_chain in args.pdb_pair_id:
            prepare(pdb_chain, masif_app="ligand", nn_model=args.nn_model)

    if args.prep:
        return

if __name__ == "__main__":
    main()
