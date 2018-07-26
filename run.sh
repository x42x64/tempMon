#!/bin/bash
mkdir /mnt/ramdsk/logger

# Absolute path to this script, e.g. /home/user/bin/foo.sh
SCRIPT=$(readlink -f "$0")
# Absolute path this script is in, thus /home/user/bin
SCRIPTPATH=$(dirname "$SCRIPT")

#LOGGER_IP=$(ip addr show wlan0 | grep "inet " | cut -d' ' -f 6 | cut -d'/' -f 1) LOGGER_DIR=/mnt/ramdsk/logger MPLBACKEND=Agg nohup python3 dataCollector.py > /dev/null &
#LOGGER_IP=$(ip addr show wlan0 | grep "inet " | cut -d' ' -f 6 | cut -d'/' -f 1) LOGGER_DIR=/mnt/ramdsk/logger MPLBACKEND=Agg nohup python3 dataCollector.py > /mnt/ramdsk/logger/log.log &
LOGGER_IP=$(ip addr show wlan0 | grep "inet " | cut -d' ' -f 6 | cut -d'/' -f 1) LOGGER_DIR=/mnt/ramdsk/logger MPLBACKEND=Agg python3 $SCRIPTPATH/dataCollector.py > /mnt/ramdsk/logger/log.log
