#!/bin/bash -l
#SBATCH --nodes=1
#SBATCH --time=48:0:0
#SBATCH --qos=gpu
#SBATCH --gres=gpu:1
#SBATCH --ntasks-per-node=1
#SBATCH --cpus-per-task=1
#SBATCH --partition=gpu
#SBATCH --mem 16384

module purge

srun python -m masif.masif_ligand.masif_ligand_train
