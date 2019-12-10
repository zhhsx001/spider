import requests
import re
import pandas as pd
from bs4 import BeautifulSoup


class Article(object):
    def __init__(self, html, file_id):
        # html :html
        self.id = file_id
        self.img_kind = ''
        self.video_url = ''
        self.html = BeautifulSoup(html, 'lxml')
        # content/text 位于p StartFragment与 p EndFragment之间
        self.content = self.html.body.find(id="endText")

    def no_kind(self):
        # 报错跳过，
        pass

    def del_attr(self):
        # 删除格式
        del self.content['class']
        del self.content['style']

    def del_brackets(self):
        # 删除括号内容
        re_ = re.compile(r'.*(\(.*\)).*')
        for p in self.content:
            res = None
            if p.string:
                res = re_.match(p.string)
            if res:
                s = res.group()[0]
                p.string.replace(s, '')

    def old_title(self):
        # 删除原标题
        tap = self.content.p
        if tap.get('class'):
            if tap.get('class')[0] == 'otitle':
                tap.extract()

    def video(self):
        # 重构是解决如何处理视频文章。
        # 视频地址
        # video = self.html.find(target="_blank", class_="video-title")
        # self.video_url = video['href']
        # # 视频配套内容
        # self.html.find(text='StartFragment').next_sibling

        p0 = self.content.find(class_='video')
        if p0:
            res = re.match(re.compile('.*src="(.*?)">.*'), p0.find('script').string)
            self.video_url = res[1]
            p0.extract()
        p1 = self.content.find(class_='gg200x300')
        p2 = self.content.find('style')
        # print(p2.find('src'))
        p3 = self.content.find(class_='video-wrapper')
        for p in [p1, p2, p3]:
            if p:
                p.extract()
        # # 删除视频
        # for tap in self.content.find_all(class_='video-inner'):
        #     tap.extract()

    def del_link(self):
        # 删除扩展阅读
        tap = self.content.find(class_='special_tag_wrap')
        if tap:
            tap.extract()
        tap2 = self.content.pre
        if tap2:
            tap2.extract()

    def del_editor(self):
        # 删除文脚编辑，文章内容编辑。
        tap = self.content.find(class_='ep-source cDGray')
        tap.extract()

    def add_editor(self):
        # 定位文章内容，删除页脚责编，增加诸黎。
        p_list = self.content.find_all('p')
        p_list[-1].string = '编辑诸黎'

    def del_blank(self):
        # 删除空行
        for tap in self.content:
            if tap.string is None:
                tap.extract()

    def save_img(self):
        tap_img = self.content.find('img', recursive=True)
        # print(tap_img)
        if tap_img:
            img_url = tap_img.get('src')
            # print(img_url)
            img = requests.get(img_url)
            with open('new/big/'+self.id+'p.'+img_url.split('.')[-1].split('?')[0], 'wb') as f:
                f.write(img.content)
        else:
            print('htmlid: ', self.id)
            img_url = pd.read_csv('df_test.csv').iloc[int(self.id)]['img']
            img = requests.get(img_url)
            with open('new/small/'+self.id+'p.'+img_url.split('.')[-1].split('?')[0], 'wb') as f:
                f.write(img.content)
        self.img_kind = img_url.split('.')[-1].split('?')[0]

    def tech_handle(self):
        # 科技类文章，头尾需要特殊处理。
        # 粗体部分去除。
        p_list = self.content.find_all('p')
        for p in p_list:
            if p.b:
                p.extract()

    def del_ad(self):
        p = self.content.find('')

    def all_handle(self):
        # 所有处理，返回最终content图文结果
        if self.no_kind():
            return None
        self.old_title()
        self.del_editor()
        self.save_img()
        # self.video()
        self.del_attr()
        self.del_link()
        # self.del_blank()
        self.del_brackets()
        self.add_editor()

        self.tech_handle()
        return self.content.prettify()



