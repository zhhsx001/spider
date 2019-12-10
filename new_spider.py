import base64
import os
import shutil
from io import BytesIO
import requests
from selenium import webdriver
from PIL import Image
from bs4 import BeautifulSoup
import pandas as pd
import article_handle


def home_spider(url_, file_name):
    browser = webdriver.Chrome()
    try:
        browser.get(url_)
        home_soup = BeautifulSoup(browser.page_source, 'lxml')
        article_list = home_soup.find_all(class_="data_row news_article clearfix")
        if url_ == 'https://sports.163.com/':
            article_list.append(home_soup.find_all(class_='data_row news_photoview clearfix'))
        articles = pd.DataFrame(columns=['url', 'title', 'img', 'time', 'keywords'])

        for one_article in article_list:
            one_title = pd.Series(index=['url', 'title', 'img', 'time', 'keywords'])
            one_title['url'] = one_article.a['href']
            one_title['title'] = one_article.h3.string
            one_title['img'] = one_article.img['src']
            one_title['time'] = one_article.span.string

            article_keywords = ''
            keywords = one_article.find(class_='keywords')
            if keywords:
                for a in keywords.find_all('a'):
                    article_keywords += ' ' + a.string
            one_title['keywords'] = keywords
            articles = articles.append(one_title, ignore_index=True)

        articles.to_csv('%s.csv' % file_name, encoding='utf8')
    finally:
        browser.close()


def big_and_small_spilt():
    choices = pd.read_csv('choices.csv', index_col=0, header=None)
    data = pd.read_csv('df_test.csv', index_col=0)

    shutil.rmtree('new/big')
    os.mkdir('new/big')
    shutil.rmtree('new/small')
    os.mkdir('new/small')

    for url_id in choices[1]:
        url_ = data.loc[url_id, 'url']
        html_spider(url_id, url_)


def html_spider(url_id, url_):
    print('爬取: ', url_)
    # 根据选取的列表，爬取对应的new，根据有大图，无大图分成两组存储。
    request = requests.get(url_)
    soup = BeautifulSoup(request.text, 'lxml')
    content = soup.find(id="endText")

    content.find(class_='ep-source cDGray').extract()
    mark = 'small'
    img = content.find('img')
    if img:
        mark = 'big'

    with open('new/%s/%d.html' % (mark, url_id), 'w', encoding='utf8') as f:
        f.write(request.text)


def picture_post(picture_url, img_kind):
    token_url = 'http://admin.kingmasports.com/admapi/v1/store/qiniu/uploadToken?upMode=base64&uid=9'
    post_url = "https://upload-z1.qiniup.com/putb64/-1/key/"

    if img_kind == 'png':
        img_kind = 'PNG'
    elif img_kind == 'gif':
        img_kind = 'gif'
    else:
        img_kind = 'JPEG'
    token_header = {'accept': 'application/json, text/plain, */*',
                    'accept-Encoding': 'gzip, deflate',
                    'accept-Language': 'zh-CN,zh;q=0.9',
                    'authorization': 'c267a03c4d9247d0b2fc3c2ff206ffeb',
                    'connection': 'keep-alive',
                    'host': 'admin.kingmasports.com',
                    'referer': 'http://admin.kingmasports.com/',
                    'user-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)'
                                  ' Chrome/78.0.3904.87 Safari/537.36'
                    }
    token = requests.get(token_url, headers=token_header)
    encode_key = token.json()['data']['encodedKey']
    up_token = token.json()['data']['token']

    post_headers = {
        'accept': "application/json, text/plain, */*",
        'accept-encoding': "gzip, deflate, br",
        'accept-language': "zh-CN,zh;q=0.9",
        'authorization': 'UpToken ' + up_token,
        # 'content-length': "43644",
        'content-type': "application/octet-stream",
        'origin': "http://admin.kingmasports.com",
        'referer': "http://admin.kingmasports.com/",
        'sec-fetch-mode': "cors",
        'sec-fetch-site': "cross-site",
        'user-agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                      "Chrome/78.0.3904.87 Safari/537.36",
        'cache-control': "no-cache",
        'postman-token': "d037b4e3-5cd4-f506-ac21-37539c7d5ce0"
    }
    post_u = post_url + encode_key

    requests.options(post_u, headers=post_headers)

    img = Image.open(picture_url)
    output_buffer = BytesIO()
    img.save(output_buffer, format=img_kind)
    byte_data = output_buffer.getvalue()
    base64_str = base64.b64encode(byte_data)
    response = requests.post(post_u, headers=post_headers, data=base64_str)

    print('---post picture:')
    print(response.status_code)
    print(response.text)
    picture_id = response.json()['key']
    return picture_id
    # 或者上传所有文字后，根据标题选择对应的图片上传。selenium


def create_article(title, image_url=[], button=False, content='', video=''):
    article = {"articleId": 0,
               "title": title,
               "subTitle": "",
               "weight": 0,
               "categoryId": 1,
               "orgId": "",
               "articleImages": image_url,
               "jumbotron": button,
               "articleBannerImages": [],
               "video": video,
               "publish": None,
               "editorData": content}

    headers = {
        'accept': "application/json, text/plain, */*",
        'accept-encoding': "gzip, deflate",
        'accept-language': "zh-CN,zh;q=0.9",
        'authorization': "c267a03c4d9247d0b2fc3c2ff206ffeb",
        'connection': "keep-alive",
        'content-type': "application/json",
        'host': "admin.kingmasports.com",
        'origin': "http://admin.kingmasports.com",
        'referer': "http://admin.kingmasports.com/",
        'user-agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                      "Chrome/78.0.3904.87 Safari/537.36",
        'cache-control': "no-cache",
        'postman-token': "92df53b3-ab03-a1b3-66bb-3845f33d1871"
    }

    create_url = 'http://admin.kingmasports.com/admapi/v1/article/article?uid=9'

    r = requests.post(create_url, headers=headers, json=article)
    print('create article')
    print(r.text)


def report():
    big_html = os.listdir('new/big')
    small_html = os.listdir('new/small')

    df = pd.read_csv('df_test.csv')
    print('the last number: ', df.count()[0])
    for i in range(df.count()[0]):
        # 处理比例不平衡条件。
        if i % 3 == 0 and big_html:
            html_uri = big_html.pop()
            img_uri = 'new/big/' + html_uri[:-5] + 'p.'
            button = True
            html_uri = 'new/big/' + html_uri
        elif small_html:
            html_uri = small_html.pop()
            img_uri = 'new/small/' + html_uri[:-5] + 'p.'
            button = False
            html_uri = 'new/small/' + html_uri
        else:
            html_uri = big_html.pop()
            img_uri = 'new/big/' + html_uri[:-5] + 'p.'
            button = False
            html_uri = 'new/big/' + html_uri

        with open(html_uri, 'r', encoding='utf8') as f:
            html_page = f.read()
        article = article_handle.Article(html_page, html_uri[:-5].split('/')[-1])
        text = article.all_handle()
        if text is None:
            continue
        title = df.iloc[int(html_uri[:-5].split('/')[-1])]['title']
        image_url = [{'url': 'https://cdn.kingmasports.com/' + picture_post(img_uri + article.img_kind,
                                                                            article.img_kind)}]
        print(image_url)
        content = text
        video = ''
        create_article(title=title, image_url=image_url, button=button, content=content, video=video)


if __name__ == "__main__":
    pass
