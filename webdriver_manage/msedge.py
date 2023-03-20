#!/usr/bin/env python
# -*- coding:utf-8 -*-
__author__ = "Sam.huang"

from os import remove, popen
from zipfile import ZipFile
from winreg import OpenKey, QueryValueEx, HKEY_CURRENT_USER
from requests import get
from datetime import datetime
from download_webdriver import download_webdriver
import get_path



def get_local_edge_version():
    """
    通过注册表获取本机Edge浏览器版本
    return ：local_edge_version     本机安装的edge浏览器版本号
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
    用popen通过命令行查询msedgedriver版本号
    Microsoft Edge WebDriver 110.0.1587.56 (65e63b43e03b1519efb720810a66373ecd5de466)
    return：local_msedgedriver_version      返回本机安装的msedgedriver版本号
    """
    try:
        outstd = popen('msedgedriver --version').read()
       
        local_msedgedriver_version = outstd.split(' ')[3]     # 取第二个值即版本号
        print('本机MSEdgeDriver版本 {}'.format(local_msedgedriver_version))
        return local_msedgedriver_version
    
    except IndexError as e:
        # print("本机未安装MSEdgeDriver")
        return 0 

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

    # 判断是否需要更新
    if edge_main_version != msedgedriver_main_version:
        print("MSEdgeDriver版本 {} 和Edge版本 {} 不兼容,需要更新MSEdgeDriver".format(msedgedriver_version,edge_version))
        download_msedgedriver_url = f"https://msedgedriver.azureedge.net/{edge_version}/edgedriver_win32.zip"
        msedgedriver_path = get_path.get_webdriver_path('msedgedriver.exe')
        save_filename = 'edgedriver_win32.zip'
        # print(download_msedgedriver_url)
        download_webdriver(download_msedgedriver_url, save_filename, msedgedriver_path)
        get_local_msedgedriver_version()

    else:
        print("MSEdgeDriver版本{}和Edge版本{}兼容，无需更新MSEdgeDriver版本".format(msedgedriver_version,edge_version))



if __name__=='__main__':
    # get_local_edge_version()
    # get_local_msedgedriver_version()
    # download_msedgedriver()
    check_msedgedriver()
    # print(get_path.get_webdriver_path('msedgedriver.exe'))