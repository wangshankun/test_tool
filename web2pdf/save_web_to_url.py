from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import pyautogui
import json
import time

# 輸入PDF保存的路徑
PDF_savepath = r'C:\Users\swang\Desktop'
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
driver = webdriver.Chrome(options=chrome_options, executable_path=CHROMEDRIVER_PATH)

target_url = "https://mp.weixin.qq.com/s?__biz=MzUyMzUyNzM4Ng==&mid=2247502236&idx=2&sn=078ab216b38c098af551c2d9b2283c8c&chksm=fa39bc29cd4e353f57196ded7297778a50a72b4e6d1ef3b3fccf84ae8a55e65a60474521bdbb&scene=21#wechat_redirect"
driver.get(target_url)
#driver.execute_script("window.scrollBy(0,500)")
#driver.execute_script("""var data=document.querySelectorAll('div[role="link"][tabindex="0"]').forEach(v=>v.remove())""")
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

elements = driver.find_elements(By.XPATH, '//span[(text()= "点击下方关注小吏")]')
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

'''
element = driver.find_element(By.XPATH, '//div[@id="js_content"]/section[2]')
print(element)
driver.execute_script("""
var element = arguments[0];
element.parentNode.removeChild(element);
""", element)
'''

'''
driver.execute_script("""
var data=document.querySelectorAll('.wx_profile_card_inner').forEach(v=>v.remove())
""")
'''
#driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")#直接滚动到页末
#element_present = EC.presence_of_element_located((By.ID, 'element_id'))
'''
# 定义一个初始值
temp_height = 0
while True:
    # 循环将滚动条下拉
    driver.execute_script("window.scrollBy(0,500)")
    # sleep一下让滚动条反应一下
    time.sleep(1)
    # 获取当前滚动条距离顶部的距离
    check_height = driver.execute_script(
        "return document.documentElement.scrollTop || window.pageYOffset || document.body.scrollTop;")
    print(check_height, temp_height)
    # 如果两者相等说明到底了
    if check_height == temp_height:
        break
    temp_height = check_height
'''

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

#等待图片全部刷新出来，但是不滑动鼠标不会主动刷新出来
#element_present = EC.presence_of_all_elements_located((By.CLASS_NAME, 'rich_pages wxw-img'))
#WebDriverWait(driver, 60).until(element_present)
scroll_to_bottom(driver)
driver.execute_script('window.print();')

#移动鼠标点击保存按钮
#pyautogui.moveTo(1209, 928, 1)
#pyautogui.click(button='left')

driver.quit()
