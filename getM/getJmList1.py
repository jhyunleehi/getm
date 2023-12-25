#!/usr/bin/python
import os
import time
import re
import urllib
from   bs4 import BeautifulSoup

url="http://bigdata-trader.com/itemcodehelp.jsp"
conn=urllib.urlopen(url)
html=conn.read()
source=BeautifulSoup(html.decode("utf-8"), "lxml")
line=source.find_all("tr")
jmList = {}
for i in range(0, len(line)):
    jmCode = line[i].find_all("td")[0].text
    jmName =  line[i].find_all("td")[1].text
    jmPart =  line[i].find_all("td")[2].text
    jmList[jmCode] = jmName
    print jmCode, jmName, jmPart
f = open("jmList.dat","w")
keys = jmList.keys()

for k in keys:
    wLine = k + " " + jmList[k] +"\n"
    f.write(wLine.encode('utf-8'))
f.close()
