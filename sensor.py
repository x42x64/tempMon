import time
import BMP280
import soundProcessor

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

class bmp280Temp(sensor):

    def __init__(self):
        sensor.__init__(self)
        self.unit = "°C"
        self.bmp280 = BMP280.BMP180()

    def querySensor(self):
        self.value, _ = self.bmp280.get_temperature_and_pressure()


class bmp280Pressure(sensor):
    def __init__(self):
        sensor.__init__(self)
        self.unit = "kPa"
        self.bmp280 = BMP280.BMP180()

    def querySensor(self):
        _, self.value = self.bmp280.get_temperature_and_pressure()

class heaterActive(sensor):
    def __init__(self):
        sensor.__init__(self)
        self.unit = "-"
        self.soundProcessor = soundProcessor.soundProcessor()

    def querySensor(self):
        self.value = self.soundProcessor.get_heater_state()
        self.ts = self.soundProcessor.get_last_update_time()

class noiseFFT(sensor):
    def __init__(self, fft_idx):
        sensor.__init__(self)
        self.unit = "-"
        self.soundProcessor = soundProcessor.soundProcessor()
        self.fft_idx = fft_idx

    def querySensor(self):
        self.value = self.soundProcessor.get_fft(self.fft_idx)
        self.ts = self.soundProcessor.get_last_update_time()




