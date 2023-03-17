#!/usr/bin/env python
# -*- coding:utf-8 -*-
__author__ = "Sam.huang"

from os import remove
from zipfile import ZipFile
from requests import get
from tqdm import tqdm
from datetime import datetime


def download_webdriver(download_webdriver_url, save_filename, save_webdriver_path):
    """
    下载WebDriver、并解压到指定目录
    """

     # 用流stream的方式获取url的数据
    resp = get(download_webdriver_url, stream=True)

    # 拿到文件的长度，并把total初始化为0
    total = int(resp.headers.get('content-lenght', 0))

    # 初始化tqdm，传入总数，文件名等数据，接着就是写入，更新等操作
    with open(save_filename, "wb") as zip_file, tqdm(
        desc = '下载中',
        total = total,
        ncols= 100,
        unit = "iB",
        leave= True,
        unit_scale = True,
        unit_divisor = 1024) as bar:
        for data in resp.iter_content(chunk_size=1024):
            size = zip_file.write(data)
            bar.update(size)

    # 解压文件到WebDriver Path路径下
    msedgedriver_file = ZipFile(save_filename, "r")
    for file in msedgedriver_file.namelist():
        if save_webdriver_path != None:
            msedgedriver_file.extract(file, save_webdriver_path)
        else:
            pass
    msedgedriver_file.close()
    remove(save_filename)
    print(f"{save_filename}文件替换到 {save_webdriver_path} 成功。")



if __name__=='__main__':
    download_webdriver_url = f"https://msedgedriver.azureedge.net/111.0.1661.43/edgedriver_win32.zip"
    save_filename = 'edgedriver_win32.zip'
    save_webdriver_path= 'D:\\Python38\\'
    download_webdriver(download_webdriver_url, save_filename, save_webdriver_path)