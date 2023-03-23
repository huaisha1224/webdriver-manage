#!/usr/bin/env python
# -*- coding:utf-8 -*-
__author__ = "Sam.huang"

from chrome import check_chromedriver
from msedge import check_msedgedriver
from firefox import check_geckodriver


if __name__=='__main__':
    check_chromedriver()  # chromedriver
    # check_msedgedriver()    # msedgedriver 
    # check_geckodriver()