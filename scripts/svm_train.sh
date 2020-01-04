#!/bin/bash

svm-train -g 2 -c 2 training_no_0.txt model_no_0_2_2.txt && /
svm-train -g 2 -c 4 training_no_0.txt model_no_0_2_4.txt && /
svm-train -g 0.5 -c 2 training_no_0.txt model_no_0_0_2.txt && /
svm-train -g 0.5 -c 4 training_no_0.txt model_no_0_0_4.txt
