import csv
import time
import json
import requests
import numpy as np
import gevent.monkey
import urllib
from datetime import datetime
from urllib.request import urlopen

start_time = time.time()
header_row = False
count = 0
file_name = "dust_result_" + time.strftime("%Y%m%d-%H%M%S") + ".csv"

# urls = ['https://api.waqi.info/mapq/bounds/?bounds=26.748288,97.037243,50.571187,1153.902477&inc=placeholders&k=_2Y2EzVBxYGVgdIzsJSBRWXmldaA09PSNWFXgZZQ==&_=1491802275939']

xmax = 153
xmin = 97

ymax = 46
ymin = 22

# x_list = np.linspace(xmin,xmax,10)
# y_list = np.linspace(ymin,ymax,10)
x_list = np.arange(xmin,xmax,2)
y_list = np.arange(ymin,ymax,2)

urls = []
for x_idx, x in enumerate(x_list):
    for y_idx, y in enumerate(y_list):
        if x_idx > 0 and y_idx > 0:
            urls.append('https://api.waqi.info/mapq/bounds/?bounds='+ str(y_list[y_idx-1]) + ',' + str(x_list[x_idx-1]) + ',' + str(y) + ',' + str(x) +'&inc=placeholders&k=_2Y2EzVBxmFRAdIyNNSzJWXmldaAw9AzdWFlY7IA==&_=1492570231356')
        # print(x)
        # print(y)

print(len(urls))


def print_head(url):
    global header_row
    # print('Starting {}'.format(url))
    data = urlopen(url).read().decode('utf8')
    resultstr = json.loads(data)

    print("length:", str(len(resultstr)))

    with open(file_name, "a", encoding='utf-8') as outcsv:

        dict_writer = csv.DictWriter(outcsv,
                                     fieldnames=["lat", "lon", "city", "idx", "stamp", "pol", "x", "aqi", "tz",
                                                 "utime", "img"], delimiter=',', lineterminator='\n')
        if header_row == False:
            dict_writer.writeheader()
            header_row = True
        dict_writer.writerows(resultstr)

    print("--- %s seconds ---" % (time.time() - start_time))

jobs = [gevent.spawn(print_head, _url) for _url in urls]

gevent.wait(jobs)
