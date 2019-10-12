#!/bin/bash
for i in $1*.pssm; do
	less $i | tail -n +4 | sed 's/ \+/ /g' | cut -d " " -f24-43 | head -n -6 > ${i%.fasta.pssm}.profile
done
