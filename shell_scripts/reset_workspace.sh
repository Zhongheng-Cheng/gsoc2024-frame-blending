#!/bin/bash

source config.sh

# Create temp home in scratch/ folder
if [ ! -d "$TMP_WORK_DIR" ]; then
    mkdir -p "$TMP_WORK_DIR"
fi
cd $TMP_WORK_DIR
echo "Deleting $PROG_DIR..."
rm -rf $PROG_DIR
echo "Cloning $PROG_DIR..."
git clone https://github.com/Zhongheng-Cheng/$PROG_DIR
cd $PROG_DIR
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
rsync -av --progress $GALLINA_HOME_DIR/$PROG_DIR/data $TMP_WORK_DIR/$PROG_DIR/
rsync --progress $GALLINA_HOME_DIR/$PROG_DIR/.env $TMP_WORK_DIR/$PROG_DIR/
rsync -a --progress $FRAME_DIR $TMP_WORK_DIR/$PROG_DIR/
python framenet_xml_parser.py

deactivate

echo "Your workspace is setup in $TMP_WORK_DIR/$PROG_DIR"