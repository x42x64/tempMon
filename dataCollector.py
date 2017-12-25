import json
import sensor
import time

SENSOR_PATHS = dict()
SENSOR_PATHS["DG_Lead"] = "28-00000529cf95"
SENSOR_PATHS["DG_Return"] = "28-0000052997b1"
SENSOR_PATHS["EG_Lead"] = "28-000005298431"
SENSOR_PATHS["EG_Return"] = "28-000005298f89"
SENSOR_PATHS["HeatResorvoir_Lead"] = "28-0000052972cb"
SENSOR_PATHS["HeatResorvoir_Return"] = "28-00000529790f"
SENSOR_PATHS["UG_Lead"] = "28-00000529489e"
SENSOR_PATHS["UG_Return"] = "28-00000529685d"
SENSOR_PATHS["DG_Lead"] = "28-00000529cf95"
SENSOR_PATHS["Heater_Lead"] = "28-00000529aaec"
SENSOR_PATHS["Heater_Return"] = "28-000005293bb5"

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


def getW1Path(deviceID):
    return "/sys/bus/w1/devices/" + deviceID + "/w1_slave"

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

for k in SENSOR_PATHS.keys():
    sensors[k] = sensor.ds1820(getW1Path(SENSOR_PATHS[k]))

sensors["Ambient"]= sensor.ds1820("/home/jan/projects/heizung/test_device" + "/w1_slave")
sensors["Outside"] = sensor.ds1820("/home/jan/projects/heizung/test_device" + "/w1_slave")

sensors["Collector"] = sensor.ds1820("/home/jan/projects/heizung/test_device" + "/w1_slave")

solarController = hysteresis(20.0, 15.0)

with datalogger('/tmp/test.log') as dl:
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
            time.sleep(30.0 - duration)

        except KeyboardInterrupt:
            break

        except:
            raise


