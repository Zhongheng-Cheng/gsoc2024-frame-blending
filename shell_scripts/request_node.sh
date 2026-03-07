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
    # 1. Removed hardcoded 'gpu2080' to allow access to A100/H100 nodes
    # 2. Optimized --gres for CLIP-based multimodal inference
    srun -p gpu \
        --gres=gpu:1 \
        --time=04:00:00 \
        --mem=80G \
        --mail-user=$USERID@case.edu \
        --mail-type=ALL \
        --pty apptainer exec --nv $CONTAINER_PATH bash
        
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
