#!/bin/bash

#SBATCH --job-name=compile_dunex

#SBATCH --account=derakhti

#SBATCH --partition=compute-bigmem # NOTE(@mleclair): No particular reason to use bigmem

#SBATCH --nodes=1

#SBATCH --ntasks-per-node=8

#SBATCH --time=1:00:00

#SBATCH --mem=100G

#SBATCH --chdir=/gscratch/derakhti/shared/mleclair/dunex_model/missions/compile

#SBATCH -o ./logs/%a.out

#SBATCH --export=all

echo "LOADING ompi/4.1.0"
module load ompi/4.1.0

echo "USING /gscratch/derakhti/shared/module"
module use /gscratch/derakhti/shared/module
echo "LOADING netcdf_fortran_gcc9"
module load netcdf_fortran_gcc9
echo "Loaded"

export MCT_INCDIR=/gscratch/derakhti/shared/COAWST/MCT/include
export MCT_LIBDIR=/gscratch/derakhti/shared/COAWST/MCT/lib

mkdir -p /gscratch/derakhti/shared/mleclair/dunex_model/missions/compile/logs/
echo "Compiling..."
./coawst_dunex.bash -j 8 1>/gscratch/derakhti/shared/mleclair/dunex_model/missions/compile/logs/info.log 2>/gscratch/derakhti/shared/mleclair/dunex_model/missions/compile/logs/warning.log
echo "Done"
# coawst_dunex.bash generates this in the project root /gscratch/derakhti/shared/mleclair/dunex_model/mission
# mv /gscratch/derakhti/shared/mleclair/dunex_model/missions/coawstM /gscratch/derakhti/shared/mleclair/dunex_model/missions/bin