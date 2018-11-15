#!/usr/bin/python
# -*- coding: utf-8 -*-
# Author: mr tang
# Date:   2018-11-14 08:31:24
# Contact: mrtang@nudt.edu.cn 
# Github: trzp
# Last Modified by:   mr tang
# Last Modified time: 2018-11-14 11:02:07


def demo():
    ep = EasyPaper('savedrecs.bib','d:\\s')
    ep.main(1)
    ep.rename_files()
    print '>>>> do not close this process until all files downloaded >>>'
    print u'确认浏览器完成所有下载后，任意键将文件重命名并结束'
    getch()

if __name__ == '__main__':
    demo()