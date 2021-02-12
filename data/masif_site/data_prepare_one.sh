#!/bin/bash
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
	echo "Running masif site on $1"
	PPI_PAIR_ID=$1
	PDB_ID=$(echo $PPI_PAIR_ID| cut -d"_" -f1)
	CHAIN1=$(echo $PPI_PAIR_ID| cut -d"_" -f2)
	CHAIN2=$(echo $PPI_PAIR_ID| cut -d"_" -f3)
	python -W ignore -m masif.data_preparation.pdb_download $PPI_PAIR_ID
fi

if [ -z $CHAIN2 ]
then
    echo "Empty"
    python -W ignore -m masif.data_preparation.pdb_extract_and_triangulate $PDB_ID\_$CHAIN1
else
    python -W ignore -m masif.data_preparation/pdb_extract_and_triangulate $PDB_ID\_$CHAIN1
    python -W ignore -m masif.data_preparation/pdb_extract_and_triangulate $PDB_ID\_$CHAIN2
fi
python -m masif.data_preparation.masif_precompute masif_site $PPI_PAIR_ID
