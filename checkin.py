# encoding=utf8

import undetected_chromedriver as uc
import json
from selenium.webdriver.common.by import By
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
    return out

def socloud(cookie_string):
    # 设置驱动选项
    options = uc.ChromeOptions()
    # options.add_argument('--proxy-server=socks5://127.0.0.1:10088')
    options.add_argument("--disable-popup-blocking")

    # 获取驱动版本
    version = get_driver_version()

    
    # 创建驱动
    driver = uc.Chrome(version_main=version, options=options)
    
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
        time.sleep(3)
        element = driver.find_element(By.XPATH, '//*[@id="checkin-div"]/a')
        if element.text == '明日再来':
            print('签到成功')

    # input()

    # 退出
    driver.close()
    


if __name__ == "__main__":
    b64str = sys.argv[1]
    assert b64str
    
    # # 编码
    # message = "Hello, World!"
    # message_bytes = message.encode()
    # base64_bytes = base64.b64encode(message_bytes)
    # base64_message = base64_bytes.decode()
    # print(base64_message)

    # 解码
    base64_message = b64str
    base64_bytes = base64_message.encode()
    message_bytes = base64.b64decode(base64_bytes)
    cookie_string = message_bytes.decode()
    # print(cookie_string)

    socloud(cookie_string)