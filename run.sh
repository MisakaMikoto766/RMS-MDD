#!/bin/bash

if [ "$#" -ne 2 ]; then
    echo "Usage: ./run.sh <dataset_file> <output_file>"
    exit 1
fi

DATASET_FILE=$1
OUTPUT_FILE=$2

python ./models/inference.py --dataset_file "$DATASET_FILE" --output_file "$OUTPUT_FILE"
