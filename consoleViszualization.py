import time

from dataCollectorCallback import DataCollectorCallback


def clearScreen():
    print(chr(27) + "[2J")


class ConsoleDataVisz(DataCollectorCallback):
    def __init__(self):
        DataCollectorCallback.__init__(self)

    def onData(self, data):
        clearScreen()
        print(time.strftime("%H:%M:%S"))
        print("----------------------")
        for k in sorted(data.keys()):
            print('%-30s%10f °C' % (k, data[k]["value"]))




