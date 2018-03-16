import os
import pandas as pd
import time
from pandas.io.json import json_normalize


os.environ["MPLBACKEND"] = "Agg"
import matplotlib.pyplot as plt

from dataCollectorCallback import DataCollectorCallback


class ImageCreator(DataCollectorCallback):
    def __init__(self, historySeconds, imagepath):
        DataCollectorCallback.__init__(self)

        self.dfRingBuffer = pd.DataFrame()
        self.historySeconds = historySeconds
        self.imagePath = imagepath

    def onData(self, data):
        if data.keys() != []:
            extData = {'data': data}
            newDataEntry = json_normalize(extData)

            # create index timestamp
            dfIdx = pd.DataFrame(columns=["timestamp"])
            dfIdx = dfIdx.append({"timestamp": pd.to_datetime(time.time(), unit='s')}, ignore_index=True)

            # convert timestamps into pandas timestamps
            for clm in filter(lambda k: 'timestamp' in k, list(newDataEntry)):
                newDataEntry[clm] = pd.to_datetime(newDataEntry[clm], unit='s')

            # set index for new dataframe
            newDataEntry.index = dfIdx["timestamp"]

            # append df to ringbuffer
            self.dfRingBuffer = self.dfRingBuffer.append(newDataEntry)

            # remove too old entries from ringbuffer
            self.dfRingBuffer = self.dfRingBuffer.ix[pd.to_datetime(time.time()-self.historySeconds, unit='s'):pd.to_datetime(time.time(), unit='s')]

            keys = ["data.Heat_Resorvoir0.value", "data.Heat_Resorvoir1.value", "data.Heat_Resorvoir2.value", "data.Heat_Resorvoir3.value", "data.SolarHeatExchangeLead.value", "data.SolarHeatExchangeReturn.value" ]

            self.saveImages("graphAllValues", self.dfRingBuffer[keys])
            self.saveImages("HeatResorvoir", self.dfRingBuffer[keys])
            
            keys = ["data.DG_Lead.value", "data.DG_Return.value", "data.EG_Lead.value", "data.EG_Return.value", "data.HeatResorvoir_Lead.value", "data.HeatResorvoir_Return.value", "data.Heater_Lead.value", "data.Heater_Return.value"]
            self.saveImages("HeaterCircuits", self.dfRingBuffer[keys])

            keys = ["data.HeaterActive.value", "data.noiseFFT_3.value", "data.noiseFFT_4.value"]
            self.saveImages("HeaterActivity", self.dfRingBuffer[keys], [0, 1.1])


    def saveImages(self, name, df, ylim = [10.0, 60.0]):
        keys = [x for x in list(df) if ".value" in x]
        df_plot = df[keys]
        ax = df_plot.plot()
        ax.grid(True)
        plt.ylabel("°C")
        plt.xlabel("UTC time (m-d h)")
        ax.set_ylim(ylim)
        fig = plt.gcf()
        fig.set_size_inches(10, 5)
        ax.legend_.remove()

        plt.savefig(os.path.join(self.imagePath, name+".png"))

        fig_legend = plt.figure(figsize=(3.5,4.5))
        fig_legend.legend(ax.get_lines(), [x.replace(".value", "").replace("data.", "") for x in list(df_plot)], loc='center', frameon=False)
        plt.savefig(os.path.join(self.imagePath, name+"Legend.png"))


        plt.close(fig)
        plt.close(fig_legend)
