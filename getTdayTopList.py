#!/usr/bin/python
import os
import time
import re
import urllib
from   bs4 import BeautifulSoup


url="http://finance.naver.com/sise/lastsearch2.nhn"
conn=urllib.urlopen(url)
html=conn.read()
source=BeautifulSoup(html.decode("euc-kr"), "html.parser")
tbody=source.find_all("table", class_="type_5")
items=tbody[0].find_all("a")
topjongmok={}
for i in range(0, len(items) ):
    code    = items[i].get('href')[20:]
    name = items[i].text
    topjongmok[code]=name
f=open('TdayTopList.dat','w')
keys= topjongmok.keys()

for i in keys:
    line = i + ' ' + topjongmok[i]+'\n'
    f.write(line.encode('utf-8'))
    print line.encode('utf-8'),
f.close()
