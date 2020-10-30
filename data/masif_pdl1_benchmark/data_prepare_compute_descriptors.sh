
PDB_ID=$(echo $1| cut -d"_" -f1)
CHAIN1=$(echo $1| cut -d"_" -f2)
CHAIN2=$(echo $1| cut -d"_" -f3)
# Load your environment here.
python -W ignore -m masif.data_preparation.00-pdb_download $1
python -W ignore -m masif.data_preparation.01-pdb_extract_and_triangulate $PDB_ID\_$CHAIN1
python -W ignore -m masif.data_preparation.01-pdb_extract_and_triangulate $PDB_ID\_$CHAIN2
python -W ignore -m masif.data_preparation.04-masif_precompute masif_site $1
python -W ignore -m masif.data_preparation.04-masif_precompute masif_ppi_search $1
python -W ignore -m masif.masif_site.masif_site_predict nn_models.all_feat_3l.custom_params $1 $2
python -W ignore -m masif.masif_site.masif_site_label_surface nn_models.all_feat_3l.custom_params $1 $2
python -W ignore -m masif.masif_ppi_search.masif_ppi_search_comp_desc nn_models.sc05.all_feat.custom_params $1 $2
