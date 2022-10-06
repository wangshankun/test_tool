import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
import json
import re
import random

proxies ={
        'http': 'http://127.0.0.1:4780',
        'https': 'http://127.0.0.1:4780'  # https -> http
    }

headers={
        'Accept': '*/*',
        'Accept-Language': 'en-US,en;q=0.8',
        'Cache-Control': 'max-age=0',
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.116 Safari/537.36',
        'Connection': 'keep-alive'
    }

CHROMEDRIVER_PATH = "D:\chromedriver_win32\chromedriver.exe"
driver = webdriver.Chrome(executable_path=CHROMEDRIVER_PATH)

def getCookie():
    # 调用谷歌浏览器驱动
    #driver = webdriver.Chrome()

    driver.get("https://mp.weixin.qq.com/")
    driver.find_element(by=By.LINK_TEXT, value="使用帐号登录").click()
    driver.find_element(by=By.NAME, value="account").clear()
    # 公众号的账号
    driver.find_element(by=By.NAME, value="account").send_keys("tianruoqxxxx@163.com")
    time.sleep(2)
    driver.find_element(by=By.NAME, value="password").clear()
    driver.find_element(by=By.NAME, value="password").send_keys("Fxxxxxxx7")
    driver.find_element(by=By.CLASS_NAME, value="icon_checkbox").click()

    time.sleep(2)
    driver.find_element(by=By.CLASS_NAME, value="btn_login").click()
    time.sleep(15)
    # 此时会弹出扫码页面，需要微信扫码
    cookies = driver.get_cookies()  # 获取登录后的cookies
    print("========cookies======")
    print(cookies)
    cookie = {}
    for items in cookies:
        cookie[items.get("name")] = items.get("value")
    return cookie

def getToken(cookie):
    url = "https://mp.weixin.qq.com/"
    res = requests.get(url,headers=headers,cookies=cookie)

    token = re.findall(r'token=(\d+)', str(res.text))[0]
    return token

if __name__ == '__main__':
    cookie=getCookie()
    with open('cookies.txt', "w")as file:
        file.write(json.dumps(cookie))

    token=getToken(cookie)
    print("========token======")
    print(token)

    element = driver.find_element(By.XPATH, '//*[@id="app"]/div[2]/div[4]/div[2]/div/div[2]')
    element.click()
    time.sleep(3)
    driver.switch_to.window(driver.window_handles[-1])  # 切换到最后一个页签
    
    element = driver.find_element(By.XPATH, '//*[@id="js_editor_insertlink"]')
    element.click()
    time.sleep(1)

    element = driver.find_element(By.XPATH, '//button[(text()= "选择其他公众号")]')
    element.click()
    time.sleep(1)

    element = driver.find_element(By.XPATH, '//input[@placeholder="输入文章来源的公众号名称或微信号，回车进行搜索"]')
    element.send_keys('渤海小吏封建脉络百战')#传送入关键词
    element.send_keys(Keys.ENTER)
    time.sleep(2)
    
    element = driver.find_element(By.XPATH, '//strong[@class="inner_link_account_nickname"]')
    element.click()
    time.sleep(2)

    #elements = driver.find_elements(By.XPATH, '//div[@class="inner_link_article_title"]')
    #print(elements)

    element = driver.find_element(By.XPATH, '//input[@class="weui-desktop-pagination__input"]')
    element.send_keys(Keys.CONTROL, "a")
    ##element.clear()#先清空，本方法无效
    element.send_keys('46')#传送入关键词
    element = driver.find_element(By.LINK_TEXT, "跳转")
    element.click()
    time.sleep(1)

    with open(r"C:\Users\swang\Desktop\-wechat--main\urls.txt", "a+") as file:
        while True:
            elements = driver.find_elements(By.XPATH, '//a[(text()= "查看文章")]')
            for i in elements:
                url = i.get_attribute('href')
                print(url)
                file.write(url + "\n")

            element = driver.find_element(By.LINK_TEXT, "下一页")
            element.click()
            time.sleep(random.randint(1,11))




