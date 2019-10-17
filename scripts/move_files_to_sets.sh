#!/bin/bash

while read filename; do mv $2/${filename} $3/; done < $1
