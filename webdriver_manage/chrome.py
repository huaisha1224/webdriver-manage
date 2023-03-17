#!/usr/bin/env python
# -*- coding:utf-8 -*-
__author__ = "Sam.huang"

from os import path, remove, popen
from sys import argv
from zipfile import ZipFile
from winreg import OpenKey, QueryValueEx, HKEY_CURRENT_USER
from requests import get
from datetime import datetime
import get_path
from download_webdriver import download_webdriver

# chromedriver 下载地址
url='https://registry.npmmirror.com/-/binary/chromedriver/' 


def get_local_chrome_version():
    """
    通过注册表获取本机Chrome版本
    """
    try:
        # 通过注册表获取安装的Chrome版本号
        key = OpenKey(HKEY_CURRENT_USER, r'Software\Google\Chrome\BLBeacon')
        local_chrome_version, types = QueryValueEx(key, 'version')
        print('本机Chrome版本：{}'.format(local_chrome_version))
        return local_chrome_version
    except WindowsError as e:
        print("未安装Chrome,请在GooGle Chrome官网：https://www.google.cn/chrome/ 下载。{}".format(e))


def get_local_chromedriver_version():
    """
    查询系统安装的Chromedriver版本
    """
    # 用popen通过命令行查询Chromedriver版本号
    # ChromeDriver 110.0.5481.30 (aedb656755c469651f01505a4f15e153fc606a1e-refs/branch-heads/5481@{#191})
    try:
        outstd = popen('chromedriver --version').read()
       
        local_chromedriver_version = outstd.split(' ')[1]     # 取第二个值即版本号
        print('本机ChromeDriver版本 {}'.format(local_chromedriver_version))
        return local_chromedriver_version
    
    except IndexError as e:
        # print("本机未安装Chromedriver")
        return 0 


def get_server_chrome_versions():
    """
    获取线上所有的Chromedriver版本信息
    """
    version_list=[]
    version_url="https://registry.npmmirror.com/-/binary/chromedriver/"     # 从chromedriver所有版本信息
    rep = get(version_url).json()
    for i in rep:                               
        version = i["name"].replace("/","")         # 提取版本号
        version_list.append(version)            # 将所有版本存入列表
    # print(version_list)
    return version_list



def get_chromedriver_url(chrome_version, chrome_main_version):
    """
    chrome_version, chrome_main_version
    获取chromedriver下载链接
    """
    # chromedriver 下载地址
    url='https://registry.npmmirror.com/-/binary/chromedriver/' 
    server_chromedriver_list= get_server_chrome_versions()

    if chrome_version in server_chromedriver_list:
        # 优先使用完整版本号匹配
        download_chromedriver_url = f"{url}{chrome_version}/chromedriver_win32.zip"
        print(f"Chromedriver版本{chrome_version} 匹配成功, 开始下载")
    else:
        # 匹配失败后通过主版本号匹配
        for mian_version in server_chromedriver_list:
            if mian_version.startswith(str(chrome_main_version)):       # 用startswith() 方法检查字符串是否以主版本号开头
                download_chromedriver_url = f"{url}{mian_version}/chromedriver_win32.zip"
                print(f"Chromedriver主版本号{mian_version} 匹配成功, 开始更新")
                break
        if download_chromedriver_url == "":
            print("找不到与Chrome版本匹配的chromedriver的版本，请去 {} 查看".format(url))

    # download_chromedriver(download_chromedriver_url)
    chromedriver_path = get_path.get_webdriver_path('chromedriver.exe')
    download_webdriver(download_chromedriver_url,'chromedriver_win32.zip',chromedriver_path)
    get_local_chromedriver_version()



def download_chromedriver(download_chromedriver_url):
    """
    下载chromedriver版本
    """
    # 下载chromedriver文件到当前目录
    file = get(download_chromedriver_url)
    with open("chromedriver.zip", "wb") as zip_file:        
        zip_file.write(file.content)
        print("Chromedriver下载完成")
    

    # 解压文件到chromedriver path路径下
    path = get_path.get_webdriver_path('chromedriver.exe')
    chromedriver_file = ZipFile("chromedriver.zip", "r")
    for file in chromedriver_file.namelist():
        if path != None:
            chromedriver_file.extract(file, path)
        else:
            pass
    chromedriver_file.close()
    remove('chromedriver.zip')
    print(f"ChromeDriver文件替换到 {path} 成功。")
    get_local_chromedriver_version()
    #print('本机ChromeDriver最新版本：',get_local_chromedriver_version())
    

def check_chromedriver():
    """
    比较本地Chrome版本和Chromedriver版本是否匹配
    """

    try:
        # 判断本机Chrome版本号
        chrome_version = get_local_chrome_version()
        chrome_main_version = int(chrome_version.split(".")[0])     # 获取Chrome主版本号
    except WindowsError as e:
        print("未安装Chrome,请在GooGle Chrome官网：https://www.google.cn/chrome/ 下载。{}".format(e))
        return 0
    
    try:
        # 判断是否安装ChromeDriver以及版本
        chromedriver_version = get_local_chromedriver_version()
        # print(chromedriver_version)
        if chromedriver_version != 0:
            chromedriver_main_version = int(chromedriver_version.split(".")[0]) # 获取chromedriver主版本号
        else:
            # print(chromedriver_version)
            print("本机未安装Chromedriver, 需下载安装ChromeDriver")
            chromedriver_main_version = 0
            # get_chromedriver_url(chrome_version, chrome_main_version)

    except IndexError as e:
        return 0

    if chrome_main_version != chromedriver_main_version:
        print("Chromedriver版本 {} 和Chrome版本 {} 不兼容,需要更新Chromedriver".format(chromedriver_version,chrome_version))
        get_chromedriver_url(chrome_version, chrome_main_version)

    else:
        print("Chromedriver版本{}和Chrome版本{}兼容，无需更新Chromedriver版本".format(chromedriver_version,chrome_version))



if __name__=='__main__':
    # get_local_chrome_version()
    # get_local_chromedriver_version()
    # get_server_chrome_versions()
    check_chromedriver()
    # get_chromedriver_url()