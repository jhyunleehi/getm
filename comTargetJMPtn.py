#!/usr/bin/python
#-*- coding: utf-8 -*-

import os
import re
import time
import urllib
from   bs4 import BeautifulSoup
import datetime
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

#-----------------------------------
# 숫자 만 분리; 뭔가 더 좋은 방법이 있을 거 같은데...
def toint(numstr):
    p=re.compile('[0-9]+')
    m=p.findall(numstr)
    retstr=''
    for i in m:
        retstr=retstr+i
    #retnum=int(m.group())
    return retstr

def getURLJmHistory(code):
    url = "http://finance.naver.com/item/sise_day.nhn"
    jmurl = url + "?code=" + code + "&" + "page=1"
    u=urllib.urlopen(jmurl)
    html=u.read()
    source=BeautifulSoup(html,"html.parser")
    trlists=source.find_all("tr")
    result=[]
    temp={}
    for i in range(1, len(trlists)-1):
        if(trlists[i].span != None):
            #trlists[i].td.text
            sdate=trlists[i].find_all("td",align="center")[0].text
            endp =trlists[i].find_all("td",class_="num")[0].text
            stp  =trlists[i].find_all("td",class_="num")[2].text
            #print sdate, endp, stp
            temp[sdate]=toint(endp)
    tempkey=temp.keys()
    tempkey.sort()
    #print tempkey
    ep1=0
    ep2=0
    for i in tempkey:
        ep2=temp[i]
        if ((ep1 <= ep2)and(ep1!=0)):
            result.append(1)
        elif ((ep1 > ep2)and(ep1!=0)):
            result.append(0)
        ep1=ep2
    #print temp
    return result

#-----------------------------------
# 분석된 패턴 파일을 읽어와서 메모리에 적재
f=open("Pattern.dat","r")
PTN={}
lines= f.readlines()
for i in lines:
    item = i.split()
    key  = int(item[0])
    value = int(item[1])
    PTN[key]=value
f.close()

#-----------------------------------
# target jongmok을 읽어 온다.
f=open("targetJMList.dat","r")
line=f.readlines()
JM=[]
JMD={}
for i in line:
    JM.append(i.split()[0])           #종목 코드값
    JMD[i.split()[0]] =i.split()[1]   #종목 이름
#print JMD
f.close()

f=open("targetJMListPtn.out","a")
now=datetime.datetime.now()
line= '\n###'+ str(now)+'\n'
f.write(unicode(line))
line= 'code   SU%  SD%  LU% LD%  NAME\n'
f.write(unicode(line))
#-----------------------------------
# url에서 종목의 변동 이력을 읽어 온다.
for code in JM:
    time.sleep(0.01)
    JMdata= getURLJmHistory(code)
    srtk=0
    endk =0
    #JMdata=[0,1,0,1,0,1,0,1,0,1,0,1]
    if (len(JMdata) >= 4):                  #제공된 예측 패턴 값이 4이하면 계산하지 않는다.
        #print JMdata
        for i in range(0, len(JMdata)):    #검색 대상 범위선정을 위해서  startkey, endkey를 결정한다.
            if(JMdata[i]==1):
                srtk = srtk | 0x1
                endk = endk | 0x1
            else:
                srtk= srtk | 0x0
                endk = endk | 0x0
            srtk= srtk << 0x1
            endk  = endk << 0x1
        for i in range(0, 15-len(JMdata)):
            srtk = srtk | 0x0
            endk = endk | 0x1
            srtk= srtk << 1
            endk  = endk << 1
        srtk = srtk | 0x0
        endk = endk | 0x1
        sumup=0                                #누적상승값
        sumdown=0                              #누적하락값
        nxtup=0                                #검색 패턴 다음일자 상승
        nxtdown=0                              #검색 패턴 다음일자 하락
        for i in range(srtk,endk+1):
            if (PTN[i] != 0):
                val=i
                ptn=PTN[i]                     #ptn  값이 0일때는 계산하지 않지만 값이 있는 경우 가중치 적용
                for j in range(1, 16-len(JMdata)+1):
                    if ((val&1) ==1):         #입력된 패턴 이후 16비트 까지의 패턴을 전체 누적 계산
                        sumup+=ptn
                        #a=a+'1'
                    else:
                        sumdown+=ptn
                        #b=b+'0'
                    if (j== 16-len(JMdata)) : #입력된 패턴 바로 다음 위치의 상승/하락 위치를 계산
                         if((val&1)==1):
                             nxtup+=ptn
                         else:
                             nxtdown+=ptn
                    val = val >> 1
        #print endk-srtk
        LUPct = int(sumup*1.0/(sumup+sumdown)*100)
        LDPct = int(sumdown*1.0/(sumup+sumdown)*100)
        SUPct = int(float(nxtup)/(nxtup+nxtdown)*100)
        SDPct = int(float(nxtdown)/(nxtup+nxtdown)*100)
        #line = code +' '+ JMD[code] + '= SU:' + str(SUPct)+'% '+ 'SD:' + str(SDPct)+'% '+ 'LU:' + str(LUPct)+'% '+ 'LD:' + str(LDPct)+'% \n'
        line = "%s  %d   %d   %d   %d   %s\n" % ( code, SUPct, SDPct, LUPct, LDPct, JMD[code] )
        print unicode(line),
        f.write(unicode(line))
        #f.write (line.encode('utf-8'))
f.close()

