import datetime
import time
import matplotlib
import numpy

def testing_data():
    dates, prices, volumes = [], [], []
    try:
        source_code = open('btceUSD.csv', 'r').read()
        split_source = ssource_code.split('\n')
        for line in split_source[-50000:]:
            split_line = line.split(',')
            dates.append(float(split_line[0]))
            prices.append(float(split_line[1]))
            volumes.append(float(split_line[2]))
    except Exception as exception:
        print('Failed:Raw Data:' + str(exception))
    matplotlib.pyplot.plot(dates, prices)
    matplotlib.pyplot.show()

if __name__ == '__main__':
    testing_data()