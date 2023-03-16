#!/usr/bin/env python
# -*- coding:utf-8 -*-
__author__ = "Sam.huang"

from webdriver_manage.chrome import check_chromedriver
from webdriver_manage.msedge import check_msedgedriver


if __name__=='__main__':
    # check_chromedriver()  # chromedriver
    check_msedgedriver()    # msedgedriver  