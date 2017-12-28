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

            self.saveImages()


    def saveImages(self):
        keys = [x for x in list(self.dfRingBuffer) if ".value" in x]
        df_plot = self.dfRingBuffer[keys]
        ax = df_plot.plot()
        ax.grid(True)
        plt.ylabel("°C")
        plt.xlabel("UTC time (m-d h)")
        fig = plt.gcf()
        fig.set_size_inches(10, 5)
        ax.legend_.remove()
        plt.savefig(os.path.join(self.imagePath, "graphHeatResorvoir.png"))

        print(list(df_plot))
        fig_legend = plt.figure(figsize=(3.5, 1.5))
        fig_legend.legend(ax.get_lines(), list(df_plot), loc='center', frameon=False)
        plt.savefig(os.path.join(self.imagePath, "graphHeatResorvoirLegend.png"))

