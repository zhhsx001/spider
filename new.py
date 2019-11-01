from bs4 import BeautifulSoup
import requests


url = 'http://47.94.140.188:18035/#/article/create_article'
res = requests.get(url)
with open('new.html', 'w', encoding='utf8') as f:
    f.write(res.text)
