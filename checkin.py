import undetected_chromedriver as uc
import json
from selenium.webdriver.common.by import By
import time
import sys

def socloud(cookie_string):
    # 设置驱动选项
    options = uc.ChromeOptions()
    # options.add_argument('--proxy-server=socks5://127.0.0.1:10088')
    options.add_argument("--disable-popup-blocking")

    # 创建驱动
    driver = uc.Chrome(version_main='110', options=options)

    # 记得写完整的url 包括http和https
    driver.get('https://socloud.me/user##')

    # 首先清除由于浏览器打开已有的
    driver.delete_all_cookies()

    # 读取cookie
    # with open('cookies.txt','r') as f:
    #     # 使用json读取cookies 注意读取的是文件 所以用load而不是loads
    #     cookies_list = json.load(f)

    #     #方法2删除该字段
    #     for cookie in cookies_list:
    #         # 该字段有问题所以删除就可以 
    #         # if 'expiry' in cookie:
    #         #     del cookie['expiry']
    #         driver.add_cookie(cookie)

    # 读取及载入cookie
    cookies_list = json.loads(cookie_string)
    for cookie in cookies_list:
        driver.add_cookie(cookie)

    # 刷新网页
    driver.refresh()

    # 检测签到情况
    element = driver.find_element(By.XPATH, '//*[@id="checkin-div"]/a')
    # print(element.text)
    if element.text == '明日再来':
        print('明日再来, 今天已签到')
    else:
        element.click()
        print('进行签到')
        element.clear()
        time.sleep(3)
        element = driver.find_element(By.XPATH, '//*[@id="checkin-div"]/a')
        if element.text == '明日再来':
            print('签到成功')

    # input()

    # 退出
    driver.close()


if __name__ == "__main__":
    cookie_string = sys.argv[1]
    assert cookie_string
    
    socloud(cookie_string)