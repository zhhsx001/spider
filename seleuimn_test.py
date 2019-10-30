import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

Cookie= 'role=%E6%80%BB%E4%BC%9A%E7%AE%A1%E7%90%86%E5%91%98; uid=9; username=yunying1; x-session-id=654e53b8876e4963bd049520d857e98a; permission={%22home%22:1%2C%22statistics%22:1%2C%22sta_article_browse%22:1%2C%22org%22:1%2C%22org_branch%22:1%2C%22org_member%22:1%2C%22zongqin_approve%22:1%2C%22zongci%22:1%2C%22shortcut%22:1%2C%22chuancheng%22:1%2C%22announcement%22:1%2C%22article%22:1%2C%22article_category%22:1%2C%22articles%22:1%2C%22create_article%22:1%2C%22donate%22:1%2C%22donate_item%22:1%2C%22modify_password%22:1}'


home_url = 'http://47.94.140.188:18035/'
new_article_url = 'http://47.94.140.188:18035/#/article/create_article'

browser = webdriver.Chrome()

browser.get(home_url)
user_name = browser.find_element_by_name('username')
user_name.send_keys('yunying1')

pass_word = browser.find_element_by_name('password')
pass_word.send_keys('6siZfgx9')
pass_word.send_keys(Keys.ENTER)

time.sleep(1)
browser.get(new_article_url)
time.sleep(2)

with open('new_article.html', 'w', encoding='utf8') as f:
    f.write(browser.page_source)

#login_form = driver.find_element_by_xpath("//form[@id='loginForm']")
title = browser.find_element_by_xpath("//input[@class='el-input__inner']")
title.send_keys('这里是标题')

kind = browser.find_element_by_xpath('/html/body/section/section/main/div/div/div/form/div[5]/div/div[1]/div/input')
print(kind)

picture = browser.find_element_by_xpath("/html/body/section/section/main/div/div/div/form/div[6]/div/div[2]/div[1]/div/div")
print(picture)


text = browser.find_element_by_xpath('//iframe[1]')
print(text)


button = browser.find_element_by_xpath('//button[1]')
button.click()
print(button)
time.sleep(3)

browser.close()
