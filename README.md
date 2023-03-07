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
    
    from webdriver_manage.chrome import check_chromedriver
    check_chromedriver()


运行结果如下

	本机Chrome版本：110.0.5481.178
	本机ChromeDriver版本 109.0.5414.25
	Chromedriver版本 109.0.5414.25 和Chrome版本 110.0.5481.178 不兼容,开始更新Chromedriver
	Chromedriver主版本号110.0.5481.30 匹配成功, 下载地址: https://registry.npmmirror.com/-/binary/chromedriver/110.0.5481.30/chromedriver_win32.zip
	Chromedriver下载完成

## 更新记录
- 【2023-03-07】提交代码
- 【2023-03-07】支持Chrome浏览器


## 待完成的功能
- 【支持edge浏览器】
- 【支持firefox浏览器】 
- 【支持IE浏览器】
- 【下载浏览器】