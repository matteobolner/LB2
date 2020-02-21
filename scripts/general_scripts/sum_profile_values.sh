#!/bin/bash
for i in $1*.profile; do
	awk '{ sum += $1 } END { printf  sum ; printf " " }' $i
	basename $i
done

