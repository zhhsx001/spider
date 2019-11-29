import os
from flask import Flask, url_for, render_template, request, flash, redirect
from bs4 import BeautifulSoup
import pandas as pd
import spider
import article_handle
app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def show_title():
    if request.method == 'POST':
        return redirect('accept_title')
    df = pd.read_csv('df_test.csv')
    df = df[['url', 'title']]
    return render_template('index.html', tables=df)


@app.route('/complete', methods=['GET', 'POST'])
def accept_title():
    result = []
    for key in request.form.keys():

        result.append(key)
    result = pd.Series(result)

    result.to_csv('choices.csv', header=False, encoding='utf8')
    return render_template('complete.html')


@app.route('/report', methods=['GET', 'POST'])
def report():
    spider.big_and_small_spilt()
    big_html = os.listdir('new/big')
    small_html = os.listdir('new/small')
    df = pd.read_csv('df_test.csv')

    for i in range(30):
        try:
            # 处理比例不平衡条件。
            if i % 3 == 0 and big_html:
                html_uri = big_html.pop()
                img_uri = 'new/big/'+html_uri[:-5]+'p.'
                button = True
                html_uri = 'new/big/'+ html_uri
            elif small_html:
                html_uri = small_html.pop()
                img_uri = 'new/small/'+html_uri[:-5]+'p.'
                button = False
                html_uri = 'new/small/'+html_uri
            elif big_html:
                html_uri = big_html.pop()
                img_uri = 'new/big/'+html_uri[:-5]+'p.'
                button = False
                html_uri = 'new/big/'+ html_uri

            with open(html_uri, 'r', encoding='utf8') as f:
                html_page = f.read()

            article = article_handle.Article(html_page, html_uri[:-5].split('/')[-1])
            article.all_handle()

            # title, image_url = [], button = False, content = '', video = ''
            title = df.iloc[int(html_uri[:-5].split('/')[-1])]['title']
            image_url = [{'url': 'https://cdn.kingmasports.com/'+spider.picture_post(img_uri+article.img_kind,
                                                                                      article.img_kind)}]

            content = article.content.prettify()
            video = ''
            spider.create_article(title=title, image_url=image_url, button=button, content=content, video=video)
        except Exception as e:
            print('Error: ', e)

    return render_template('report.html')


if __name__ == '__main__':
    aim = ['https://news.163.com/', 'https://news.163.com/world/', 'https://news.163.com/domestic/',
           'https://tech.163.com/', 'https://sports.163.com/', 'https://ent.163.com/']
    url_ = aim[0]
    file_name = 'df_test'
    spider.home_spider(url_, file_name)
    app.run()