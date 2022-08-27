#!/usr/bin/env python3
#-*- coding: utf-8 -*-
__author__ = 'cqhac@qq.com'

from bs4 import BeautifulSoup
import urllib.request, urllib.error
import re
import xlwt
import sqlite3

class Main(object):
    head = {"User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.71 Safari/537.36"}
    charset = 'utf-8'

    FindLink = re.compile(r'<a href="(.*?)">')
    FindTitle = re.compile(r'<span class="title">(.*)</span>')
    FindRate = re.compile(r'<span class="rating_num" property="v:average">(.*)</span>')
    FindJudgeNum = re.compile(r'<span>(\d*)人评价</span>')
    FindInq = re.compile(r'<span class="inq">(.*)</span>')
    FindAbout = re.compile(r'<p class="">(.*?)</p>', re.S)

    def __init__(self, url):
        self.url = url
        self.res = self.Get()
        self.InitDatabase()
        self.Save2Database(self.res)

    def Get(self):
        tot = []
        for i in range(0, 10):
            url = self.url + str(i * 25)
            html = self.GetHtml(url)
            soup = BeautifulSoup(html, 'html.parser')
            for item in soup.find_all('div', class_ = 'item'):
                #print(item)
                data = []
                item = str(item)
                link = re.findall(self.FindLink, item)[0]
                data.append(link)
                title = re.findall(self.FindTitle, item)
                if(len(title) == 2):
                    cn_title = title[0]
                    data.append(cn_title)
                    en_title = title[1].replace("/", "")
                    data.append(en_title)
                else:
                    data.append(title[0])
                    data.append(' ')
                rate = re.findall(self.FindRate, item)[0]
                data.append(rate)
                judgenum = re.findall(self.FindJudgeNum, item)[0]
                data.append(judgenum)
                inq = re.findall(self.FindInq, item)
                if len(inq) != 0:
                    inq = inq[0].replace("。", "")
                    data.append(inq)
                else:
                    data.append(" ")
                about = re.findall(self.FindAbout, item)[0]
                about = re.sub('<br(\s+)?/>(\s+)?', " ", about)
                about = re.sub('/', " ", about)
                data.append(about.strip())
                tot.append(data)
        return tot

    def GetHtml(self, url):
        request = urllib.request.Request(url, headers = self.head)
        html = ''
        try:
            response = urllib.request.urlopen(request)
            html = response.read().decode(self.charset)
        except urllib.error.URLError as e:
            if hasattr(e, "code"):
                print(e.code)
            if hasattr(e, "reason"):
                print(e.reason)
        return html
    
#    def Save(self, data):
#        wb = xlwt.Workbook(encoding = self.charset, style_compression = 0)
#        sheet = wb.add_sheet('豆瓣TOP250', cell_overwrite_ok = True)
#        col = ("电影详情链接", "影片中文名", "影片外国名", "评分", "评价数", "概况", "相关信息")
#        for i in range(0, 7):
#            sheet.write(0, i, col[i])
#        for i in range(0,250):
#            res = data[i]
#            for j in range(0, 7):
#                sheet.write(i + 1, j, res[j])
#        wb.save('豆瓣TOP250.xls')

    def InitDatabase(self):
        init_sql =  '''
            CREATE TABLE doubanTOP250
            (id integer primary key autoincrement,
            info_link text,
            cn_name varchar,
            en_name varchar,
            score numeric,
            rate numeric,
            instroduction text,
            info text)
        '''
        conn = sqlite3.connect('豆瓣TOP250.db')
        cur = conn.cursor()
        cur.execute(init_sql)
        conn.commit()
        conn.close()

    def Save2Database(self, data):
        conn = sqlite3.connect('豆瓣TOP250.db')
        cur = conn.cursor()
        for res in data:
            for index in range(len(res)):
                if index == 3 or index == 4:
                    continue
                res[index] = '"' + res[index] + '"'
            sql = '''
                    insert into doubanTOP250 (
                    info_link, cn_name,en_name,score,rate,instroduction,info) 
                    values(%s)'''%",".join(res)
            #print(sql)
            cur.execute(sql)
            conn.commit()
        cur.close()
        conn.close()

if __name__ == "__main__":
    run = Main('https://movie.douban.com/top250?start=')
    print("Finished!")
