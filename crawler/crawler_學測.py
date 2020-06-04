from selenium import webdriver
import time
from lxml import etree
import requests
import pandas as pd
from django import *

Link = list()
Link.append("https://university-tw.ldkrsi.men/caac/#gsc.tab=0")
url = Link[0]
browser = webdriver.Chrome('./chromedriver')
browser.get(url)
cookies = browser.get_cookies()
session = requests.Session()
headers = {'User-Agent': 'Mozilla/5.0 (Macintosh Intel Mac OS X 10_13_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.181 Safari/537.36'}
for cookie in cookies:
    session.cookies.set(cookie['name'], cookie['value'])
res = session.get(url, headers=headers)
html = etree.HTML(res.text)
browser.quit()
uni_link = html.xpath('//div[@class="container"]//ul[@class="flexbox schools"]//li/a/@href')
UniversityLink = list()
for i in uni_link:
    UniversityLink.append('https://university-tw.ldkrsi.men/caac/'+i+'/#gsc.tab=0')

CODE = list()
NUMBER = list()
STANDER = list()
for i in range(5):
    s_list = list()
    STANDER.append(s_list)

MULTIPLE = list()
for i in range(5):
    s_list = list()
    MULTIPLE.append(s_list)

#University_list = html.xpath("")
for k in range(len(UniversityLink)):
    browser = webdriver.Chrome('./chromedriver')
    url = UniversityLink[k]
    browser.get(url)
    cookies = browser.get_cookies()
    session = requests.Session()
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh Intel Mac OS X 10_13_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.181 Safari/537.36'}
    for cookie in cookies:
        session.cookies.set(cookie['name'], cookie['value'])
    res = session.get(url, headers=headers)
    html = etree.HTML(res.text)
    browser.quit()

    standard = list()
    multiple = list()

    code = html.xpath('//div[@class="container-big"]//table[@class="depsTable"]//tbody//tr//td[1]//a/text()')
    for i in code:
        CODE.append(i)
    #tiltle = html.xpath('//div[@class="container-big"]//table[@class="depsTable"]//tbody//tr//td[2]//a/text()')
    memNum = html.xpath('//div[@class="container-big"]//table[@class="depsTable"]//tbody//tr//td[3]/text()')
    for i in memNum:
        NUMBER.append(i)

    for i in range(5):
        j = i+4
        standard.append(html.xpath('//div[@class="container-big"]//table[@class="depsTable"]//tbody//tr//td['+str(j)+']/text()'))

    for subject in range(len(standard)):
        for s in standard[subject]:
            STANDER[subject].append(s)

    for i in range(5):
        j = i+10
        multiple.append(html.xpath('//div[@class="container-big"]//table[@class="depsTable"]//tbody//tr//td['+str(j)+']/text()'))

    for subject in range(len(multiple)):
        for s in multiple[subject]:
            MULTIPLE[subject].append(s)


df = pd.DataFrame({"Code": CODE, "num": NUMBER, "s_Chinese": STANDER[0], "s_English": STANDER[1], "s_Math":STANDER[2],
                   "s_Society":STANDER[3], "s_Science":STANDER[4],"m_Chinese": MULTIPLE[0], "m_English": MULTIPLE[1], "m_Math":MULTIPLE[2],
                   "m_Society":MULTIPLE[3], "m_Science":MULTIPLE[4]})

print(len(CODE))
print(len(NUMBER))
print(len(STANDER[0]))
print(len(MULTIPLE[0]))

df.to_csv('./學測_.csv')