#!/bin/bash
for i in $1*.pdb; do 
	mkdssp -i $i -o ${i%.pdb}.dssp
done



