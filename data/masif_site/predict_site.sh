#!/bin/bash
python -W ignore -m masif.masif_site.masif_site_predict nn_models.all_feat_3l.custom_params $1 $2
