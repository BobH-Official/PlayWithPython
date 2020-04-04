#!/usr/local/bin/python3
# -*- coding: UTF-8 -*-
#
#  bingWallpapers.py
#  https://github.com/unouprimeOder/PlayWithPython
#  https://github.com/unouprimeOder/PlayWithPython/blob/master/Proj-1/bingWallpapers.py
#
#  Created by unouprimeOder on 20200125.
#  Copyright © 2020 unouprimeOder. All rights reserved.
#

import requests
from lxml import etree
import random
import time
import os

# MARK: - Root Path
root = os.getcwd() + '/'

# MARK: - Logs
# MARK: Log
logPath = root + 'log.txt'
log = open(logPath, 'a')
# 开头写一些分隔符
log.write('#############################################\n')
log.write(time.strftime('%Y-%m-%d %a. %H:%M:%S', time.localtime(time.time())))
log.write('\n')
log.write('#############################################\n')
# MARK: Save Log


def logprint(text):
    print(text)
    log.write(text + '\n')

# MARK: - Get Page HTML


def getPageHTML(url, triedNum=0, sleepTime=5, tryNum=20):
    logprint('>>>>正在访问: {}'.format(url))
    # 获取页面
    data = requests.get(url)
    # 处理状态
    statusCode = data.status_code
    if not statusCode == 200:
        data = 'timeout'
        # 递归，尝试多次
        if triedNum <= tryNum:
            logprint('>>>>休息 {} 秒'.format(sleepTime))
            time.sleep(sleepTime)
            logprint('>>>>重新访问: '+url+' : '+str(triedNum))
            triedNum = triedNum + 1
            getPageHTML(url=url, triedNum=triedNum, tryNum=tryNum)
        else:
            logprint('>>>>尝试 {} 次无效'.format(tryNum))
    return data

# MARK: - Get Info
# MARK:  Get Picture URL


def getInfoUrl(page):
    logprint('>>>>正在获取URL信息')
    data = page
    selector = etree.HTML(data.text)
    returnData = selector.xpath('/html/body/div[3]/div/div/img/@src')
    return returnData
# MARK:  Get Picture Name


def getInfoName(page):
    logprint('>>>>正在获取NAME信息')
    data = page
    selector = etree.HTML(data.text)
    returnData = selector.xpath('/html/body/div[3]/div/div/div[1]/h3/text()')
    return returnData
# MARK:  Get Picture Date


def getInfoDate(page):
    logprint('>>>>正在获取DATE信息')
    data = page
    selector = etree.HTML(data.text)
    returnData = selector.xpath(
        '/html/body/div[3]/div/div/div[1]/p[1]/em/text()')
    return returnData

# MARK: - Save Image


def saveImage(imgUrl, path, imgName):
    if not os.path.exists(path):  # 判断文件夹是否已经存在
        os.makedirs(path)
    imgPath = path + imgName
    if not os.path.exists(imgPath):  # 判断文件是否已经存在
        img = requests.get(imgUrl).content  # 获取文件的二进制编码
        file = open(imgPath, "wb")  # 用二进制模式打开
        file.write(img)  # 直接写入二进制文件
        logprint('>>>>file #' + imgName + ' written')
    else:
        logprint('>>>>file #' + imgName + ' already exists')


#########MAIN STARTS HERE#########
# MARK: - MAIN STARTS HERE -
#########MAIN STARTS HERE#########

# MARK:  Start
logprint('@@@@@@START@@@@@@')
print(time.strftime('%Y-%m-%d %a. %H:%M:%S', time.localtime(time.time())))

for i in range(1, 121):
    # 创建当前页面URL
    url = 'https://bing.ioliu.cn/?p={}'.format(i)
    # 获取页面
    page = getPageHTML(url)
    # 判断是不是timeout
    if page == 'timeout':
        logprint(
            '>>>>!!!!!!!BROKEN!!!!!!!\n>>>>{}\n>>>>!!!!!!!BROKEN!!!!!!!'.format(url))
        logprint(time.strftime('%Y-%m-%d %a. %H:%M:%S',
                               time.localtime(time.time())))
    else:
        # 获取页面信息
        dataUrl = getInfoUrl(page)
        dataName = getInfoName(page)
        dataDate = getInfoDate(page)
        # 依次获取12张图片
        for s in range(0, 12):
            # 读取图片信息
            imgUrl = dataUrl[s]
            name = dataDate[s] + '_[' + dataName[s] + '].jpeg'
            # 处理名字里的不合法字符
            imgName = ''
            for x in name:
                if not x == '/' and not x == '©':
                    imgName = imgName + x
                elif x == '/':
                    imgName = imgName + '\\'
                elif x == '©':
                    imgName = imgName + '(c)'
            # 保存图片
            logprint('>>>>获取 #第 {} 页__第 {} 张'.format(i, s))
            saveImage(imgUrl=imgUrl, path=root + 'IMG/', imgName=imgName)
            # 休息 5 秒
            logprint('>>>>休息 5 秒')
            time.sleep(5)

# MARK:  OVER
logprint(time.strftime('%Y-%m-%d %a. %H:%M:%S', time.localtime(time.time())))
logprint('@@@@@@OVER@@@@@@')
