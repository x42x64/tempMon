#!/bin/bash
mkdir /mnt/ramdsk/logger
LOGGER_IP=$(ip addr show wlan0 | grep "inet " | cut -d' ' -f 6 | cut -d'/' -f 1) LOGGER_DIR=/mnt/ramdsk/logger MPLBACKEND=Agg nohup python3 dataCollector.py > /dev/null &
