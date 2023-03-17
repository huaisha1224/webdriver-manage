# WebDriver-Manage
[![version](https://img.shields.io/badge/python-3.4+-blue.svg)](https://www.python.org/download/releases/3.4.0/) 
[![status](https://img.shields.io/badge/status-stable-green.svg)](https://github.com/huaisha1224/webdriver-manage)
[![license](https://img.shields.io/badge/license-MIT-blue.svg)](./LICENSE)
[![star, issue](https://img.shields.io/badge/star%2C%20issue-welcome-brightgreen.svg)](https://github.com/huaisha1224/webdriver-manage)

管理Selenium所需的WebDriver,自动匹配浏览器版本并更新合适版本的webdriver驱动程序.

## 主要功能

-	查询本地浏览器版本
-	查询本地安装的webdriver版本
-	判断webdriver和浏览器版本是否匹配，不匹配时自动更新合适的webdriver


## 简单使用
    
    from chrome import check_chromedriver
	from msedge import check_msedgedriver
    
	check_chromedriver()


运行结果如下

	本机Chrome版本：111.0.5563.65
	本机ChromeDriver版本 110.0.5481.30
	Chromedriver版本 110.0.5481.30 和Chrome版本 111.0.5563.65 不兼容,需要更新Chromedriver
	Chromedriver主版本号111.0.5563.19 匹配成功, 开始更新
	下载中: 6.79MiB [00:00, 9.22MiB/s]
	chromedriver_win32.zip文件替换到 D:\Python38\ 成功。
	本机ChromeDriver版本 111.0.5563.19

## 更新记录
- 【2023-03-07】提交代码
- 【2023-03-07】支持Chrome浏览器
- 【2023-03-11】未安装chromedriver时下载chromedriver文件到Python的PATH目录中
- 【2023-03-16】支持Edge浏览器


## 待完成的功能
- 【✔】支持Chrome浏览器
- 【✔】支持edge浏览器
- 【  】支持firefox浏览器 
- 【  】支持IE浏览器
- 【  】下载浏览器