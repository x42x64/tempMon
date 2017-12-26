import time

class sensor:

    def __init__(self):
        self.ts = -1
        self.value = -255.0

    def querySensor(self):
        raise NotImplementedError
        pass

    def getValue(self):
        return self.value

    def getTimeValue(self):
        return {"timestamp":self.ts, "value":self.value}

    def getId(self):
        return self.id


class ds1820(sensor):

    def __init__(self, path):
        sensor.__init__(self)
        self.path = path

    def getPath(self):
        return self.path

    def querySensor(self):

        try:

            with open(str(self.path)) as file:
                filecontent = file.read()
    
                # Temperaturwerte auslesen und konvertieren
                stringvalue = filecontent.split("\n")[1].split(" ")[9]
                self.value = float(stringvalue[2:]) / 1000.0

                self.ts = time.time()

        except:
            print("Could not read sensor " + self.path)




