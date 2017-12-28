import datetime
import json
import sensor
import time
import os
import threading

import httpProvider
import dataLogger
import consoleViszualization
import imageCreator



if "LOGGER_IP" in os.environ.keys():
    HTTP_IP = os.environ["LOGGER_IP"]
else:
    HTTP_IP = "127.0.0.1"

HTTP_PORT = 8081

LOGGER_DIR = None
if "LOGGER_DIR" in os.environ.keys():
    LOGGER_DIR = os.environ["LOGGER_DIR"]



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

# second stub
SENSOR_PATHS["Heat_Resorvoir0"] = "28-0000052999e9"
SENSOR_PATHS["Heat_Resorvoir1"] = "28-00000529d886"
SENSOR_PATHS["Heat_Resorvoir2"] = "28-00000529668e"
SENSOR_PATHS["Heat_Resorvoir3"] = "28-00000529829d"
SENSOR_PATHS["SolarHeatExchangeLead"] = "28-0000051af834"
SENSOR_PATHS["SolarHeatExchangeReturn"] = "28-0000052930f4"

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



def getW1Path(deviceID):
    return "/sys/bus/w1/devices/" + deviceID + "/w1_slave"

class DataCollector(threading.Thread):
    lock = threading.Lock()

    def __init__(self):
        threading.Thread.__init__(self)
        self.endRequest = False
        self.callbacks = []

        self.sensors = dict()
        testSensorPath = os.path.join(os.path.dirname(os.path.realpath(__file__)), "test_device", "w1_slave")
        self.sensors["HeatResorvoir2a"] = sensor.ds1820(testSensorPath)
        self.sensors["HeatResorvoirReturnBoiler"] = sensor.ds1820(testSensorPath)
        self.sensors["Ambient"]= sensor.ds1820(testSensorPath)
        self.sensors["Outside"] = sensor.ds1820(testSensorPath)
        self.sensors["Collector"] = sensor.ds1820(testSensorPath)

        # Only use real sensors if HTTP Server is not on loopback
        if HTTP_IP != "127.0.0.1":
            for k in SENSOR_PATHS.keys():
                self.sensors[k] = sensor.ds1820(getW1Path(SENSOR_PATHS[k]))




        DataCollector.lock.acquire()
        self.data = dict()
        DataCollector.lock.release()


    def run(self):
        cont = True

        while cont:


            try:
                start = time.time()

                # query sensors
                for k in self.sensors.keys():
                    self.sensors[k].querySensor()

                # write data
                data = dict()
                DataCollector.lock.acquire()
                for k in self.sensors.keys():
                    self.data[k] = self.sensors[k].getTimeValue()
                DataCollector.lock.release()

                for cb in self.callbacks:
                    cb.onData(self.data)

                duration = time.time() - start
                time.sleep(30.0 - duration)

            except:
                raise

            DataCollector.lock.acquire()
            cont = (self.endRequest == False)
            DataCollector.lock.release()


    def getCurrentData(self):
        DataCollector.lock.acquire()
        ret = self.data
        DataCollector.lock.release()
        return ret

    def stopRequest(self):
        DataCollector.lock.acquire()
        self.endRequest = True
        DataCollector.lock.release()

    def addCallback(self, cb):
        self.callbacks.append(cb)






def main():
    dc = DataCollector()
    httpd = httpProvider.HttpProvider(dc, HTTP_IP, HTTP_PORT)

    if LOGGER_DIR:
        datalogger = dataLogger.DataLogging(LOGGER_DIR)
        dc.addCallback(datalogger)

    visz = consoleViszualization.ConsoleDataVisz()
    #dc.addCallback(visz)

    imgCreator = imageCreator.ImageCreator(120, os.getcwd())
    dc.addCallback(imgCreator)

    dc.start()
    httpd.start()


    while True:
        try:
            time.sleep(1)

        except KeyboardInterrupt:
            dc.stopRequest()
            httpd.stopRequest()
            print("Stop might take up to 30s. Please wait...")
            break
        except:
            raise


    dc.join()
    print("DC done")
    httpd.join()
    print("Application ended.")

#solarController = hysteresis(20.0, 15.0)

if __name__ == "__main__":
    main()




