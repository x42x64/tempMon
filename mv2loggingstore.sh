#!/bin/bash
shopt -s extglob
LOGGER_DIR=/mnt/ramdsk/logger

cd $LOGGER_DIR

LAST_FILE=$(ls -1 | tail -n1)
echo $LAST_FILE

mount quh:/volume1/Logging/heizung /mnt/quh 

if [ $? -eq 0 ]; then
	cp -r !($LAST_FILE) /mnt/quh
	if [ $? -eq 0 ]; then
		rm -r !($LAST_FILE)
	else
		echo "Could not copy data to network storage"
	fi

	umount /mnt/quh
fi
