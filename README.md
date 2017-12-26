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

Reboot!

### RAM Disk
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
```
12 */2 * * * /home/pi/projects/heizung/mv2loggingstorage.sh
```
