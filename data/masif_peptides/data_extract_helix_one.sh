PDB_ID=$(echo $1| cut -d"_" -f1)
CHAIN1=$(echo $1| cut -d"_" -f2)
CHAIN2=$(echo $1| cut -d"_" -f3)
python -W ignore -m masif.data_preparation.00-pdb_download $1
python -W ignore -m masif.data_preparation.01b-helix_extract_and_triangulate $1 
