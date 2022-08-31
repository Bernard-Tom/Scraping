"""
WORDS TRADUCTION SCRAPING : ANGLAIS-FRANCAIS

url : https://fichesvocabulaire.com/listes-vocabulaire-anglais-pdf

dataset caracteristics :
    size : 454 Ko
    errors during scraping process: 8 ; beacause of ','
    nb words : 65194
    nb files / theme / url : 104

Created by Tom BERNARD 2022
"""

import requests
from bs4 import BeautifulSoup
import csv
import unicodedata
import re

class FirstFrame:
    def __init__(self,url,parser):
        self.total_word_cnt = 0
        self.err_cnt = 0
        self.url = url
        self.response = requests.get(url)
        if self.response.ok:
            self.parser = parser
            self.soup = BeautifulSoup(self.response.text,parser)
        else : 
            print(f'ERR : {self.url} not found')

    def run(self):
        ol = self.soup.find('ol')
        lis = ol.findAll('li')
        #i = 0

        for li in lis:
            #i += 1
            #if i > 5 : break
            a = li.find('a')
            strong = li.find('strong')
            if a != None:
                link = a['href']
                theme = self.normalize_string(strong.text)
                newFrame = SecondFrame(link,'html.parser',theme)
                newFrame.create_file()
                newFrame.extract_data()
                self.total_word_cnt += newFrame.word_cnt
                self.err_cnt += newFrame.err_cnt
                print(f'Data extracting from {newFrame.url} Sucssed , total words saved:{self.total_word_cnt} ; link processed:{SecondFrame.link_cnt}\n\r')
        print(f'END : Total err : {self.err_cnt}')

    def normalize_string(self,string:str):
        string = ''.join((c for c in unicodedata.normalize('NFD', string) if unicodedata.category(c) != 'Mn'))
        string = re.sub('\W+','_', string)
        while string.endswith('_'):
            string = string[:-1]
        return(string)

class SecondFrame(FirstFrame):
    link_cnt = 0
    def __init__(self, url, parser,theme):
        super().__init__(url, parser)
        SecondFrame.link_cnt += 1
        self.theme = theme
        self.word_cnt = 0

    def create_file(self):
        self.filename = str(self.theme + '.csv')
        csvfile = open(f'./data/{self.filename}','w',newline='')
        self.csvwriter = csv.writer(csvfile, delimiter=';', quoting=csv.QUOTE_MINIMAL)
        
    def extract_data(self):
        table = self.soup.find('table')
        trs = table.find_all('tr')
        for tr in trs:
            row = []
            tds = tr.find_all('td')
            for td in tds:
                row.append(self.remove_space(td.text))
            try :
                self.csvwriter.writerow(row)
                self.word_cnt += 2
            except : 
                print("Err")
                self.err_cnt += 1
    def remove_space(self,word:str):
        while word.endswith(' '):
            word = word[:-1]
        return(word) 

parser = 'html.parser'
firstFrame = FirstFrame('https://fichesvocabulaire.com/listes-vocabulaire-anglais-pdf',parser)
firstFrame.run()