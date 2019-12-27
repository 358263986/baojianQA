import requests
from bs4 import BeautifulSoup
import pymongo

# headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.97 Safari/537.36'}
# html = requests.get('http://jbk.99.com.cn/dmyh/',headers = headers)
# Soup = BeautifulSoup(html.text,'lxml')
# print(Soup)


class DiseaseSpider:

    def __init__(self):
        self.conn = pymongo.MongoClient('Localhost',27017)
        self.db = self.conn['medical']
        self.col = self.db['data']

    def get_html(self,url):
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.97 Safari/537.36'}
        html = requests.get(url,headers = headers)
        return html

    # 获取所有的疾病信息路径
    def get_allurl(self):
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.97 Safari/537.36'}
        pages = []
        for index in range(1,12):
            all_url='https://jbk.99.com.cn/keshi/laonianke-'+str(index)+'.html'
            html = requests.get(all_url,headers=headers)
            Soup2 = BeautifulSoup(html.text,'lxml')
            # pages = Soup2.find('div','part-cont3').find_all('a')
            for nums in range(1,11):
                for disease in Soup2.select('#part > div.part-cont3 > dl:nth-child('+str(nums)+') > dd > h3 > a'):
                    pages.append(disease['href'])
        print(pages)
        return pages

    def spider_main(self):
        print('begin')
        urls = self.get_allurl()
        for u in urls:
            try:
                basic_url = 'https:' + u
                cause_url = 'https:' + u + 'bingyin.html'
                symptom_url = 'https:' + u + 'zhengzhuang.html'
                examination_url = 'https:' + u + 'jiancha.html'
                prevent_url = 'https:' + u + 'yufang.html'
                treat_url = 'https:' + u + 'zhiliao.html'
                complication_url = 'https:' + u + 'bingfazheng.html'
                data = {}
                data['url'] = basic_url
                data['basic_info'] = self.basicinfo_spider(basic_url)
                data['cause'] = self.cause_spider(cause_url)
                data['symptom'] = self.symptom_spider(symptom_url)
                data['examination'] = self.common_spider(examination_url)
                data['prevent'] = self.common_spider(prevent_url)
                data['treat'] = self.common_spider(treat_url)
                data['complication'] = self.common_spider(complication_url)
                print(basic_url)
                self.col.insert(data)

            except Exception as e:
                print(e,u)
        return


    # 1.基本信息（什么是XX）2.发病部位3.疾病用药
    def basicinfo_spider(self, url):
        html = self.get_html(url)
        Soup = BeautifulSoup(html.text,'lxml')
        basic_data = {}
        name = ''
        position = ''
        definition = ''
        drug = ''
        for k in Soup.select('#disease > h2'):
            name = k.get_text().replace('\r\n        ','')
        for p in Soup.select('#d-top > dl > dd > ul > li:nth-child(1) > a'):
            position = p.get_text()
        for d in Soup.select('#d-top > dl > dd > ul > li:nth-child(3) > span'):
            drug = d.get_text()
        for d in Soup.select('#d-js > div > dl > dd > p:nth-child(2)'):
            # d-js > div > dl > dd
            # d-js > div > dl > dd > p:nth-child(2)
            definition = d.get_text().replace('\u3000\u3000','')
        basic_data['name'] = name
        basic_data['position'] = position
        basic_data['drug'] = drug
        basic_data['definition'] = definition
        print(basic_data)
        return basic_data

    # 病因
    def cause_spider(self,url):
        html = self.get_html(url)
        Soup = BeautifulSoup(html.text,'lxml')
        cause = ''
        for c in Soup.select('#d-js > div.d-js-cont2'):
            cause = c.get_text()
        return cause

    # 症状
    def symptom_spider(self,url):
        html = self.get_html(url)
        Soup =BeautifulSoup(html.text,'lxml')
        symptom = ''
        for s in Soup.select('#Div1 > div > dl > dd'):
            symptom = s.get_text()
        return symptom

    # 检查
    # def examination_spider(self,url):
    #     html = self.get_html(url)
    #     Soup = BeautifulSoup(html.text,'lxml')
    #     for e in Soup.select('#d-js > div.d-js-cont2'):
    #         examination = e.get_text()
    #     return examination

    # # 预防
    # def prevent_spider(self,url):
    #     html = self.get_html(url)
    #     Soup = BeautifulSoup(html.text,'lxml')
    #     for p in Soup.select('#d-js > div.d-js-cont2'):
    #         prevent = p.get_text()
    #     return prevent

    # 检查，预防，治疗和并发症,只用换url就行
    def common_spider(self, url):
        html = self.get_html(url)
        Soup = BeautifulSoup(html.text, 'lxml')
        common = ''
        for c in Soup.select('#d-js > div.d-js-cont2'):
            common = c.get_text()
        return common

a=DiseaseSpider()
a.spider_main()



