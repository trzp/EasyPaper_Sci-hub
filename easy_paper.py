#!/usr/bin/python
# -*- coding: utf-8 -*-
# Author: mr tang
# Date:   2018-11-14 08:31:24
# Contact: mrtang@nudt.edu.cn 
# Github: trzp
# Last Modified by:   mr tang
# Last Modified time: 2018-11-14 11:02:07

import bibtexparser
import os
import re
import time
from selenium import webdriver
from bs4 import BeautifulSoup
import re
from msvcrt import getch
import json

class EasyPaper:
    '''a script for easy downloading papers
       author: mrtang
       contact: mrtang@nudt.edu.cn'''

    def  __init__(self,src_file,dst_fold):
        '''
        src_file: bib file contains information about papers
        dst_fold: fold for saving downloaded files
        timeout: the maximun time period for downloading one paper, once the time 
        exceeded, the current downloading will be discarded
        '''
        if not os.path.exists(src_file): raise BaseException,'src_file is not exists!'
        if src_file[-3:].lower()!= 'bib':  raise TypeError,'only bib file supported!'

        if not os.path.exists(dst_fold):    os.makedirs(dst_fold)
        self.dst_fold = dst_fold
        self.src_file = src_file
        
        options = webdriver.ChromeOptions()
        prefs = {'profile.default_content_settings.popups':0, 'download.default_directory': '%s'%self.dst_fold}
        options.add_experimental_option('prefs', prefs)
        self.driver = webdriver.Chrome(chrome_options=options)
        
        self.paper_dict = {}
        
        print '>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>'
        print '>>>> a tool for easily downloading papers >>>>'
        print '>>>>         engine started               >>>>'
        print '>>>>           by mrtang                  >>>>'
        print '>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>'

    def read_bib_file(self):
        with open(self.src_file) as f:
            tem = f.read()
        content = bibtexparser.loads(tem).entries

        self.paper_dict = {}
        for p in content:       #使用doi构造url在浏览器中打开
            if p.has_key('doi'):
                doi = p['doi']
                while doi.startswith('{'):  #web of science直接生成的doi前面多了一层‘{}’
                    doi = doi[1:]
                while doi.endswith('}'):
                    doi = doi[:-1]

                url = "https://www.sci-hub.tw/%s"%doi
                title = self._valid_name(p['title'])
                fname = self._file_name_by_doi(doi)
                self.paper_dict[fname] = {'url':url,'title':title}
        
        jsObj = json.dumps(self.paper_dict)
        with open(self.dst_fold + r'/' + 'log.json','w') as f:
            f.write(jsObj)

    def check_files(self):
        files = []
        self.pdfs = []
        filelist = os.listdir(self.dst_fold)
        for file in filelist:
            filename  = file.split('.pdf')[0]
            # filename = os.path.splitext(file)[0]
            olddir = os.path.join(self.dst_fold,file)
            if os.path.isdir(olddir):
                continue
            self.pdfs.append(filename)
            files.append(file)
        return files

    def _valid_name(self,title):   #构造符合命名规则的文件名
        rstr = r'\n'
        title = re.sub(rstr,'',title)
        rstr = r'\t'
        title = re.sub(rstr,'',title)
        rstr = r"[\/\\\:\*\?\"\<\>\|{}]"  #其他非法字符: / \ : * ? " < > | { }
        return re.sub(rstr,'', title)

    def _file_name_by_doi(self,doi):    #sci-hub下载的文件大部分是以doi命名的(将/\替换成了@)
        rstr = r'\\'
        doi = re.sub(rstr,'@',doi)
        rstr = r'//'
        doi = re.sub(rstr,'@',doi)
        rstr = r'\/'
        return re.sub(rstr,'@',doi)

    def fetch(self):
        self.read_bib_file()
        self.check_files()
        count = 0
        for key in self.paper_dict:
            if key in self.pdfs:   continue
            newtab = 'window.open("%s")'%self.paper_dict[key]['url']
            self.driver.execute_script(newtab)
            print '>> url: %s'%self.paper_dict[key]['url']
            time.sleep(1.5)
            count += 1
        return count

    def _download(self):
        title = re.compile(r'Sci-Hub')
        page  = self.driver.page_source
        soup = BeautifulSoup(page, 'lxml')

        try:
            r = title.findall(str(soup.head.find('title'))) #匹配scihub网址
            if len(r)==0:
                return
        except:
            return
            
        #什么原理使得soup和driver都无法捕获captcha呢
        # self.driver.find_element_by_xpath('//*[@id="captcha"]')

        #找到sava元素并点击下载
        self.driver.find_element_by_xpath('/html/body/div[1]/div[1]/ul/li[2]/a').click()
        time.sleep(2)
        self.driver.close() #关闭当前页

    def download(self,n,wait = True):
        if wait:
            time.sleep(n)
        print '>> download papers'
        handles = self.driver.window_handles
        for handle in handles:
            self.driver.switch_to.window(handle)
            self._download()
            time.sleep(0.5)

    def main(self,n = 2):
        '''
        Once a web request need verification, the download will be failure.
        The program will try again to download these papers.
        In many cases, by again making a request can get access to the paper.
        Howerver, since we build new connection based on the comparation of
        pdf filename and the DOI. The cases that the file does not named by
        the DOI code means these files would always be connected in each 
        request. Therefore, we suggested that you should manully deleted the
        items in the bib file that has been downloaded.
        
        In the future, we would fix this issue, that keeps the requests that
        need a verfication to you to manually do the verfication.
        
        The main difficulty is that I don't know how to confirm a web page
        contains a captcha, I just cann't get the captcha element by selenium
        and beautifulsoup, why? If you have the ansower, please contact me via
        mrtang@nudt.edu.cn
        '''
        for i in xrange(n):
            count = self.fetch()
            self.download(count)
            handles = self.driver.window_handles
            self.driver.switch_to.window(handles[-1])   #reget handle
            time.sleep(5)

    def rename_files(self):
        files = self.check_files()
        with open(self.dst_fold + '\\' + 'log.json','r') as f:
            paper_dict = json.loads(f.read())

        for file in files:
            if file[-4:] != '.pdf': continue
            filename = file[:-4]
            if not paper_dict.has_key(filename): continue
            newname = paper_dict[filename]['title']
            newdir = os.path.join(self.dst_fold,newname + '.pdf')
            olddir = os.path.join(self.dst_fold,file)

            print '>>> old name: %s'%file
            print '>>> new name: %s'%newname
            
            print newdir
            print olddir
            os.rename(olddir,newdir)
            time.sleep(0.5)









