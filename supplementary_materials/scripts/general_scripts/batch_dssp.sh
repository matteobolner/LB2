#!/bin/bash
for i in $1*.pdb; do 
	/home/pelmo/Desktop/programs/dssp/src/dssp-3.0.0/mkdssp	 -i $i -o ${i%.pdb}.dssp
done



