PDB_ID=$(echo $1| cut -d"_" -f1)
CHAIN1=$(echo $1| cut -d"_" -f2)
CHAIN2=$(echo $1| cut -d"_" -f3)
# Invoke your environment here.
python -W ignore -m masif.data_preparation.01-pdb_extract_and_triangulate $PDB_ID\_$CHAIN1
python -W ignore -m masif.data_preparation.01-pdb_extract_and_triangulate $PDB_ID\_$CHAIN2
python -W ignore -m masif.data_preparation.04-masif_precompute masif_site $1
python -W ignore -m masif.data_preparation.04-masif_precompute masif_ppi_search $1
