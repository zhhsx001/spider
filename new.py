from bs4 import BeautifulSoup
import requests

url = 'https://news.163.com/19/1025/16/ESBJM4AE0001875O.html'
res = requests.get(url)
print(type(res.text))
'''soup = BeautifulSoup(res, 'lxml')'''
with open('new.html', 'w', encoding='utf8') as f:
    f.write(res.text)