# -*- coding:utf-8 -*-
import requests
from bs4 import BeautifulSoup
import re




def findPinyin (zi):
    #url = "https://hanyu.baidu.com/s?wd=" + zi +"&from=zici"

    heads = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36 Edg/124.0.0.0'}

    response = requests.get(url, headers=heads)

    resp = response.text
    #print("resp.text++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
    #print(resp)
    soup = BeautifulSoup(resp,"html.parser")
    print(soup.p)

    '''
    <div class="pronounce" id="pinyin">
    <span><b>liǎng</b>

    '''
    # prt =  re.compile(r'pinyin\*><span><b>')
    prt = re.compile(r'pinyin')

    #print(response.text)
    matchs = re.search(prt, resp)
    #print(matchs)
    strat1 = matchs.start()
    #print(strat1)

    pinyin = resp[strat1:strat1+200]
    #print(pinyin)
    str1 = pinyin.split("<b>")[1]
    #print(str1)
    str2 = str1.split("</b>")
    print(zi,str2[0])


    #return



shengpizi = "洑"

for z in shengpizi:
    #print(z)
    findPinyin(z)