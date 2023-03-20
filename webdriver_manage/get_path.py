#!/usr/bin/env python
# -*- coding:utf-8 -*-
__author__ = "Sam.huang"

from os import path, popen



def get_webdriver_path(webdriver_name):
    """
    获取webdriver路径
    先用popen执行windows命令拿到所有的本机PATH路径
    然后去这些路径里面遍历是否有指定文件名
    如果查询失败说明本机没有安装webdriver、那就查询Python所在路径
    webdriver_name：要查找的webdriver程序名，比如chromedriver.exe、msedgedriver.exe、geckodriver.exe
    return  webdriver_path：返回获取到的webdriver安装路径
    """
    # 通过命令行获取本机所有path路径
    try:
        out_path_dir = popen('echo %PATH%').read()
        path_dir_list = out_path_dir.split(';')

        # 遍历path路径中是否有指定文件
        for webdriver_path in path_dir_list:
            if path.exists(webdriver_path + '\{webdriver_name}'):
                return webdriver_path

                # 未找到webDriver时就安装到Python目录下
            elif path.exists(webdriver_path + '\python.exe'): 
                return webdriver_path
            else:
                pass
    except IndexError:
        pass

if  __name__=='__main__':
    print(get_webdriver_path('msedgedriver.exe'))


