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
        time.sleep(0.5)
        new_height = driver.execute_script(js)

# 輸入PDF保存的路徑
PDF_savepath = r'C:\Users\swang\Desktop\文章'
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
 
CHROMEDRIVER_PATH = "D:\chromedriver_win32\chromedriver.exe"
 
target_url = "https://www.e360xs.com/mulu/150/150175-77415433.html"

while target_url != "":
    driver = webdriver.Chrome(options=chrome_options, executable_path=CHROMEDRIVER_PATH)
    driver.get(target_url)

    driver.execute_script(  """
                                document.querySelectorAll('img[class="richText-img-source"]').forEach(el => el.remove());#删除所有图片
                            """)

    elements = driver.find_elements(By.XPATH, '//figcaption')
    for element in elements:
        driver.execute_script("""
        var element = arguments[0];
        element.parentNode.removeChild(element);
        """, element)

    driver.execute_script(  """
                                var element = document.querySelector('div[id="header"]');
                                if (element)
                                    element.parentNode.removeChild(element);
                            """)

    driver.execute_script(  """
                                var element = document.querySelector('div[id="read_title"]');
                                if (element)
                                    element.parentNode.removeChild(element);
                            """)

    driver.execute_script(  """
                                var element = document.querySelector('div[id="reader_top"]');
                                if (element)
                                    element.parentNode.removeChild(element);
                            """)

    driver.execute_script(  """
                                var element = document.querySelector('div[id="bottom"]');
                                if (element)
                                    element.parentNode.removeChild(element);
                            """)
                            
    driver.execute_script(  """
                                var element = document.querySelector('div[class="article_nav"]');
                                if (element)
                                    element.parentNode.removeChild(element);
                            """)

    scroll_to_bottom(driver)

    next_page = driver.find_element(By.XPATH, '//a[(text()= "下一页(快捷键:→)")]')
    target_url = next_page.get_attribute('href')

    elements = driver.find_elements(By.XPATH, '//*[@id="read_content"]/a')
    for element in elements:
        driver.execute_script("""
        var element = arguments[0];
        element.parentNode.removeChild(element);
        """, element)

    driver.execute_script(  """
                                var element = document.querySelector('div[id="read_link"]');
                                if (element)
                                    element.parentNode.removeChild(element);
                            """)

    driver.execute_script('window.print()')
    
    driver.quit()
