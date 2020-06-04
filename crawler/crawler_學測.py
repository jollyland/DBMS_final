from selenium import webdriver
import time
from lxml import etree
import requests
import pandas as pd
Link = ['https://university-tw.ldkrsi.men/caac/006/#gsc.tab=0']
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
standard = list()
multiple = list()
# ----- [Title] ---------
code = html.xpath('//div[@class="container-big"]//table[@class="depsTable"]//tbody//tr//td[1]//a/text()')
#tiltle = html.xpath('//div[@class="container-big"]//table[@class="depsTable"]//tbody//tr//td[2]//a/text()')
memNum = html.xpath('//div[@class="container-big"]//table[@class="depsTable"]//tbody//tr//td[3]/text()')
for i in range(6):
    j = i+4
    standard.append(html.xpath('//div[@class="container-big"]//table[@class="depsTable"]//tbody//tr//td['+str(j)+']/text()'))
print(code)
#print(tiltle)
print(memNum)
for i in range(6):
    print(standard[i])

df = pd.DataFrame({"Code": code, "num": memNum, "Chinese": standard[0], "English": standard[1], "Math":standard[2],
                   "Society":standard[3], "Science":standard[4], "EnListen":standard[5]})

df.to_csv('./006.csv')
