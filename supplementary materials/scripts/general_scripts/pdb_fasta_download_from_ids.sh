#!/bin/bash
for line in $(cat $1); do wget https://www.rcsb.org/pdb/download/downloadFile.do?fileFormat=fastachain&compression=NO&structureId=(cut -f 1 -d "_" $line)&chainId=(cut -f 2 -d "_" $line)
done
