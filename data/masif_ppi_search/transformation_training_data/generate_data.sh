python -m masif.masif_ppi_search.transformation_training_data.second_stage_transformation_training  {masif_source}/data/masif_ppi_search/ 1000 2000 9.0 ./transformation_data/ $1
python -m masif.masif_ppi_search.transformation_training_data.precompute_evaluation_features
