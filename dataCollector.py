import json
import sensor
import time
import os
import threading

from http.server import BaseHTTPRequestHandler, HTTPServer

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


class DataCollectorCallback:
    def __init__(self):
        pass

    def onData(self, data):
        raise NotImplementedError

class DataLogging(DataCollectorCallback):
    def __init__(self, path):
        DataCollectorCallback.__init__(self)
        self.path = path

    def setPath(self, path):
        self.path = path

    def onData(self, data):
        extData = {'timestamp': time.time(), 'data': data}
        with open(self.path, 'a') as file:
            json.dump(extData, file)
            file.write("\n")

class httpProvider(threading.Thread):
    dc = None
    lock = threading.Lock()

    def __init__(self, dataCollector):
        threading.Thread.__init__(self)
        self.endRequest = False
        httpProvider.dc = dataCollector


    class httpServer_RequestHandler(BaseHTTPRequestHandler):
        # GET
        def do_GET(self):
            # Send response status code
            self.send_response(200)

            # Send headers
            self.send_header('Content-type', 'text/html')
            self.end_headers()

            # Send message back to client
            message = json.dumps(httpProvider.dc.getCurrentData())
            # Write content as utf-8 data
            self.wfile.write(bytes(message, "utf8"))
            return

    def stopRequest(self):
        self.httpd.shutdown()

    def run(self):
        print('starting server...')

        # Server settings
        # Choose port 8080, for port 80, which is normally used for a http server, you need root access
        server_address = ('127.0.0.1', 8081)
        self.httpd = HTTPServer(server_address, httpProvider.httpServer_RequestHandler)
        print('running server...')

        try:
            self.httpd.serve_forever()
        finally:
            self.httpd.server_close()


def clearScreen():
    print(chr(27) + "[2J")

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
        self.sensors["HeatResorvoir0"] = sensor.ds1820(testSensorPath)
        self.sensors["HeatResorvoir1"] = sensor.ds1820(testSensorPath)
        self.sensors["HeatResorvoir2"] = sensor.ds1820(testSensorPath)
        self.sensors["HeatResorvoir3"] = sensor.ds1820(testSensorPath)
        self.sensors["SolarHeatExchangeLead"] = sensor.ds1820(testSensorPath)
        self.sensors["SolarHeatExchangeReturn"] = sensor.ds1820(testSensorPath)
        self.sensors["HeatResorvoir2a"] = sensor.ds1820(testSensorPath)
        self.sensors["HeatResorvoirReturnBoiler"] = sensor.ds1820(testSensorPath)

        #for k in SENSOR_PATHS.keys():
        #    self.sensors[k] = sensor.ds1820(getW1Path(SENSOR_PATHS[k]))

        self.sensors["Ambient"]= sensor.ds1820(testSensorPath)
        self.sensors["Outside"] = sensor.ds1820(testSensorPath)

        self.sensors["Collector"] = sensor.ds1820(testSensorPath)


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
    httpd = httpProvider(dc)
    datalogger = DataLogging("/tmp/logger2.log")
    dc.addCallback(datalogger)
    dc.start()
    httpd.start()


    while True:
        try:
            #clearScreen()
            data = dc.getCurrentData()
            #for k in data.keys():
            #    print(k + ": \t" + str(data[k]["value"]) + "°C")

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




