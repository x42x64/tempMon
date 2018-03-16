import pyaudio
import numpy as np
import time

class soundProcessor:
    class __soundProcessor:
        FORMAT = pyaudio.paFloat32
        CHANNELS = 1
        RATE = 48000
        CHUNK = 512
        START = 0
        N = 512

        wave_x = 0
        wave_y = 0
        spec_x = 0
        spec_y = 0
        spec_x_aggr = None
        spec_y_aggr = None
        data = []

        last_update = None

        def __init__(self, input_device_index=2):
            self.pa = pyaudio.PyAudio()
            self.stream = self.pa.open(format=self.FORMAT,
                                       channels=self.CHANNELS,
                                       rate=self.RATE,
                                       input=True,
                                       output=False,
                                       frames_per_buffer=self.CHUNK,
                                       input_device_index=input_device_index)
            self.wave_x = range(self.START, self.START + self.N)
            self.spec_x = np.fft.fftfreq(self.N, d=1.0 / self.RATE)

        def __del__(self):
            if self.stream:
                self.pa.close(self.stream)

        def __audioinput(self):
            ret = self.stream.read(self.CHUNK, exception_on_overflow=False)
            ret = np.fromstring(ret, np.float32)
            ret = ret - np.mean(ret)
            return ret

        def __fft(self):
            self.wave_y = self.data[self.START:self.START + self.N]
            y = np.fft.fft(self.data[self.START:self.START + self.N])
            self.spec_y = np.array([np.sqrt(c.real ** 2 + c.imag ** 2) for c in y])

        def __update_aggregate(self, phi):
            if self.spec_y_aggr is None:
                self.spec_y_aggr = self.spec_y

            self.spec_y_aggr = self.spec_y_aggr * (1.0 - phi) + self.spec_y * phi

        def __update(self):
            if not self.last_update or (time.time() - self.last_update) > 10.0:
                for _ in range(20):
                    self.data = self.audioinput()
                    self.fft()
                    self.update_aggregate(0.05)
                self.last_update = time.time()

        def get_fft(self, idx):
            self.__update()
            return self.spec_y_aggr[idx]

        def get_heater_state(self):
            self.__update()

            ret = None
            if self.spec_y_aggr[3] > 0.5 or self.spec_y_aggr[4] > 0.8:
                ret = 1.0
            else:
                ret = 0.0

            return ret

        def get_last_update_time(self):
            return self.last_update


    instance = None

    def __init__(self):
        if not soundProcessor.instance:
            soundProcessor.instance = soundProcessor.__soundProcessor()

    def __getattr__(self, item):
        return getattr(self.instance, item)