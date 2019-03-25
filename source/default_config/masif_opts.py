masif_opts = {}
# Default directories
masif_opts['raw_pdb_dir'] = 'data_preparation/00-raw_pdbs/'
masif_opts['pdb_chain_dir'] = 'data_preparation/01-benchmark_pdbs/'
masif_opts['ply_chain_dir'] = 'data_preparation/01-benchmark_surfaces/'
masif_opts['mat_dir'] = 'data_preparation/02-matfile/'
masif_opts['coord_dir'] = 'data_preparation/03-coords/'
masif_opts['coord_dir_npy'] = 'data_preparation/03-coords_npy/'
masif_opts['tmp_dir'] = '/tmp/'
masif_opts['ply_file_template'] = masif_opts['ply_chain_dir']+'/{}_{}.ply'
masif_opts['mat_dir_template'] = masif_opts['mat_dir']+'/{}'
masif_opts['coord_dir_template'] = masif_opts['coord_dir']+'/{}'
masif_opts['mat_file_template'] = masif_opts['mat_dir']+'/{}/{}.mat'
masif_opts['coord_file_template'] = masif_opts['coord_dir']+'/{}/{}.mat'

# Surface features
masif_opts['use_hbond'] = True
masif_opts['use_hphob'] = True
masif_opts['use_apbs'] = True
masif_opts['compute_iface'] = True
# Mesh resolution. Everything gets very slow if it is lower than 1.0 
masif_opts['mesh_res'] = 1.0
masif_opts['feature_interpolation'] = True

# Parameters for shape complementarity calculations.
masif_opts['sc_radius'] = 9.0 
masif_opts['sc_interaction_cutoff'] = 1.5
masif_opts['sc_w'] = 0.25

# Coords params
masif_opts['radius'] = 12.0

# Neural network patch application specific parameters. 
masif_opts['ppi_search'] = {}
masif_opts['ppi_search']['training_list'] = 'lists/training.txt'
masif_opts['ppi_search']['testing_list'] = 'lists/testing.txt'
masif_opts['ppi_search']['max_shape_size'] = 200
masif_opts['ppi_search']['max_distance'] = 12.0 # Radius for the neural network.
masif_opts['ppi_search']['masif_precomputation_dir'] = 'data_preparation/04b-precomputation_12A/precomputation/'
masif_opts['ppi_search']['feat_mask'] = [1.0]*5
masif_opts['ppi_search']['max_distance'] = 200
masif_opts['ppi_search']['max_sc_filt'] = 1.0
masif_opts['ppi_search']['min_sc_filt'] = 0.5
masif_opts['ppi_search']['pos_surf_accept_probability'] = 1.0
masif_opts['ppi_search']['pos_interface_cutoff'] = 1.0
masif_opts['ppi_search']['range_val_samples'] = 0.9 # 0.9 to 1.0
masif_opts['ppi_search']['cache_dir'] = 'nn_models/sc05/cache/'
masif_opts['ppi_search']['model_dir'] = 'nn_models/sc05/all_feat/model/'
masif_opts['ppi_search']['desc_dir'] = 'descriptors/sc05/all_feat/'

# Neural network patch application specific parameters. 
masif_opts['site'] = {}
masif_opts['site']['training_list'] = 'lists/training.txt'
masif_opts['site']['testing_list'] = 'lists/testing.txt'
masif_opts['site']['max_shape_size'] = 100
masif_opts['site']['n_conv_layers'] = 3
masif_opts['site']['max_distance'] = 9.0 # Radius for the neural network.
masif_opts['site']['masif_precomputation_dir'] = 'data_preparation/04a-precomputation_9A/precomputation/'
masif_opts['site']['feat_mask'] = [1.0]*5
masif_opts['site']['max_distance'] = 100
masif_opts['site']['range_val_samples'] = 0.9 # 0.9 to 1.0
masif_opts['site']['model_dir'] = 'nn_models/all_feat_3l/'

# Neural network ligand application specific parameters. 
masif_opts['ligand'] = {}
masif_opts['ligand']['assembly_dir'] = 'data_preparation/00b-pdbs_assembly'
masif_opts['ligand']['ligand_coords_dir'] = 'data_preparation/00c-ligand_coords'

