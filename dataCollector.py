import json
import sensor
import time

class hysteresis:
    def __init__(self, upper, lower):
        self.state = False
        self.upper = upper
        self.lower = lower

    def check(self, value):
        if self.state:
            if value < self.lower:
                self.state = False

        else:
            if value > self.upper:
                self.state = True

        return self.state

    def getState(self):
        return self.state

class datalogger:
    def __init__(self, path):
        self.path = path
        self.numLogLines = 0
        with open(path, 'w') as file:
            file.write("{'loggingdata':[")

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        with open(self.path, 'a') as file:
            file.write("]}")

    def log(self, d):
        extData = {'ts': time.time(), 'data': d}
        print(extData)
        with open(self.path, 'a') as file:
            if self.numLogLines > 0:
                file.write(",")

            json.dump(extData, file)
            self.numLogLines += 1




sensors = dict()

#sensors["HeatResorvoir0"] = sensor.ds1820("/sys/bus/w1/devices/" + str("bla") + "/w1_slave")
sensors["HeatResorvoir0"] = sensor.ds1820("/home/jan/projects/heizung/test_device" + "/w1_slave")
sensors["HeatResorvoir1"] = sensor.ds1820("/home/jan/projects/heizung/test_device" + "/w1_slave")
sensors["HeatResorvoir2"] = sensor.ds1820("/home/jan/projects/heizung/test_device" + "/w1_slave")
sensors["HeatResorvoir3"] = sensor.ds1820("/home/jan/projects/heizung/test_device" + "/w1_slave")
sensors["SolarHeatExchangeLead"] = sensor.ds1820("/home/jan/projects/heizung/test_device" + "/w1_slave")
sensors["SolarHeatExchangeReturn"] = sensor.ds1820("/home/jan/projects/heizung/test_device" + "/w1_slave")
sensors["HeatResorvoir2a"] = sensor.ds1820("/home/jan/projects/heizung/test_device" + "/w1_slave")
sensors["HeatResorvoirReturnBoiler"] = sensor.ds1820("/home/jan/projects/heizung/test_device" + "/w1_slave")
sensors["UG_Lead"]= sensor.ds1820("/home/jan/projects/heizung/test_device" + "/w1_slave")
sensors["UG_Return"] = sensor.ds1820("/home/jan/projects/heizung/test_device" + "/w1_slave")
sensors["EG_Lead"]= sensor.ds1820("/home/jan/projects/heizung/test_device" + "/w1_slave")
sensors["EG_Return"] = sensor.ds1820("/home/jan/projects/heizung/test_device" + "/w1_slave")
sensors["OG_Lead"]= sensor.ds1820("/home/jan/projects/heizung/test_device" + "/w1_slave")
sensors["OG_Return"] = sensor.ds1820("/home/jan/projects/heizung/test_device" + "/w1_slave")
sensors["HeatResorvoir_Lead"]= sensor.ds1820("/home/jan/projects/heizung/test_device" + "/w1_slave")
sensors["HeatResorvoir_Return"] = sensor.ds1820("/home/jan/projects/heizung/test_device" + "/w1_slave")

sensors["Ambient"]= sensor.ds1820("/home/jan/projects/heizung/test_device" + "/w1_slave")
sensors["Outside"] = sensor.ds1820("/home/jan/projects/heizung/test_device" + "/w1_slave")

sensors["Collector"] = sensor.ds1820("/home/jan/projects/heizung/test_device" + "/w1_slave")

solarController = hysteresis(20.0, 15.0)

with datalogger('/home/jan/projects/heizung/test_device/test.log') as dl:
    while True:
        try:
            start = time.time()

            # query sensors
            for k in sensors.keys():
                sensors[k].querySensor()

            # write data
            data = dict()
            for k in sensors.keys():
                data[k] = sensors[k].getTimeValue()




            # do actions
            #   activate solar pump
            data["solarPump"] = solarController.check(sensors["Collector"].getValue())
            data["boilerPump"] = False

            #   activate boiler pump





            # write to logfile
            dl.log(data)

            print(data)

            duration = time.time() - start
            time.sleep(10.0 - duration)

        except KeyboardInterrupt:
            break

        except:
            raise


