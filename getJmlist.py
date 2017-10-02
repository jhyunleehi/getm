#!/usr/bin/python
import os
import re
import urllib
import urllib2
from bs4 import BeautifulSoup

url="http://bigdata-trader.com/itemcodehelp.jsp"

conn = urllib.urlopen(url)
html = conn.read()
soup = BeautifulSoup(html.decode("utf-8"), "lxml")
line = soup.find_all("tr")
jmList = {}
p=re.compile('[a-zA-Z]')
for i in range(0, len(line)):
    jmCode = line[i].find_all("td")[0].text
    jmName =  line[i].find_all("td")[1].text
    jmPart =  line[i].find_all("td")[2].text
    m=p.match(jmCode)
    if m:
        print jmCode
    else:
        jmList[jmCode] = jmName
        #print jmCode, jmName, jmPart
f = open("jmList.dat","w")
keys = jmList.keys()
keys.sort()
for k in keys:
    wLine = k + " " + jmList[k] +"\n"
    f.write(wLine.encode('utf-8'))
f.close()
