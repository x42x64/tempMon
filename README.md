# tempMon

## Setup Raspberry Pi
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
