import requests
from bs4 import BeautifulSoup
import pymongo


class DiseaseSpider2:

    def __init__(self):
        self.conn = pymongo.MongoClient('Localhost',27017)
        self.db = self.conn['medical']
        self.col = self.db['manxingbing3']

    def get_html(self,url):
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.97 Safari/537.36'}
        html = requests.get(url,headers = headers)
        return html

    # 获取所有的疾病信息路径
    def get_allurl(self):
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.97 Safari/537.36'}
        pages = []
        names = []
        for index in range(1, 158):
            all_url = 'http://jbk.39.net/zq/manxingbing/zl?c1=73&p=' + str(index)
            html = requests.get(all_url, headers=headers)
            Soup2 = BeautifulSoup(html.text, 'lxml')
            for nums in range(2, 12):
                for disease in Soup2.select('body > div.chronic.wrap > div.content.clearfix > div.fl730.mr20 > div:nth-child('+str(nums)+') > div > div.drug-info-name > a'):
                    pages.append(disease['href'])
                    names.append(disease.get_text())

        print(pages)
        print(names)
        return pages


    def spider_main(self):
        print('begin')
        urls = self.get_allurl()
        rest_url = []
        print('spider')
        drugs = []
        examinations = []
        for url in urls:
            u = url.split('blby/')[0]
            try:
                basic_url = u + 'jbzs/'
                cause_url = u + 'blby/'
                symptom_url = u + 'zztz/'
                drug_url = u + 'cyyp/'
                examination_url = u + 'jcjb/'
                prevent_url = u + 'yfhl/'
                treat_url = u + 'yyzl/'
                complication_url = u + 'bfbz/'
                diet_url = u + 'ysbj/'
                data = {}
                # data['url'] = basic_url
                # data['basic_info'] = self.basicinfo_spide(basic_url)
                # data['cause'] = self.cause_spider(cause_url)
                data['drugs'] = self.drug_spider(drug_url)
                # data['symptom'] = self.symptom_spider(symptom_url)
                data['examination'] = self.examination_spider(examination_url)
                # data['prevent'] = self.prevent_spider(prevent_url)
                # data['treat'] = self.treat_spider(treat_url)
                # data['complication'] = self.complication_spider(complication_url)
                # data['diet'] = self.diet_spider(diet_url)
                for drug in self.drug_spider(complication_url):
                    drugs.append(drug)
                for examine in self.examination_spider(examination_url):
                    examinations.append(examine)
                # print(basic_url)
                # self.col.insert(data)

            except Exception as e:
                rest_url.append(u)
                print(e,u)
                # print(rest_url)
        path = "F:\\"
        examinations_path = path + 'examinations.txt'
        drug_path = path + 'drugs.txt'
        file1 = open(examinations_path, 'w')
        file2 = open(drug_path, 'w')
        for d in drugs :
            file1.write(d+'\n')
        for e in examinations:
            file2.write(e+'\n')
        return


    def basicinfo_spide(self,url):
        html = self.get_html(url)
        Soup = BeautifulSoup(html.text,'lxml')
        basic_data = {}
        for n in Soup.select('body > div.container > div.list_left > div:nth-child(1) > p.disease_title'):
            name = n.get_text()
        for p in Soup.select('body > div.container > div.list_left > div:nth-child(2) > ul > li:nth-child(3) > span:nth-child(2)'):
            position = p.get_text()
        # for d in Soup.select('body > div.container > div.list_left > div:nth-child(3) > ul > li:nth-child(7) > span:nth-child(2)'):
        #     drug = d.get_text().replace('[详细]', '').split('\n')[1:-2]
        for d in Soup.select('body > div.container > div.list_left > div:nth-child(1) > p.introduction'):
           definition = d.get_text()
        # for s in Soup.select('body > div.container > div.list_left > div:nth-child(2)'):
        #     symptom = n.get_text().split('相关症状：')[1].split('并发疾病：')[0].replace('[详细]', '').split('\n')[1:-1]
        basic_data['name'] = name
        basic_data['position'] = position
        # basic_data['drug'] = drug
        basic_data['definition'] = definition
        # basic_data['symptom'] = symptom
        # print(url)
        return basic_data

    # 病因
    def cause_spider(self, url):
        html = self.get_html(url)
        Soup = BeautifulSoup(html.text, 'lxml')
        cause = ''
        for c in Soup.select('body > div.container > div.list_left > div:nth-child(1) > div.article_box > div'):
            cause = c.get_text()
