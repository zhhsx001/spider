import requests
from selenium import webdriver
from bs4 import BeautifulSoup
import pandas as pd


url = 'https://news.163.com/'
aim = ['wangyi.html', 'domestic.html', 'world.html', 'tech.html', 'jiankang.html']


def home_spider(url_, file_name):
    browser = webdriver.Chrome()
    try:
        browser.get(url)
        home_soup = BeautifulSoup(browser.page_source, 'lxml')
        article_list = home_soup.find_all(class_="data_row news_article clearfix")
        string = pd.DataFrame(columns=['url', 'title', 'img', 'time', 'keywords'])

        for article in article_list:
            one_title = pd.Series(index=['url', 'title', 'img', 'time', 'keywords'])
            one_title['url'] = article.a['href']
            one_title['title'] = article.h3.string
            one_title['img'] = article.img['src']
            one_title['time'] = article.span.string
            article_keywords = ''

            keywords = article.find(class_='keywords')
            try:
                for a in keywords.find_all('a'):
                    article_keywords += ' ' + a.string

            except Exception as e:
                continue
            one_title['keywords'] = keywords
            string = string.append(one_title, ignore_index=True)

        string.to_csv('wangyi.csv')
    finally:
        browser.close()


def html_spider(url_):
    result = requests.get(url_)
    with open('new.html', 'w', encoding='utf8') as f:
        f.write(result.text)


def page_analysis(html):
    pass


def save_file():
    pass


def content():
    # 根据选取返回的列表，将对应页面下载，分成大小图两个文件夹。
    pass


def text_report():
    pass


with open('html/tech.html', 'r') as f:
    s = BeautifulSoup(f, 'lxml')
    text = s.get_text()
    x = s.body


with open('wangyi.html', 'r', encoding='utf-8') as f:
    html = f.read()
soup = BeautifulSoup(html, 'lxml')
res_list = soup.find_all(class_="data_row news_article clearfix news_first")
res = res_list[0]
print('a: ', res.a['href'])
print('标题：', res.h3.string)
print('小图: ', res.img['src'])
'''for r in res:
    # 标题

    # url
    # 小图'''