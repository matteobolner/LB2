#!/bin/bash
set -m
export OMP_NUM_THREADS=6
svm-predict $1 $2 $3
