#!/bin/bash
for i in $1/*; do
       psiblast -query $i -db $2 -evalue 0.01 -num_iterations 3 -out_ascii_pssm $i.pssm -out $i.alns.blast
done       
