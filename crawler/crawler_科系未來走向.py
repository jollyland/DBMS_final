from selenium import webdriver
import time
from lxml import etree
import requests
import pandas as pd
from django import *
Link = ['https://www.104.com.tw/jb/career/department/navigation']
url = Link[0]
browser = webdriver.Chrome('./chromedriver')
browser.get(url)
cookies = browser.get_cookies()
session = requests.Session()
headers = {'User-Agent': 'Mozilla/5.0 (Macintosh Intel Mac OS X 10_13_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.181 Safari/537.36'}
for cookie in cookies:
     session.cookies.set(cookie['name'], cookie['value'])
res = session.get(url, headers=headers)
res.encoding = res.apparent_encoding

html = etree.HTML(res.text)
browser.quit()

# ----- [University] ---------
uni_name = html.xpath('//div[@class="container"]//div[@class="navigation p1"]/div[2]//a[contains(text(),"大學") and not(contains(text(),"科技"))]/text()')
uni_link = html.xpath('//div[@class="container"]//div[@class="navigation p1"]/div[2]//a[contains(text(),"大學") and not(contains(text(),"科技"))]/@href')
print(uni_name)
print(uni_link)
UNIVERSITY = list()
DEPARTMENT = list()
RATIO = list()
CAR1 = list()
CAR2 = list()
CAR3 = list()
for i in range(70,73):
    link = 'https://www.104.com.tw'
    link += uni_link[i]
    browser = webdriver.Chrome('./chromedriver')
    url = link
    browser.get(url)
    res = session.get(url, headers=headers)
    res.encoding = res.apparent_encoding
    html = etree.HTML(res.text)
    browser.quit()
    #------- major -----------
    dep = html.xpath('//body[@class="department"]//div[@class="container"]//a[@class="a2"]/text()')
    major = html.xpath('//body[@class="department"]//div[@class="container"]//a[@class="a2"]/@href')
    for j in range(len(dep)):
        UNIVERSITY.append(uni_name[i])
        DEPARTMENT.append(dep[j])
        link = 'https://www.104.com.tw'
        link += major[j]
        browser = webdriver.Chrome('./chromedriver')
        url = link
        browser.get(url)
        res = session.get(url, headers=headers)
        res.encoding = res.apparent_encoding
        html = etree.HTML(res.text)
        browser.quit()
        #----------ratio ----------
        ratio = html.xpath('//div[@class="wawa3"]/div[@class="cnt"]/text()')
        # print(ratio)
        if len(ratio)!=0:
            RATIO.append(ratio[0])
        else:
            RATIO.append("NULL")
        #----------career --------
        career1 = html.xpath('//div[@class="content"]//div[@class="yearContent"]//div[@class="wrap"]/div/dl[1]/dd[1]/a[@class="a2 left"]/text()')
        # print(career1[0])
        if len(career1)!=0:
            CAR1.append(career1[0])
        else:
            CAR1.append("NULL")
        career2 = html.xpath('//div[@class="content"]//div[@class="yearContent"]//div[@class="wrap"]/div/dl[1]/dd[2]/a[@class="a2 left"]/text()')
        #　print(career2[0])
        if len(career2) != 0:
            CAR2.append(career2[0])
        else:
            CAR2.append("NULL")
        career3 = html.xpath('//div[@class="content"]//div[@class="yearContent"]//div[@class="wrap"]/div/dl[1]/dd[3]/a[@class="a2 left"]/text()')
        # print(career3[0])
        if len(career3) != 0:
            CAR3.append(career3[0])
        else:
            CAR3.append("NULL")

    df = pd.DataFrame({"University":UNIVERSITY,"DEPARTMENT":DEPARTMENT,"CAR1":CAR1,"CAR2":CAR2,"CAR3":CAR3})
    df2 = pd.DataFrame({"University":UNIVERSITY,"DEPARTMENT":DEPARTMENT,"Ratio":RATIO})
    df.to_csv('./職業output 71-73.csv',index=False)
    df2.to_csv('./比率output 71-73.csv',index=False)
