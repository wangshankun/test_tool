from queue import Empty
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import pyautogui
import json
import time

def scroll_to_bottom(driver):
    js = "return action=document.body.scrollHeight"
    # 初始化现在滚动条所在高度为0
    height = 0
    # 当前窗口总高度
    new_height = driver.execute_script(js)

    while height < new_height:
        # 将滚动条调整至页面底部
        for i in range(height, new_height, 300):
            driver.execute_script('window.scrollTo(0, {})'.format(i))
            time.sleep(0.5)
        height = new_height
        time.sleep(2)
        new_height = driver.execute_script(js)

# 輸入PDF保存的路徑
PDF_savepath = r'C:\Users\swang\Desktop\渤海小吏文章'
chrome_options = webdriver.ChromeOptions()
appState = {
   'recentDestinations': [
      {
           'id': 'Save as PDF',
           'origin': 'local',
           'account': ''
      }
  ],
   'selectedDestinationId': 'Save as PDF',
   'version': 2,
   #取消页眉页脚
   "isHeaderFooterEnabled": False
}
prefs = {
   'printing.print_preview_sticky_settings.appState': json.dumps(appState), 
   'savefile.default_directory': PDF_savepath
}
chrome_options.add_experimental_option('prefs', prefs)
chrome_options.add_argument('--kiosk-printing')
#chrome_options.add_argument('--window-size=1920,1080')   # 设置窗口界面大小
#chrome_options.add_argument('--headless')#设置无头模式

CHROMEDRIVER_PATH = "D:\chromedriver_win32\chromedriver.exe"


fo = open(r"C:\Users\swang\Desktop\bohaixiaoli.txt", "r")
urls = fo.readlines()
fo.close()
urls.reverse()

for target_url in urls:
    #target_url = "https://mp.weixin.qq.com/s?__biz=MzUyMzUyNzM4Ng==&mid=2247502236&idx=2&sn=078ab216b38c098af551c2d9b2283c8c&chksm=fa39bc29cd4e353f57196ded7297778a50a72b4e6d1ef3b3fccf84ae8a55e65a60474521bdbb&scene=21#wechat_redirect"
    #target_url = "https://mp.weixin.qq.com/s?__biz=MzUyMzUyNzM4Ng==&mid=2247511265&idx=1&sn=e37efc6efa6148a101907b3fa04aab3e&chksm=fa39d954cd4e5042ef3a72b1ea9e199778e927d72b9fbd3c7a85efa1bd7e84c7a94595c5be50&scene=27#wechat_redirect"
    driver = webdriver.Chrome(options=chrome_options, executable_path=CHROMEDRIVER_PATH)
    driver.get(target_url)
    elements = driver.find_elements(By.XPATH, '//div[@id="meta_content"]/span')
    #print(target_url)
    #print(elements)
    flags = [x.text for x in elements]

    if "渤海小吏" in flags:
        driver.execute_script("""
        var element = document.querySelector('div[id="content_bottom_area"]');
        if (element)
            element.parentNode.removeChild(element);
        """)
        elements = driver.find_elements(By.XPATH, '//div[@id="js_content"]/section')
        for element in elements:
            driver.execute_script("""
            var element = arguments[0];
            element.parentNode.removeChild(element);
            """, element)

        elements = driver.find_elements(By.XPATH, '//span[(text()="点击下方关注小吏")]')
        for element in elements:
            driver.execute_script("""
            var element = arguments[0];
            element.parentNode.removeChild(element);
            """, element)

        elements = driver.find_elements(By.XPATH, '//div[@id="js_tags"]')
        for element in elements:
            driver.execute_script("""
            var element = arguments[0];
            element.parentNode.removeChild(element);
            """, element)

        scroll_to_bottom(driver)
        
        title = driver.find_element(By.XPATH, '//h1[@id="activity-name"]').text
        publish_time = driver.find_element(By.XPATH, '//em[@id="publish_time"]').text
        save_name = publish_time + " " + title

        try:
            driver.execute_script('document.title="{}";window.print();'.format(save_name))
        except Exception as e:
            print(e)
            l = '.()%#@!/&''""'
            trantab = dict((ord(char), u'') for char in l)#去掉特殊符号尤其是双引号，这会导致execute_script解析失败
            save_name = str(save_name).translate(trantab)
            driver.execute_script('document.title="{}";window.print();'.format(save_name))
        driver.quit()