# print(cause)
#         print(url)
        return cause

    def drug_spider(self,url):
        html = self.get_html(url)
        Soup = BeautifulSoup(html.text,'lxml')
        drugs = []
        try:
            for n in Soup.find('div', 'chi-drug').find('ul', 'drug-list').find_all('h4'):
                drugs.append(n.get_text().replace('\n', ''))
        except Exception as e:
            return drugs
        drugs = list(set(drugs))
        # for num in range(1,15):
        #     for d in Soup.select('body > div.container > div > div.fl730.mr20 > div > ul > li:nth-child(' +str(num)+') > h4 > a'):
        #         name = d.get_text()
        #     for f in Soup.select('body > div.container > div > div.fl730.mr20 > div > ul > li:nth-child(' +str(num)+') > p > i'):
        #         factory = f.get_text()
        #     drug = name + ' ' + factory
        #     drugs.append(drugs)
        return drugs
    # 症状
#     def symptom_spider(self,url):
#         html = self.get_html(url)
#         Soup =BeautifulSoup(html.text,'lxml')
#         symptom = ''
#         for s in Soup.select('body > div.container > div.list_left > div:nth-child(1) > div.article_box > p:nth-child(3)'):
#             symptom = s.get_text()
#             # symptom = s.get_text().replace('\u3000\u3000 \xa0 一、症状\u3000\u3000', '').split('\u3000\u3000二、诊断\u3000\u3000')[0].replace('\u3000\u3000','').replace('\xa0','')
# #       for cs in Soup.select('body > div.container > div.list_left > div:nth-child(1) > div.article_box > p:nth-child(2)'):
# #           common_symptom = cs.get_text().replace('\n典型症状：\r\n','').replace('\r\n','')
# #       symptom['common_symptom'] = common_symptom
# #       symptom['specific_symptom'] = specific_symptom
# #         print(url)
#         return symptom

    # 检查
    def examination_spider(self,url):
# headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.97 Safari/537.36'}
# html = requests.get('http://jbk.39.net/xhdbb/jcjb/',headers = headers)
        html = self.get_html(url)
        examination = []
        Soup = BeautifulSoup(html.text,'lxml')
        for e in Soup.find('div','checkbox-data').find_all('a'):
            examination.append(e.get_text())
        print(examination)
        return examination
# print(examination)

    # 预防
    def prevent_spider(self,url):

        html = self.get_html(url)
        Soup = BeautifulSoup(html.text,'lxml')
        for p in Soup.select('body > div.container > div.list_left > div:nth-child(1) > div.article_box > div'):
            prevent = p.get_text()
        # print(url)
        return prevent

    # 治疗
    def treat_spider(self,url):

        html = self.get_html(url)
        Soup = BeautifulSoup(html.text,'lxml')
        for p in Soup.select('body > div.container > div.list_left > div:nth-child(1) > div.article_box > div'):
            prevent = p.get_text()
        # print(url)
        return prevent

    # 并发症
    def  complication_spider(self, url):
        html = self.get_html(url)
        Soup = BeautifulSoup(html.text, 'lxml')
        for c in Soup.select('body > div.container > div.list_left > div:nth-child(1) > div.article_box > div'):
            complication = c.get_text().replace('\n',' ')
        # print(url)
        return complication

    # 饮食
    def diet_spider(self,url):
        html = self.get_html(url)
        Soup = BeautifulSoup(html.text,'lxml')
        for d in Soup.select('body > div.container > div.list_left > div:nth-child(1) > div.article_box > div.article_paragraph'):
            diet = d.get_text()
# print(diet)
#         print(url)
        return diet

a = DiseaseSpider2()
a.spider_main()

