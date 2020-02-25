#!/bin/bash
for i in $1*.dssp; do
	grep -A 500000 "#" $i  | cut -b 12,14,17 | tail -n +2| sed 's/./&:/1'| sed 's/./&:/3' | sed 's/$/:/'> ${i%.dssp}
done
