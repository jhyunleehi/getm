#!/usr/bin/python
import os
import time
import re
import urllib
from   bs4 import BeautifulSoup

def toint(numstr):
    p=re.compile('[0-9]+')
    m=p.findall(numstr)
    retstr=''
    for i in m:
        retstr=retstr+i
    #retnum=int(m.group())
    return retstr

def getbypage(url,code):
    filename="jmdata/"+code+".data"
    #f=open(filename,'a')
    u=urllib.urlopen(url)
    html=u.read()
    source=BeautifulSoup(html,"html.parser")
    trlists=source.find_all("tr")
    f=open(filename,'a')
    for i in range(1, len(trlists)-1):
        if(trlists[i].span != None):
             #trlists[i].td.text
             sdate=trlists[i].find_all("td",align="center")[0].text
             endp =trlists[i].find_all("td",class_="num")[0].text
             stp  =trlists[i].find_all("td",class_="num")[2].text
             htp  =trlists[i].find_all("td",class_="num")[3].text
             ltp  =trlists[i].find_all("td",class_="num")[4].text
             exch =trlists[i].find_all("td",class_="num")[5].text
             print sdate, endp, stp, htp, ltp, exch
             line=sdate+' '+toint(endp)+' '+toint(stp)+' '+toint(htp)+' '+toint(ltp)+' '+toint(exch)+'\n'
             #print line
             f.write(line)
    f.close()

def getbycode(url, code):

    print url, code
    if os.path.isfile("jmdata/"+code+".data"):
        file_exists=True
    else:
        file_exists=False
    nurl=url+"?code="+code+"&"+"page=1"
    #print nurl
    u=urllib.urlopen(nurl)
    html=u.read()
    source=BeautifulSoup(html, "html.parser")
    maxPage=source.find_all("table",align="center")
    mp=maxPage[0].find_all("td",class_="pgRR")
    mpNum= (mp[0].a.get('href')[-3:])
    pat=re.compile("[0-9]+")
    mxNum=int(pat.search(mpNum).group(0))
    if file_exists:
        mxNum=1
    for page in range(1, mxNum+1):
        #print page, str(page)
        pageurl=url+"?code="+code+"&"+"page="+str(page)
        print pageurl
        time.sleep(0.01)
        getbypage(pageurl,code)
    filename = "jmdata/"+code + ".data"
    f=open(filename,'r')
    lines=f.readlines()
    f.close()
    jongmokDIC={}
    for  line in lines:
        key=line[0:10]
        val=line[10:]
        jongmokDIC[key]=val
    keylist=jongmokDIC.keys()
    keylist.sort()
    f=open(filename,'w')
    for i in keylist:
        line=i+' ' + jongmokDIC[i]
        f.write(line)
    f.close()

url="http://finance.naver.com/item/sise_day.nhn"
f=open("targetJMList.dat","r")
line=f.readlines()
items=[]
for i in line:
    item=i.split()
    items.append(item[0])

for i in items:
    getbycode(url,i)
