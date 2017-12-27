import pandas as pd
import json
import glob
import os

import time
import datetime
from itertools import compress

def loadLogsAsDF(loggingDir, start = 0, end = time.time()):
    lst = []

    filepathlist = glob.glob(os.path.join(loggingDir, "*.log"))

    # filter only relevant files for the selected time
    filelist = [datetime.datetime.strptime(os.path.basename(x)[:-4], "%Y_%m_%d_%H%M%SZ") for x in filepathlist]
    subselection = [(x.timestamp() > int(start/3600)*3600.0 and x.timestamp() < int(end/3600)*3600.0) for x in filelist]



    for fn in list(compress(filepathlist,subselection)):
        with open(fn) as f:
            content = f.readlines()

        content = [x.strip() for x in content]


        for line in content:
            lst.append(json.loads(line))



    df = pd.io.json.json_normalize(lst)

    # set index
    for clm in filter(lambda k: 'timestamp' in k, list(df)):
        df[clm] = pd.to_datetime(df[clm], unit='s')

    df.index = df['timestamp']
    del df['timestamp']

    return df




