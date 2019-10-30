import requests
from bs4 import BeautifulSoup

new_article_url = 'http://47.94.140.188:18035/#/article/create_article'

response = requests.get(new_article_url)
with open('new.html', 'w', encoding='utf8') as f:
    f.write(response.text)