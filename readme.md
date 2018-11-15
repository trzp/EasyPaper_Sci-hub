![EasyPaper-SCI-Hub](logo//logo.png)
## EasyPaper_SCI-Hub是什么?
是一个基于SCI-Hub的批量文献下载工具

## EasyPaper_SCI-Hub有什么特点？
只需要将从文献数据库生成的.bib类型的题录文件传递给它，它就可以帮你完成文献的批量下载

## 环境依赖
* chrome浏览器
* 和你的chrome浏览器版本匹配的[chromedriver](http://npm.taobao.org/mirrors/chromedriver/)
* 将下载的chromedriver.exe放置在某个目录如c:\program files\chromedriver，并将该目录添到加环境变量
* python2
* 依赖的python包有：[bibtexparser](https://github.com/sciunto-org/python-bibtexparser), selenium, bs4, json

## 使用方法
* 准备bib文件
    * 首先你需要准备好你要下载文献的相关信息，我们这里需要的是.bib文件，且每个题录提供有DOI号码 
    * 推荐使用web of science搜索确定题录并将其导出为bib文献格式，如果该选项不可用，您可以先尝试将其导出为endnote格式，导入endnote数据库之后通过endnote导出为bib亦可
    * 假设您准备的bib文件为d:\\mypaper\\paper.bib, 并且计划将下载的文献放置在d:\\mypaper中
* 运行脚本
    * 编辑脚本，如demo.py

    ```javascript
    #coding:utf-8
    
    from easy_paper import *
    from msvcrt import getch
    
    def demo():
        ep = EasyPaper('d:\mypaper\paper.bib','d:\mypaper')
        ep.main(1)
        ep.rename_files()
        print '>>>> do not close this process until all files downloaded >>>'
        print u'确认浏览器完成所有下载后，任意键将文件重命名并结束'
        getch()

    if __name__ == '__main__':
        demo()
      
    ```
    
    * 这个脚本运行后，将从提供的bib文件中读取相关信息并启动chrome浏览器搜索相关文献并下载，由于sci-hub有时需要输入验证码，因此在每次请求时对这类网页将直接丢弃，并重新尝试。ep.main(2)的参数就是指重连的次数。很多情况下重连能够解决验证码问题。
    * 每次重连都将根据已经下载的文献确定哪些需要重新下载，由于浏览器下载的文件名随机性很大，因此我不能保证对所有文件都有十足把握
    * 因此，不宜将重连次数设置过大，以免产生重复下载
    * 建议在下载完成后，手动在bib中删除已经下载的文献信息，再重试。
    
## 任何建议请联系
* mrtang@nudt.edu.cn