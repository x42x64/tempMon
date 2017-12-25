To add a star topology of a one wire network to the raspberry pi:
https://www.raspberrypi.org/forums/viewtopic.php?f=44&t=65137&start=50#p1185342

> Fortunately since Raspberry Pi kernel 4.9.28, you can setup multiple gpio 1-Wire buses by executing as root e.g.:
```
dtoverlay w1-gpio gpiopin=22 pullup=0
dtoverlay w1-gpio gpiopin=23 pullup=0
dtoverlay w1-gpio gpiopin=25 pullup=0
sleep 5
ls -l /sys/bus/w1/devices/
```
