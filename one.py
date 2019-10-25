import chardet
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait


browser = webdriver.Chrome()
try:
    browser.get('https://news.163.com/')

    #wait = WebDriverWait(browser, 10)
    print(type(browser))
    s = browser.page_source
    print(type(s))
    with open('wangyi.html', 'w', encoding='utf-8') as f:
        f.write(browser.page_source)
finally:
    browser.close()