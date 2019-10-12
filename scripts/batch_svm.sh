#!/bin/bash

for i in $1*.profile; do
       python3 /home/pelmo/lb2_project/scripts/svm_input_from_profile.py $i $2/${i%.profile}.dssp
done       
