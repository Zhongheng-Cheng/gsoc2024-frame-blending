#!/bin/bash

# Customize these variables
USERID="zxc808"
NODE="gpu"

GALLINA_HOME_DIR="/mnt/rds/redhen/gallina/home/$USERID"
TMP_WORK_DIR="/scratch/users/$USERID"
PROG_DIR="gsoc2024-frame-blending"
FRAME_DIR="/mnt/rds/redhen/gallina/projects/ChattyAI/FramesConstructions/fndata-1.7/frame"

module load Python/3.11.3
module load PyTorch/2.1.2-foss-2023a-CUDA-12.1.1
module load PyYAML/6.0-GCCcore-12.3.0

