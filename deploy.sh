#!/bin/bash

if [ -z "$1" ] || [ -z "$2" ]; then
  echo "Usage: $0 <model_type> <model_id_or_path>"
  exit 1
fi

MODEL_TYPE=$1
MODEL_ID_OR_PATH=$2

export RAY_memory_monitor_refresh_ms=0
export CUDA_VISIBLE_DEVICES=0,1

swift deploy \
  --model_type $MODEL_TYPE \
  --tensor_parallel_size 1 \
  --model_id_or_path $MODEL_ID_OR_PATH \
  --do_sample True \
  --temperature 0.3
