#!/bin/bash
for i in 0_2 0_4 2_2 2_4; do python3 /home/pelmo/lb2_project/scripts/model_performance.py set$1.final.dssp pred_no_$1_$i.ss > perf_no_$1_$i.perf; done
for i in 0_2 0_4 2_2 2_4; do python3 /home/pelmo/lb2_project/scripts/sov.py set$1.final.dssp pred_no_$1_$i.ss > sov_no_$1_$i.perf; done
