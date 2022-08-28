# author: NatsumeHikaru
# email: cqhac@qq.com
# use it to get phonetic symbol from oxford dictionary.put it to anki
# mode 0: just input and then output
# mode 1: input the word and output the word and the phonetic symbol
# mode 2: exit

#!/usr/bin/env python3
#-*- coding: utf-8 -*-

from bs4 import BeautifulSoup
import urllib.request, urllib.error
import re
import os
import sys

phon = ''

class Work(object):
    head = {"User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.71 Safari/537.36"}
    charset = 'utf-8'

    Find = re.compile(r'<span class="phon">/(.*?)/</span>')

    def __init__(self, url):
        self.url = url
        self.res = self.Get()
    
    def callback(self):
        return self.res

    def Get(self):
        url = self.url
        html = self.Gethtml(url) 

        soup = BeautifulSoup(html, 'html.parser')
        item = soup.find_all('span', class_ = 'phon')
        res = re.findall(self.Find, str(item[0]))
        #with open("test.txt", mode="w", encoding="utf-8") as f:
            #f.write(str(res))

        res=str(res).replace("['","")
        res = res.replace("']","")
        res='['+res+']'
        return res;

    def Gethtml(self, url):
        url = self.url
        request = urllib.request.Request(url, headers = self.head)
        html = ''
        try:
            response = urllib.request.urlopen(request)
            html = response.read().decode('utf-8')
        except urllib.error.URLError as e:
            if hasattr(e, "code"):
                print(e.code)
            if hasattr(e, "reason"):
                print(e.reason)

        return html

if __name__ == '__main__':
    #run = Work("https://www.oxfordlearnersdictionaries.com/definition/english/english")
    #print(run.callback())
    with open('test.txt', 'a', encoding="utf-8") as f:
        while(True):
            mode = int(input())
            if mode == 0:
                string = str(input())
                meaning = str(input())
                f.write(string+"\t"+meaning+"\n")
                print('写入成功')
            elif mode == 1:
                word = str(input())
                run = Work("https://www.oxfordlearnersdictionaries.com/definition/english/"+word)
                res = run.callback()
                print(res)
                meaning = str(input())
                w = word+"<br>"+res+"\t"+meaning
                print(w)
                print("是否写入(1是,0否)")
                s = int(input())
                if s == 1:
                    f.write(word+"<br>"+res+"\t"+meaning+"\n")
                    print('写入成功')
                else:
                    continue
            elif mode == 2:
                print('退出')
                exit()

