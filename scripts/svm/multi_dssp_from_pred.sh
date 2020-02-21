#!/bin/bash
for i in 0_2 0_4 2_2 2_4; do python3 /home/pelmo/lb2_project/scripts/svm/dssp_from_pred.py pred_no_$1_$i.pred set$1.final.dssp pred_no_$1_$i.ss; done
