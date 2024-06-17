# -*- coding:utf-8 -*-
import requests
from bs4 import BeautifulSoup
import re




def findsth ():
    url = "https://mobile.anjuke.com/xf/xin/"

    heads = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36 Edg/124.0.0.0'}

    response = requests.get(url, headers=heads)

    resp = response.text

    print(resp)
    soup = BeautifulSoup(resp,"html.parser")






findsth()