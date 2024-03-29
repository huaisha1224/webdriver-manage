#!/usr/bin/env python
# -*- coding:utf-8 -*-
__author__ = "Sam.huang"

from os import popen
from zipfile import ZipFile
from winreg import OpenKey, QueryValueEx, HKEY_CURRENT_USER
from requests import get
import get_path
from download_webdriver import download_webdriver


# chromedriver 淘宝源下载地址
url='https://registry.npmmirror.com/-/binary/chromedriver/' 


def get_local_chrome_version():
    """
    通过注册表获取本机Chrome版本
    return：local_chrome_version    返回本机安装的chromne版本号
    """
    try:
        # 通过注册表获取安装的Chrome版本号
        key = OpenKey(HKEY_CURRENT_USER, r'Software\Google\Chrome\BLBeacon')
        local_chrome_version, types = QueryValueEx(key, 'version')
        print(f'本机Chrome版本：{local_chrome_version}')
        return local_chrome_version
    except WindowsError as e:
        print("未安装Chrome,请在GooGle Chrome官网：https://www.google.cn/chrome/ 下载。{}".format(e))


def get_local_chromedriver_version():
    """
    查询系统安装的Chromedriver版本
    用popen通过命令行查询Chromedriver版本号
    ChromeDriver 110.0.5481.30 (aedb656755c469651f01505a4f15e153fc606a1e-refs/branch-heads/5481@{#191})
    local_chromedriver_version：返回本机安装的chromedriver版本号
    """
    local_chromedriver_version = '0'  # 设置初始值为0
    try:
        outstd = popen('chromedriver --version').read()
       
        local_chromedriver_version = outstd.split(' ')[1]     # 取第二个值即版本号
        print(f'本机ChromeDriver版本: {local_chromedriver_version}')
    
    except IndexError as e:
        print(f"本机未安装Chromedriver {e}")

    return local_chromedriver_version


def get_server_chrome_versions():
    """
    从淘宝源上获取所有的chromedriver版本信息
    version_list：返回所有的chromedriver信息
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
    通过传入的Chrome版本号进行匹配、优先匹配完版本，如果匹配不上就匹配主版本号
    chrome_version：Chrome主浏览器版本
    chrome_main_version：Chrome完整版本号
    匹配到下载地址之后调用下载模块
    """
    # chromedriver 下载地址
    download_chromedriver_url = ""
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

    # 判断Chromedriver下载地址
    if download_chromedriver_url == "":
        print(f"找不到与Chrome版本匹配的chromedriver的版本，请去 {url} 查看")
    else:
        chromedriver_path = get_path.get_webdriver_path('chromedriver.exe')
        download_webdriver(download_chromedriver_url,'chromedriver_win32.zip',chromedriver_path)
        get_local_chromedriver_version()

def get_testing_chromedriver_download_url(version):
    """
    Chrome 114版本之后Google不在提供对应的ChromeDriver
    需要从https://github.com/GoogleChromeLabs/chrome-for-testing#json-api-endpoints下载对应的版本
    """
    url = "https://googlechromelabs.github.io/chrome-for-testing/latest-versions-per-milestone-with-downloads.json"

    try:
        response = get(url)
        response.raise_for_status()
        data = response.json()

        # 查找匹配指定版本的milestone
        milestone = None
        for m in data["milestones"].values():
            if m["version"].startswith(str(version)):
                milestone = m
                break

        if milestone:
            # 获取win32平台下的Chromedriver下载地址
            for d in milestone["downloads"]["chromedriver"]:
                if d["platform"] == "win32":
                    chromedriver_testing_url = d["url"]
                    print(chromedriver_testing_url)
                    # 调用下载模块
                    chromedriver_path = get_path.get_webdriver_path('chromedriver.exe')
                    download_webdriver(chromedriver_testing_url,'chromedriver_win32.zip',chromedriver_path)
                    # return d["url"]
        return None
    
    except Exception as e:
        print(f"请求失败：{e}")
        return None

def check_chromedriver():
    """
    比较本地Chrome版本和Chromedriver版本是否匹配
    如果不匹配就调用下载更新chromedriver
    """

    try:
        # 判断本机Chrome版本号
        chrome_version = get_local_chrome_version()
        if chrome_version is None:
            print("未安装Chrome，请在Google Chrome官网：https://www.google.cn/chrome/ 下载。")
            return

        chrome_main_version = int(chrome_version.split(".")[0])     # 获取Chrome主版本号

    except WindowsError as e:
        print("获取Chrome版本号出错：{}".format(e))
        return
    
    try:
        # 判断是否安装ChromeDriver以及版本
        chromedriver_version = get_local_chromedriver_version()
        if chromedriver_version == 0:
            return

        chromedriver_main_version = int(chromedriver_version.split(".")[0]) # 获取chromedriver主版本号

    except IndexError as e:
        return 0

    # 判断是否需要更新
    if chrome_main_version != chromedriver_main_version:
        print(f"Chromedriver版本 {chromedriver_version} 和Chrome版本 {chrome_version} 不兼容，需要更新Chromedriver")
        if chrome_main_version >= 115:
            get_testing_chromedriver_download_url(chrome_main_version)
        else:
            get_chromedriver_url(chrome_version, chrome_main_version)
    else:
        print(f"Chromedriver版本 {chromedriver_version} 和Chrome版本 {chrome_version} 兼容，无需更新Chromedriver版本")


if __name__=='__main__':
    # get_local_chrome_version()
    # get_local_chromedriver_version()
    # get_server_chrome_versions()
    check_chromedriver()
    # download_url = get_testing_chromedriver_download_url('116')
    # print(download_url)