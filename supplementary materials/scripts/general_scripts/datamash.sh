#!/bin/bash
cat $1 | sed 's/$//' |sed 's/\./,/g' | datamash -W transpose --no-strict --filler 0,0 | datamash -W transpose | datamash -W --group 1 --no-strict --filler XYZ mean 2 pstdev 2 mean 3 pstdev 3 mean 4 pstdev 4  #| datamash -W transpose # | # sed '$!N;s/\n/ /'
