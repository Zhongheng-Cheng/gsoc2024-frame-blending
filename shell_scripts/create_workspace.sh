#!/bin/bash

source config.sh

cd $GALLINA_HOME_DIR/$PROG_DIR
git pull origin main

if [ ! -d $TMP_WORK_DIR ]; then
    mkdir $TMP_WORK_DIR
fi
# rsync -av --progress --exclude='.git' --exclude='venv' $GALLINA_HOME_DIR/$PROG_DIR $TMP_WORK_DIR/

rsync -av --progress $GALLINA_HOME_DIR/$PROG_DIR/data $TMP_WORK_DIR/$PROG_DIR/



