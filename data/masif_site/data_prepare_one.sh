#!/bin/bash
masif_root=$(git rev-parse --show-toplevel)
masif_source=$masif_root/source/
masif_matlab=$masif_root/source/matlab_libs/
export PYTHONPATH=$PYTHONPATH:$masif_source
export masif_matlab
if [ "$1" == "--file" ]
then
	echo "Running masif site on $2"
	PPI_PAIR_ID=$3
	PDB_ID=$(echo $PPI_PAIR_ID| cut -d"_" -f1)
	CHAIN1=$(echo $PPI_PAIR_ID| cut -d"_" -f2)
	CHAIN2=$(echo $PPI_PAIR_ID| cut -d"_" -f3)
	FILENAME=$2
	mkdir -p data_preparation/00-raw_pdbs/
	cp $FILENAME data_preparation/00-raw_pdbs/$PDB_ID\.pdb
else
	PPI_PAIR_ID=$1
	PDB_ID=$(echo $PPI_PAIR_ID| cut -d"_" -f1)
	CHAIN1=$(echo $PPI_PAIR_ID| cut -d"_" -f2)
	CHAIN2=$(echo $PPI_PAIR_ID| cut -d"_" -f3)
	python -W ignore -m masif.data_preparation.00-pdb_download $PPI_PAIR_ID
fi

if [ -z $CHAIN2 ]
then
    echo "Empty"
    python -W ignore -m masif.data_preparation.01-pdb_extract_and_triangulate $PDB_ID\_$CHAIN1
else
    python -W ignore -m masif.data_preparation/01-pdb_extract_and_triangulate $PDB_ID\_$CHAIN1
    python -W ignore -m masif.data_preparation/01-pdb_extract_and_triangulate $PDB_ID\_$CHAIN2
fi
python -m masif.data_preparation.04-masif_precompute masif_site $PPI_PAIR_ID
