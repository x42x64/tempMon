import time
import BMP280

class sensor:

    def __init__(self):
        self.ts = -1
        self.value = -255.0
        self.unit = "-"

    def querySensor(self):
        raise NotImplementedError
        pass

    def getValue(self):
        return self.value

    def getTimeValue(self):
        return {"timestamp":self.ts, "value":self.value, "unit":self.unit}

    def getId(self):
        return self.id


class ds1820(sensor):

    def __init__(self, path):
        sensor.__init__(self)
        self.unit = "°C"
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

class bmp280Temp():

    def __init__(self):
        sensor.__init__(self)
        self.unit = "°C"
        self.bmp280 = BMP280.BMP180()

    def querySensor(self):
        self.value, _ = self.bmp280.get_temperature_and_pressure()


class bmp280Pressure():
    def __init__(self):
        sensor.__init__(self)
        self.unit = "kPa"
        self.bmp280 = BMP280.BMP180()

    def querySensor(self):
        _, self.value = self.bmp280.get_temperature_and_pressure()






