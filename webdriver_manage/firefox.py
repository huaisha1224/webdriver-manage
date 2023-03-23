#!/usr/bin/env python
# -*- coding:utf-8 -*-
__author__ = "Sam.huang"

from os import popen
from winreg import OpenKey, QueryValueEx, HKEY_LOCAL_MACHINE
from download_webdriver import download_webdriver
import get_path


def get_local_firefox_version():
    """
    通过注册表获取本机FireFox浏览器版本
    return ：local_firefox_version     本机安装的FireFox浏览器版本号
    """
    try:
        # 通过注册表获取安装的firefox版本号
        key = OpenKey(HKEY_LOCAL_MACHINE, r'SOFTWARE\Mozilla\Mozilla Firefox')
        local_firefox_version, types = QueryValueEx(key, 'CurrentVersion')
        print(f'本机FireFox浏览器版本：{local_firefox_version}')
        # print(local_firefox_version.split(' ')[0])
        return local_firefox_version.split(' ')[0]  # 返回第一位数字版本号

    except WindowsError as e:
        print("未安装FireFox,请在firefox官网：https://www.mozilla.org/zh-CN/firefox/new/下载。")


def get_local_geckodriver_version():
    """
    查询系统安装的GeckoDriver版本
    用popen通过命令行查询GeckoDriver版本号
    geckodriver 0.32.2 (602aa16c20d4 2023-02-08 00:09 +0000)
    return：local_geckodriver_version      返回本机安装的GeckoDriver版本号
    """
    try:
        outstd = popen('geckodriver --version').read()

        local_geckodriver_version = outstd.split(' ')[1]     # 取第二个值即版本号
        print('本机GeckoDriver版本 {}'.format(local_geckodriver_version))
        return local_geckodriver_version

    except IndexError as e:
        # print("本机未安装GeckoDriver")
        return 0


def check_geckodriver():
    """
    判断本地FireFox版本和GeckoDriver版本是否匹配、如果不匹配就更新
    firefox_version_map：firefox浏览器和geckodriver驱动对应表
    geckodriver_version：匹配的geckodriver驱动版本号
    local_geckodriver_version：本机电脑安装的geckodriver驱动版本
    https://firefox-source-docs.mozilla.org/testing/geckodriver/Support.html firefox和geckodriver映射关系

    """

    try:
        # 判断本机FireFox版本号
        firefox_version = get_local_firefox_version()
        # firefox_main_version = int(firefox_version.split(".")[0])     # 获取FireFox主版本号
    except WindowsError as e:
        print("未安装FireFox,请在FireFox官网：https://www.mozilla.org/zh-CN/firefox/new/ 下载。")
        return 0
    # browser_version = '110.0'
    
    # Firefox版本号GeckoDriver版本号映射表
    firefox_version_map = [
        (62, '0.20.1'),
        (79, '0.24.0'),
        (90, '0.30.0'),
        (91, '0.32.2')
    ]
    # 遍历Firefox版本号和对应的geckodriver版本号
    for v in sorted(firefox_version_map, key=lambda x: x[0], reverse=True):
        # print(v)
        # 如果当前浏览器版本号大于等于Firefox版本号，则返回对应的GeckoDriver版本号
        if firefox_version.split('.') and int(firefox_version.split('.')[0]) >= v[0]:
            geckodriver_version = v[1]
            break
        else:
            geckodriver_version = 'default value'
    # print(geckodriver_version)


    try:
        # 判断本地安装的GeckoDriver版本
        local_geckodriver_version = get_local_geckodriver_version()
    except IndexError as e:
        return 0
        
    try:
        # 判断是否需要更新
        if local_geckodriver_version != geckodriver_version:
            print(f"GeckoDriver版本 {local_geckodriver_version} 和FireFox版本 {firefox_version} 不兼容,需要更新GeckoDriver")
            download_geckodriver_url = f"https://registry.npmmirror.com/-/binary/geckodriver/v{geckodriver_version}/geckodriver-v{geckodriver_version}-win32.zip"
            geckodriver_path = get_path.get_webdriver_path('geckodriver.exe')
            save_filename = f'geckodriver-v{geckodriver_version}-win32.zip'
            download_webdriver(download_geckodriver_url, save_filename, geckodriver_path)
            get_local_geckodriver_version()

        else:
            print(f"GeckoDriver版本{local_geckodriver_version}和FireFox版本{firefox_version}兼容，无需更新GeckoDriver版本")
    except:
        pass

if __name__ == '__main__':
    # print(get_local_firefox_version())
    # get_local_geckodriver_version()
    check_geckodriver()
