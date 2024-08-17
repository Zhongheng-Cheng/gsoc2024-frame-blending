#!/bin/bash

source config.sh

# rsync -av --progress --exclude='.git' --exclude='venv' $TMP_WORK_DIR/$PROG_DIR $GALLINA_HOME_DIR/

rsync -av --progress $TMP_WORK_DIR/$PROG_DIR/data $GALLINA_HOME_DIR/$PROG_DIR/