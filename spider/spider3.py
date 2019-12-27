import requests
from bs4 import BeautifulSoup
import pymongo
import re

class diseaseSpider3:

    def __init__(self):
        self.conn = pymongo.MongoClient('Localhost',27017)
        self.db = self.conn['medical']
        self.col = self.db['data6']


    def get_html(self,url):
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.97 Safari/537.36'}
        html = requests.get(url,headers = headers)
        return html


    def get_allurl(self):
        print('begin url')
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.97 Safari/537.36'}
        pages = []
        count = 0
        names = []
        for index in range(1, 217):
            all_url = 'https://www.wiki8.com/search?q=%E8%80%81%E5%B9%B4%E7%97%85&Page=' + str(index)
            html = requests.get(all_url, headers=headers)
            Soup = BeautifulSoup(html.text, 'lxml')
            for nums in range(1, 31):
                for disease in Soup.select('#content > ul.sResult > li:nth-child('+str(nums)+' )> a'):
                    pages.append(disease['href'])
                    names.append(disease.get_text())
                    count+=1
        print(pages)
        print(names)
        print(count)
        return pages
    #
    # def getPageUrl(self,url):
    #     html = self.get_html(url)
        # headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.97 Safari/537.36'}
        # html = requests.get('https://www.wiki8.com/laoniandaixiexingjianzhongdu_161885/',headers = headers)
        # Soup = BeautifulSoup(html.text,'lxml')
        # ul = Soup.find('div',"TableOfContents").find('ul').findAll('a')
        # names = []
        # hrefs = []
        # for u in ul:
        #     print(u)
        #     names.append(u.get_text())
        #     hrefs.append(u['href'])
        # urls = {}
        # for i in range(0,names.__len__()):
        #     urls[names[i]] = hrefs[i]
        # # return urls
        # print(urls)

    def spider_main(self):
        print('begin')
        all_url = self.get_allurl()
        for u in all_url:
            try:
                data = self.data_spider(u)
                self.col.insert(data)
            except Exception as e:
                print(e, u)
        return


    def data_spider(self,url):
        # headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.97 Safari/537.36'}
        # html = requests.get('https://www.wiki8.com/laoniandaixiexingjianzhongdu_161885/',headers = headers)
        html = self.get_html(url)
        soup = BeautifulSoup(html.text,'lxml')
        names = []
        for n in soup.find('div',id="content").findAll('h2'):
            names.append(n.get_text())
        names.remove('目录')
        print(names)

        data = {}
        i=1
        content = soup.find('div',id="content").get_text().split('目录')[1]
        content1 = content.split(str(names[0]))[2].replace('\n','')
        data[names[0]] = content1.split(str(names[1]))[0]
        newcontent = str(names[0]).join(content1.split(str(names[1]))[1:])
        while i<(names.__len__()-1):

            if(names[i] == '21 相关药品'):
                infobox = []
                infobox = newcontent.split(str(names[i + 1]))[0].replace(' ', '').split('、')
                data[names[i]] = infobox

            elif (names[i] == '22 相关检查'):
                infobox = []
                infobox = newcontent.split(str(names[i + 1]))[0].replace(' ', '').split('、')
                data[names[i]] = infobox

            else:
                data[names[i]] = newcontent.split(str(names[i + 1]))[0].replace(' ', '')
            newcontent = str(names[i]).join(newcontent.split(str(names[i + 1]))[1:])
            i += 1

        # data.pop('相关文献')
        # data.pop('1 拼音')
        # data.pop('ICD号')
        print(data)
        print(names)
        print(newcontent)
        return data

a = diseaseSpider3()
a.spider_main()

