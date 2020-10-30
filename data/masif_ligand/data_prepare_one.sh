PDB_ID=$(echo $1| cut -d"_" -f1)
CHAIN1=$(echo $1| cut -d"_" -f2)
CHAIN2=$(echo $1| cut -d"_" -f3)
python -m masif.data_preparation.00-pdb_download $1
python -m masif.data_preparation.00b-generate_assembly $1
python -m masif.data_preparation.00c-save_ligand_coords $1
python -m masif_source.01-pdb_extract_and_triangulate $PDB_ID\_$CHAIN1 masif_ligand
python -m masif_source.data_preparation.04-masif_precompute masif_ligand $1
