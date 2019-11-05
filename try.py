
import requests
from bs4 import BeautifulSoup
import article_handle

url = 'https://news.163.com/19/1104/13/ET52RF810001875P.html'

res = requests.get(url)

article = article_handle.Article(res.text, '12')


