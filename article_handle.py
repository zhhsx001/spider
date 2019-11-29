import requests
import pandas as pd
from bs4 import BeautifulSoup


class Article(object):
    def __init__(self, html, file_id, kind=None):
        # content: BeautifulSoup.
        self.img_kind = ''
        self.id = file_id
        self.kind = kind
        self.html = BeautifulSoup(html, 'lxml')
        self.content = self.html.find(id="endText")

    def content_kind(self):
        # 不显示图集类型文章。短文字，加视频的文章如何？
        pass

    def old_title(self):
        # 删除原标题
        tap = self.content.p
        if tap.get('class'):
            if tap.get('class')[0] == 'otitle':
                tap.extract()

    def video(self):
        # 删除视频
        for tap in self.content.find_all(class_='video-inner'):
            tap.extract()

    def del_link(self):
        # 删除扩展阅读
        tap = self.content.find(class_='special_tag_wrap')
        if tap:
            tap.extract()

    def del_editor(self):
        # 删除文脚编辑，文章内容编辑。
        tap = self.content.find(class_='ep-source cDGray')
        if tap:
            tap.extract()

    def add_editor(self):
        # 定位文章内容，删除页脚责编，增加诸黎。
        p_list = self.content.find_all('p')
        p_list[-1].string = '编辑诸黎'

    def del_blank(self):
        for p in self.content.find('p'):
            if p:
                if p.string is None:
                    p.extract()

    def save_img(self):
        tap_img = self.content.img
        if tap_img:
            img_url = tap_img.get('src')
            img = requests.get(img_url)
            with open('new/big/'+self.id+'p.'+img_url.split('.')[-1].split('?')[0], 'wb') as f:
                f.write(img.content)
        else:

            img_url = pd.read_csv('df_test.csv').iloc[int(self.id)]['img']

            img = requests.get(img_url)
            with open('new/small/'+self.id+'p.'+img_url.split('.')[-1].split('?')[0], 'wb') as f:
                f.write(img.content)
        self.img_kind = img_url.split('.')[-1].split('?')[0]

    def tech_handle(self):
        # 科技类文章，头尾需要特殊处理。
        p_list = self.content.find_all('p')
        if p_list[2].b:
            p_list[2].extract()
        if p_list[3].b:
            p_list[3].extract()

    def all_handle(self):
        # 所有处理，返回最终content图文结果
        self.old_title()
        #   self.del_blank()
        self.video()
        self.del_link()
        self.del_editor()
        self.add_editor()
        self.save_img()
        if self.kind == 'tech':
            self.tech_handle()

        return self.content.prettify()



