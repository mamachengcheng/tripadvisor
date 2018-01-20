# **coding: utf-8**
import xlwt
import requests
from bs4 import BeautifulSoup
import datetime


headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'zh-CN,zh;q=0.9',
}


class Crawl(object):
    def __init__(self):
        self.title = []                                                                     # 标题
        self.content = []                                                                   # 内容
        self.rank = []                                                                      # 评分
        self.date = []                                                                      # 日期

        self.url = None
        self.html = ''
        self.page_last_num = None                                                           # 最后一页
        self.soup = BeautifulSoup(self.html, 'html.parser', from_encoding='utf-8')          # 获得soup

        self.wb = ''
        self.sheet = ''

    def init(self, url):
        if self.url is None:
            self.url = url
        else:
            self.url = self._get_next_url()
        self.html = self._get_html()
        self.soup = self._get_soup()
        self.url = self._get_next_url()
        self.title = self._get_title()
        self.content = self._get_content()
        rank, date = self._get_rank_and_date()
        self.rank = rank
        self.date = date

    def __enter__(self):
        # 创建 xls 文件对象
        self.wb = xlwt.Workbook()
        # 新增一个表单
        self.sheet = self.wb.add_sheet('Sheet 1')
        sh_title = [u'评论题目', u'评论内容', u'评论时间', u'评论评分']
        for i in range(4):
            self.sheet.write(0, i, sh_title[i])
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.wb.save('data.xls')

    def _get_html(self):
        return requests.get(url=self.url, headers=headers).content

    def _get_soup(self):
        return BeautifulSoup(self.html, 'html.parser', from_encoding='utf-8')

    def _get_next_url(self):
        item = self.soup.find('a', class_='nav next taLnk ')
        return 'https://www.tripadvisor.cn' + item['href']

    def _get_title(self):
        title = []
        items = self.soup.find_all('span', class_='noQuotes')
        for item in items:
            title.append(item.text)
        return title

    def _get_content(self):
        content = []
        items = self.soup.find_all('p', class_='partial_entry')
        for item in items:
            content.append(item.text)
        return content

    def _get_rank_and_date(self):
        rank = []
        date = []
        items = self.soup.find_all('div', class_='rating reviewItemInline')
        for item in items:
            rank.append(str(item.contents[0]['class'][1][-2]))
            date.append(item.contents[1]['title'])
        return rank, date
489100193

if __name__ == '__main__':
    num_pages = 1325
    start_url = 'https://www.tripadvisor.cn/ShowUserReviews-g294212-d319086-r417921610.html'
    start_time = datetime.datetime.now()
    with Crawl() as crawl:
        for i in range(1, num_pages+1):
            print(u'第{0}页 {1}'.format(i, start_url))
            crawl.init(start_url)
            j = 1
            for title, content, date, rank in zip(crawl.title, crawl.content, crawl.date, crawl.rank):
                crawl.sheet.write((i-1)*5+j, 0, title)
                crawl.sheet.write((i-1)*5+j, 1, content)
                crawl.sheet.write((i-1)*5+j, 2, date)
                crawl.sheet.write((i-1)*5+j, 3, rank)
                j += 1
            start_url = crawl.url
    end_time = datetime.datetime.now()
    print (u'运行时间: {0}'.format(end_time - start_time).seconds)

