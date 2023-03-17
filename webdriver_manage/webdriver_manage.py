#!/usr/bin/env python
# -*- coding:utf-8 -*-
__author__ = "Sam.huang"

from chrome import check_chromedriver
from msedge import check_msedgedriver


if __name__=='__main__':
    check_chromedriver()  # chromedriver
    # msedge.check_msedgedriver()    # msedgedriver 