import requests
from bs4 import BeautifulSoup
import re

txt = "10359.txt"

class Kehu:
    def __init__(self,a0,a1,a2,a3,a4,a5,a6,a7,a8,a9,a10,a11,a12,a13):
        self.a0 = a0
        self.a1 = a1
        self.a2 = a2
        self.a3 = a3
        self.a4 = a4
        self.a5 = a5
        self.a6 = a6
        self.a7 = a7
        self.a8 = a8
        self.a9 = a9
        self.a10 = a10
        self.a11 = a11
        self.a12 = a12
        self.a13 = a13
    def showdetals(self):
        print(self.a0,self.a1,self.a2,self.a3,self.a4,self.a5,self.a6,self.a7,self.a8,self.a9,self.a10,self.a11,self.a12,self.a13)




Readdata = open (txt,encoding = 'utf-8')
data_all = Readdata.read()
#print(data_all)

list301 = []

data_m = data_all.split("span")
for d in data_m:
    #print(d)
    if "301103" in d :
        if len(d) > 10:
            list301.append(d)
    if "62305" in d :
        if len(d) > 10:
            list301.append(d)

#print(list301)

soup = BeautifulSoup(data_all,"html.parser")
trlist = soup.findAll("tr")
for tr in trlist:
    tdlist = tr.findAll("td")
    #print("+++++++++++++++++++++++++++++++++++++++++++")
    kh = []
    for td in tdlist:
        spanlist = td.findAll("span")
        #print("======================================")
        #print(spanlist)
        if len(spanlist) >0:
            shuxing = spanlist[0].string
            #print(shuxing)
            kh.append(shuxing)
    kehu1 = Kehu (kh[0],kh[1],kh[2],kh[3],kh[4],kh[5],kh[6],kh[7],kh[8],kh[9],kh[10],kh[11],kh[12],kh[13])
    kehu1.showdetals()


