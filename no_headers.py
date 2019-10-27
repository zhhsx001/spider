from bs4 import BeautifulSoup
import requests

with open('wangyi.html', 'r', encoding='utf-8') as f:
    html = f.read()
soup = BeautifulSoup(html, 'lxml')
res_list = soup.find_all(class_="data_row news_article clearfix")
res = res_list[0]

print('a: ', res.a['href'])
print('标题：', res.h3.string)
print('小图: ', res.img['src'])
print('时间: ', res.span.string)
for a in res.find(class_='keywords').find_all('a'):
    print(a.string)


'''for res in res_list:
print('a: ', res.a['href'])
    print('标题：', res.h3.string)
    print('小图: ', res.img['src'])
    print('a: ', res.a['href'])
    print('标题：', res.h3.string)
    print('小图: ', res.img['src'])
    标签 <div class="keywords">
    发布时间<span class="time">27分钟前</span>
    # 标题
    
    # url
    # 小图'''