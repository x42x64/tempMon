#!/bin/bash

sudo mount quh:/volume1/Logging/heizung /mnt/quh 

if [ $? -eq 0 ]; then
	MPLBACKEND=Agg python3 /home/pi/projects/heizung/analysis/createImage.py
	sudo umount /mnt/quh
fi
