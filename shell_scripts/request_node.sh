#!/bin/bash

NODE=""

source ./config.sh

# Check `--node` flag existence
if [ -z "$NODE" ]; then
  echo "Required flag: --node=<node_type> (e.g. cpu)"
  exit 1
fi

cd $TMP_WORK_DIR/$PROG_DIR
source venv/bin/activate

if [ "$NODE" == "gpu" ]; then
    srun -p gpu \
        -C gpu2080 \
        --gres=gpu:2 \
        --time=02:00:00 \
        --mem=64G \
        --mail-user=$USERID@case.edu \
        --mail-type=ALL \
        --pty bash
elif [ "$NODE" == "cpu" ]; then
    srun --time=02:00:00 \
        --mem=64G \
        --mail-user=$USERID@case.edu \
        --mail-type=ALL \
        --pty bash
else
    echo "Unknown NODE type: $NODE. Please specify 'gpu' or 'cpu'."
    exit 1
fi