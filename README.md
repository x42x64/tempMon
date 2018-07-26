# tempMon

## Setup Raspberry Pi
### One Wire Interface
Sources: 
* http://www.netzmafia.de/skripten/hardware/RasPi/Projekt-Onewire/index.html, 
* https://www.raspberrypi.org/forums/viewtopic.php?f=44&t=65137&start=50#p1185342
* https://pinout.xyz/

Load kernel modules
```
# /etc/modules
w1-gpio pullup=1
w1-therm
```

Set maximum number of node for the driver
```
# /etc/modprobe.d/1-wire.conf 
options wire max_slave_count=18
```

Set the w1 pin(s)
```
# /boot/config.txt
dtoverlay=w1-gpio,gpiopin=4
dtoverlay=w1-gpio,gpiopin=17
```

Activate i2c and spi:
Link: http://www.netzmafia.de/skripten/hardware/RasPi/RasPi_I2C.html
# /boot/config.txt
dtparam=i2c1=on
dtparam=i2c_arm=on
dtparam=spi=on


Reboot!

### RAM Diskasdf
Sources:
* http://www.kriwanek.de/index.php/de/raspberry-pi/265-ram-disk-auf-raspberry-pi-einrichten

Create a folder:
```
mkdir /mnt/ramdsk
```

Edit fstab:
```
# /etc/fstab
tmpfs           /mnt/ramdsk     tmpfs   nodev,nosuid,size=128M 0 0
```

Remount:
```
sudo mount -a
```

### Create cronjob to move data from ramdisk to network drive
Create a cronjob which should be run as root:
```
sudo crontab -e
```

Actual cronjob: Run script at minute 12 every second hour.
See also: https://crontab.guru/#12_*/2_*_*_*
```
12 */2 * * * /home/pi/projects/heizung/mv2loggingstorage.sh
```

### Setup for autostart
See: https://www.stuffaboutcode.com/2012/06/raspberry-pi-run-program-at-start-up.html

create a service script which runs the run.sh script as pi user.
Use sudo -u in order to run as different user.
Watch the pkill argument on how to stop the service.
Script:
```
#! /bin/sh
# /etc/init.d/heizung

### BEGIN INIT INFO
# Provides:          heizung
# Required-Start:    $remote_fs $syslog
# Required-Stop:     $remote_fs $syslog
# Default-Start:     2 3 4 5
# Default-Stop:      0 1 6
# Short-Description: Simple script to start a program at boot
# Description:       A simple script from www.stuffaboutcode.com which will sta$
### END INIT INFO

# If you want a command to always run, put it here

# Carry out specific functions when asked to by the system
case "$1" in
  start)
    echo "Starting heizung"
    # run application you want to start
    sudo -u pi /home/pi/projects/heizung/run.sh&
    ;;
  stop)
    echo "Stopping heizung"
    # kill application you want to stop
    pkill -f "python3.*dataCollector.py"
    ;;
  *)
    echo "Usage: /etc/init.d/heizung {start|stop}"
    exit 1
    ;;
esac

exit 0 

```

Register the script on startup:
```
sudo update-rc.d heizung defaults
```
Unregister the script from startup:
```
sudo update-rc.d -f heizung remove
```

