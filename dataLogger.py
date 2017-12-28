import time
import datetime
import json
import os

from dataCollectorCallback import DataCollectorCallback

class DataLogging(DataCollectorCallback):
    def __init__(self, path):
        DataCollectorCallback.__init__(self)
        self.basepath = path
        self.updatePath()

    def setBasePath(self, path):
        self.path = path

    def updatePath(self):
        filename = datetime.datetime.utcnow().strftime("%Y_%m_%d_%H0000Z.log")
        self.filepath = os.path.join(self.basepath, filename)


    def onData(self, data):
        self.updatePath()
        extData = {'timestamp': time.time(), 'data': data}
        with open(self.filepath, 'a') as file:
            json.dump(extData, file)
            file.write("\n")
