#!/bin/bash
for i in `cat $1`; do
	wget -P $2 https://files.rcsb.org/view/$i.pdb 
done
