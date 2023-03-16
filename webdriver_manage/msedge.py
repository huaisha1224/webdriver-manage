#!/usr/bin/env python
# -*- coding:utf-8 -*-
__author__ = "Sam.huang"

# from selenium import webdriver
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC
# from selenium.webdriver.common.by import By
# from selenium.webdriver.common.keys import Keys
from os import path, remove, popen
from sys import argv
from zipfile import ZipFile
from winreg import OpenKey, QueryValueEx, HKEY_CURRENT_USER
from requests import get
from datetime import datetime
from selenium import webdriver



# chrome_options = webdriver.ChromeOptions()
# chrome_options.add_argument('log-level=3')
# #   去除webdriver特征
# chrome_options.add_experimental_option('excludeSwitches', ['enable-automation'])
# chrome_options.add_experimental_option('excludeSwitches', ['enable-automation'])
# chrome_options.add_experimental_option('useAutomationExtension', False)
# chrome_options.add_argument("--disable-blink-features")
# chrome_options.add_argument("--disable-blink-features=AutomationControlled")


def get_msedgedriver_path():
    """
    获取MSedgeDriver路径
    """
    # 通过命令行获取本机所有path路径
    try:
        out_path_dir = popen('echo %PATH%').read()
        path_dir_list = out_path_dir.split(';')

        # 遍历path路径中是否有msedgedriver.exe文件
        for msedgedriver_path in path_dir_list:
            if path.exists(msedgedriver_path + '\msedgedriver.exe'):
                return msedgedriver_path

                # 未找到msedgedriver时就安装到Python目录下
            elif path.exists(msedgedriver_path + '\python.exe'): 
                return msedgedriver_path
            else:
                pass
    except IndexError:
        pass


def get_local_edge_version():
    """
    通过注册表获取本机Edge浏览器版本
    """
    try:
        # 通过注册表获取安装的Edge版本号
        key = OpenKey(HKEY_CURRENT_USER, r'SOFTWARE\Microsoft\Edge\BLBeacon')
        local_edge_version, types = QueryValueEx(key, 'version')
        print('本机Edge浏览器版本：{}'.format(local_edge_version))
        return local_edge_version
    except WindowsError as e:
        print("未安装Edge,请在Edge官网：https://www.microsoft.com/zh-cn/edge/ 下载。")


def get_local_msedgedriver_version():
    """
    查询系统安装的msedgedriver版本
    """
    # 用popen通过命令行查询msedgedriver版本号
    # Microsoft Edge WebDriver 110.0.1587.56 (65e63b43e03b1519efb720810a66373ecd5de466)
    try:
        outstd = popen('msedgedriver --version').read()
       
        local_msedgedriver_version = outstd.split(' ')[3]     # 取第二个值即版本号
        print('本机MSEdgeDriver版本 {}'.format(local_msedgedriver_version))
        return local_msedgedriver_version
    
    except IndexError as e:
        # print("本机未安装MSEdgeDriver")
        return 0 


def download_msedgedriver(msedgedriver_version):
    """
    下载MSEdgeDriver版本
    """
    # 下载MSEdgeDriver文件到当前目录
    # download_msedgedriver_url = 'https://msedgedriver.azureedge.net/111.0.1661.43/edgedriver_win32.zip'
    download_msedgedriver_url = f"https://msedgedriver.azureedge.net/{msedgedriver_version}/edgedriver_win32.zip"
    file = get(download_msedgedriver_url)
    with open("edgedriver_win32.zip", "wb") as zip_file:        
        zip_file.write(file.content)
        print("MSEdgeDriver下载完成")
    

    # 解压文件到MSEdgeDriver path路径下
    path = get_msedgedriver_path()
    msedgedriver_file = ZipFile("edgedriver_win32.zip", "r")
    for file in msedgedriver_file.namelist():
        if path != None:
            msedgedriver_file.extract(file, path)
        else:
            pass
    msedgedriver_file.close()
    remove('edgedriver_win32.zip')
    print(f"MSEdgeDriver文件替换到 {path} 成功。")
    get_local_msedgedriver_version()
    #print('本机msedgedriver最新版本：',get_local_chromedriver_version())
    

def check_msedgedriver():
    """
    判断本地Edge版本和MSEdgeDriver版本是否匹配
    """

    try:
        # 判断本机Edge版本号
        edge_version = get_local_edge_version()
        edge_main_version = int(edge_version.split(".")[0])     # 获取Edge主版本号
    except WindowsError as e:
        print("未安装Edge,请在Edge官网：https://www.microsoft.com/zh-cn/edge/ 下载。")
        return 0
    
    try:
        # 判断是否安装MSEdgeDriver以及版本
        msedgedriver_version = get_local_msedgedriver_version()
        # print(msedgedriver_version)
        if msedgedriver_version != 0:
            msedgedriver_main_version = int(msedgedriver_version.split(".")[0]) # 获取msedgedriver主版本号
        else:
            # print(msedgedriver_version)
            print("本机未安装MSEdgeDriver, 需下载安装MSEdgeDriver")
            msedgedriver_main_version = 0


    except IndexError as e:
        return 0

    if edge_main_version != msedgedriver_main_version:
        print("MSEdgeDriver版本 {} 和Edge版本 {} 不兼容,需要更新MSEdgeDriver".format(msedgedriver_version,edge_version))
        download_msedgedriver(edge_version)

    else:
        print("MSEdgeDriver版本{}和Edge版本{}兼容，无需更新MSEdgeDriver版本".format(msedgedriver_version,edge_version))



if __name__=='__main__':
    # print(get_msedgedriver_path())
    # get_local_edge_version()
    # get_local_msedgedriver_version()
    # download_msedgedriver()
    check_msedgedriver()