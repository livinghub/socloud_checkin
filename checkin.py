# encoding=utf8

import undetected_chromedriver as uc
import json
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
import time
import sys
import platform
import subprocess
import base64
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer,encoding='utf-8')

def get_driver_version():
    system = platform.system()
    if system == "Linux": # github actions linux 系统没有图形化界面，该选项不能直接用
        cmd = r'google-chrome --version'
    elif system == "Darwin":
        cmd = r'''/Applications/Google\ Chrome.app/Contents/MacOS/Google\ Chrome --version'''
    elif system == "Windows":
        cmd = r'''powershell -command "&{(Get-Item 'C:\Program Files\Google\Chrome\Application\chrome.exe').VersionInfo.ProductVersion}"'''

    try:
        out, err = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()
    except IndexError as e:
        print('Check chrome version failed:{}'.format(e))
        return 0
    if system == "Linux" or system == "Darwin":
        out = out.decode("utf-8").split(" ")[2].split(".")[0]
    elif system == "Windows":
        out = out.decode("utf-8").split(".")[0]
    # print(out)
    return int(out)

def socloud(cookie_string):
    # 设置驱动选项
    options = uc.ChromeOptions()
    # options.add_argument('--proxy-server=socks5://127.0.0.1:10088')
    options.add_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36 GLS/100.10.9989.100")
    options.add_argument("--disable-popup-blocking")

    # 获取驱动版本
    version = get_driver_version()

    
    # 创建驱动
    driver = uc.Chrome(version_main=version, options=options)
    
    # 记得写完整的url 包括http和https
    driver.get('https://socloud.me/user##')

    # 首先清除由于浏览器打开已有的
    driver.delete_all_cookies()

    # 读取及载入cookie
    if cookie_string.startswith("cookie:"):
        cookie_string = cookie_string[len("cookie:"):]
    cookie_string = cookie_string.replace("/","%2")
    cookie_dict = [ 
        {"name" : x.split('=')[0].strip(), "value": x.split('=')[1].strip()} 
        for x in cookie_string.split(';')
    ]
    for cookie in cookie_dict:
        driver.add_cookie({
            "domain": "socloud.me", # need to change
            "name": cookie["name"],
            "value": cookie["value"],
            "path": "/",
        })

    # 刷新网页
    driver.refresh()

    # 等待首页出现
    WebDriverWait(driver, 240).until(
        lambda x: x.title != "登录 — SoCloud"
    )

    # 检测签到情况
    element = driver.find_element(By.XPATH, '//*[@id="checkin-div"]/a')
    # print(element.text)
    if element.text == '明日再来':
        print('明日再来, 今天已签到')
    elif element.text == '每日签到':
        element.click()
        print('进行签到')
        time.sleep(3)
        element = driver.find_element(By.XPATH, '//*[@id="checkin-div"]/a')
        if element.text == '明日再来':
            print('签到成功')

    # input()

    # 退出
    # driver.close()
    driver.quit()
    


if __name__ == "__main__":
    cookie_string = sys.argv[1]
    assert cookie_string
    
    socloud(cookie_string)