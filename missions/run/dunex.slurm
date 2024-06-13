#!/bin/bash

## Job Name

#SBATCH --job-name=mission

## Allocation Definition

## The account and partition options should be the same except in a few cases (e.g. ckpt queue and genpool queue).

#SBATCH --account=derakhti

#SBATCH --partition=compute-bigmem

## Resources

## Total number of Nodes

#SBATCH --nodes=1

## Number of cores per node

#SBATCH --ntasks-per-node=40

## Walltime (3 hours). Do not specify a walltime substantially more than your job needs.

#SBATCH --time=72:00:00

## Memory per node. It is important to specify the memory since the default memory is very small.

## For mox, --mem may be more than 100G depending on the memory of your nodes.

## For ikt, --mem may be 58G or more depending on the memory of your nodes.

## See above section on "Specifying memory" for choices for --mem.

#SBATCH --mem=100G

## Specify the working directory for this job

#SBATCH --chdir=/gscratch/derakhti/shared/mleclair/dunex_model/missions/

#SBATCH --export=all

module load ompi/4.1.0

module use /gscratch/derakhti/shared/module
module load netcdf_c_gcc9
module load netcdf_fortran_gcc9

mkdir -p /gscratch/derakhti/shared/mleclair/dunex_model/missions/run/logs/mission56
mpirun -np 40 /gscratch/derakhti/shared/mleclair/dunex_model/missions/coawstM \
 /gscratch/derakhti/shared/mleclair/dunex_model/missions/coupling_dunex.in \
  > /gscratch/derakhti/shared/mleclair/dunex_model/missions/run/56/logs/log.out 2>&1
bash /gscratch/derakhti/shared/mleclair/dunex_model/missions/scripts/move_logs.sh