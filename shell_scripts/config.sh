#!/bin/bash

USERID=""

# Read in flags
for arg in "$@"
do
    case $arg in
        --user=*)
        USERID="${arg#*=}"
        shift
        ;;
        --node=*)
        NODE="${arg#*=}"
        shift
        ;;
        *)
        echo "Invalid option: $arg" >&2
        exit 1
        ;;
    esac
done

# Check `--user` flag existence
if [ -z "$USERID" ]; then
    echo "Required flag: --user=<user_id> (e.g. abc123)"
    exit 1
fi

# Other settings
GALLINA_HOME_DIR="/mnt/rds/redhen/gallina/home/zxc808"
TMP_WORK_DIR="/scratch/users/$USERID"
PROG_DIR="gsoc2024-frame-blending"
FRAME_DIR="/mnt/rds/redhen/gallina/projects/ChattyAI/FramesConstructions/fndata-1.7/frame"

module load Python/3.11.3
module load PyTorch/2.1.2-foss-2023a-CUDA-12.1.1
module load PyYAML/6.0-GCCcore-12.3.0

