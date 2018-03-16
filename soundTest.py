import numpy as np
import pyaudio
import time

import soundProcessor

#import matplotlib.pyplot as plt

class SpectrumAnalyzer:
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
    sim = False
    wf = None

    def __init__(self, sim=False):
        self.sim = sim


        if not sim:
            self.pa = pyaudio.PyAudio()
            self.stream = self.pa.open(format = self.FORMAT,
                channels = self.CHANNELS,
                rate = self.RATE,
                input = True,
                output = False,
                frames_per_buffer = self.CHUNK,
                input_device_index=2)
        else:
            import wave
            self.wf = wave.open('heizung_pi.wav','rb')

        # Main loop
        self.loop()

    def loop(self):
        try:
            i = 0
            while True :
                self.data = self.audioinput()
                if not self.data.any():
                    break

                self.fft()
                self.update_aggregate(0.005)
                if i%50 == 0:
                    self.graphplot()
                    print("Stream time: " + str(float(i) / self.RATE * self.CHUNK))
                    self.consoleOut()

                i=i+1



        except KeyboardInterrupt:
            self.pa.close(self.stream)

        print("End...")

    def audioinput(self):
        if self.sim:
            ret = self.wf.readframes(self.CHUNK)
            sw = self.wf.getsampwidth()
            ret = np.fromstring(ret, np.int16).astype(dtype=np.float32)/32768.0
        else:
            ret = self.stream.read(self.CHUNK, exception_on_overflow=False)
            ret = np.fromstring(ret, np.float32)
        ret = ret - np.mean(ret)
        return ret

    def fft(self):
        self.wave_x = range(self.START, self.START + self.N)
        self.wave_y = self.data[self.START:self.START + self.N]
        self.spec_x = np.fft.fftfreq(self.N, d = 1.0 / self.RATE)
        y = np.fft.fft(self.data[self.START:self.START + self.N])
        self.spec_y = np.array([np.sqrt(c.real ** 2 + c.imag ** 2) for c in y])

    def update_aggregate(self, phi):
        if self.spec_y_aggr is None:
            self.spec_y_aggr = self.spec_y

        self.spec_y_aggr = self.spec_y_aggr * (1.0-phi) + self.spec_y * phi


#    def graphplot(self):
#        plt.clf()
#        # wave
#        plt.subplot(311)
#        plt.plot(self.wave_x, self.wave_y)
#        plt.axis([self.START, self.START + self.N, -0.5, 0.5])
#        plt.xlabel("time [sample]")
#        plt.ylabel("amplitude")
#        #Spectrum
#        plt.subplot(312)
#        plt.plot(self.spec_x, self.spec_y_aggr, marker= 'o', linestyle='-')
#        plt.axis([0, self.RATE / 2, 0, 50])
#        plt.xlabel("frequency [Hz]")
#        plt.ylabel("amplitude spectrum")
#        #Pause
#        plt.pause(.01)

    def consoleOut(self):
        print(self.spec_y_aggr[0:6])
        #if self.spec_y_aggr[4] > 0.65:
        #    print("On")
        #else:
        #    print("Off")

if __name__ == "__main__":
    p = pyaudio.PyAudio()
    info = p.get_host_api_info_by_index(0)
    numdevices = info.get('deviceCount')
    #for i in range(0, numdevices):
    #    if (p.get_device_info_by_host_api_device_index(0, i).get('maxInputChannels')) > 0:
    #        print("Input Device id ", i, " - ", p.get_device_info_by_host_api_device_index(0, i).get('name'))

    #spec = SpectrumAnalyzer(sim=True)

    sp1 = soundProcessor.soundProcessor()
    sp2 = soundProcessor.soundProcessor()
    sp3 = soundProcessor.soundProcessor()

    for _ in range(40):
        print(str(sp1.get_heater_state()) + " " +
              str(sp2.get_fft(3)) + " " +
              str(sp3.get_fft(4)) )

        time.sleep(5)
