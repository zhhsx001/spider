from bs4 import BeautifulSoup
import requests

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