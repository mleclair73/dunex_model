#!/bin/bash

# remove PRINT files from workspace (output from SWAN)
mkdir -p run/logs
mv PRINT* run/logs
mv slurm* run/logs
mv swaninit* run/logs
mv Errfile* run/logs

