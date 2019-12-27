import requests
from bs4 import BeautifulSoup

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.97 Safari/537.36'}
html = requests.get('http://jbk.39.net/tnb/jbzs/',headers = headers)

Soup = BeautifulSoup(html.text,'lxml')
drugs = []
x = Soup.select('body > div.container > div.list_left > div:nth-child(2)')
for n in Soup.select('body > div.container > div.list_left > div:nth-child(2)'):
    drugs = n.get_text().split('相关症状：')[1].split('并发疾病：')[0].replace('[详细]', '').split('\n')[1:-1]
# for num in range(1,15):
    # for d in Soup.select('body > div.container > div > div.fl730.mr20 > div > ul > li:nth-child(' +str(num)+') > h4 > a'):
    #     name = d.get_text()
    # for f in Soup.select('body > div.container > div > div.fl730.mr20 > div > ul > li:nth-child(' +str(num)+') > p > i'):
    #     factory = f.get_text()
    # drug = name + ' ' + factory
    # drugs.append(drug)
print(drugs)

