#! /usr/local/bin/python3
import requests
from lxml import etree
import random
import time
import os
from selenium import webdriver


header = {
    'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 11_0_1 like Mac OS X) AppleWebKit/604.1.38 (KHTML, like Gecko) Version/11.0 Mobile/15A402 Safari/604.1'}

root = os.getcwd() + '/'  # 这里加上’/‘是为了后面方便

logPath = root + 'bilibili/log.txt'
log = open(logPath, "a")
log.write('\n')

brokenLogPath = root + 'bilibili/bilibiliBrokenLog.txt'
brokenLog = open(brokenLogPath, "a")
brokenLog.write('\n')
brokenLog.write('@@@@@@START@@@@@@\n')


def logprint(text=''):
    print(text)
    log.write(text+'\n')


pageLogPath = root + 'bilibili/bilibiliPageLog.txt'
pageLog = open(pageLogPath, "w")
pageLog.write('\n')
pageLog.write('@@@@@@START@@@@@@\n')


def getPage(url, driver, tryNum=0):
    print('>>>>正在访问: {}'.format(url))
    driver.get(url)
    logprint(">>>>睡 5 秒")
    time.sleep(5)
    data = driver.page_source
    dataInfo = etree.HTML(data)
    is404 = dataInfo.xpath('/html/body/div[3]/img/@class')
    logprint(">>>>得到 #{}".format(url))
    if is404 == ['img-404']:
        data = 'timeout'
        if tryNum <= 20:
            logprint('>>>>休息10s')
            time.sleep(10)
            logprint('>>>>重新访问: '+url+' : '+str(tryNum))
            tryNum = tryNum + 1
            getPage(url=url, driver=driver, tryNum=tryNum)
        else:
            logprint('>>>>尝试20次无效')
    return data


def getInfo(url, driver, tryNum=0):
    logprint('>>>>正在获取页面信息')
    data = getPage(url=url, driver=driver)
    if data == 'timeout':
        logprint('data of getinfo is timeout')
        imgURL = 'timeout'
        pageNum = 404
        pageName = 'timeout'
    else:
        selector = etree.HTML(data)
        imgURL = selector.xpath('//*[@id="cp_image"]/@src')
        if imgURL == []:
            if tryNum <= 20:
                logprint('>>>>重新获取页面: '+url+' : '+str(tryNum))
                tryNum = tryNum + 1
                imgURL = 'timeout'
                getInfo(url=url, driver=driver, tryNum=tryNum)
            else:
                logprint('>>>>尝试 20 次无效')
                imgURL = 'timeout'
                pageNum = 404
                pageName = 'timeout'
                saveBrokenLog(url)
        else:
            imgURL = imgURL[0]
        pageNum = selector.xpath('//*[@id="lbcurrentpage"]/text()')[0]
        pageNum = int(pageNum)
        pageName = selector.xpath('/html/body/div[1]/div/div/p/text()')[0]
        pageName.replace('\s', '')
        abcd = ''
        for i in pageName:
            if not i == '\t':
                if not i == ' ':
                    abcd += i
        pageName = abcd
        logprint('>>>> #' + str(pageNum))
        logprint('>>>> #' + pageName)
        logprint('>>>> #' + imgURL)
    return [pageNum, imgURL, pageName]


def getAllPages(driver):
    url = 'http://www.mangabz.com/287bz/'
    data = getPage(url=url, driver=driver)
    if not data == 'timeout':
        selector = etree.HTML(data)
        urls = selector.xpath('/html/body/div[5]/div[2]/a/@href')
        names = selector.xpath('/html/body/div[5]/div[2]/a/text()')
        pagenums = selector.xpath('/html/body/div[5]/div[2]/a/span/text()')
        nums = []
        returnData = []

        count = 0
        for s in pagenums:
            a = ''
            count += 1
            for i in s:
                if i == '1' or i == '2' or i == '3' or i == '4' or i == '5' or i == '6' or i == '7' or i == '8' or i == '9' or i == '0':
                    a += i
            a = int(a)
            nums.append(a)
        for i in range(count + 1):
            i = i - 1
            pageLog.write('>>>>>>>>>>>>>>>>>>>>\n')
            pageLog.write('####' + str(i+1)+names[i]+urls[i]+str(nums[i])+'\n')
            pageLog.write('\n')
            returnData.append([i + 1, names[i], urls[i], nums[i]])
            # name is a string, url is a string, nums is a int which refers to how many pages this chapter got, the first one is the chapter's id
    else:
        returnData = ['timeout']
    return(returnData)


def saveImage(imgUrl, path, name):
    img = requests.get(imgUrl, headers=header)
    img = img.content
    file = open(path, "wb")
    file.write(img)
    logprint('>>>>file #'+name + 'written>>>>>>>')


def saveBrokenLog(url, chapterNum=-1, pageNum=-1, chapterName=''):
    logprint('>>>>存入 bilibiliBrokenLog.txt')
    logprint(
        '!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!\n')
    brokenLog.write(
        '--------------------------------------------------------------------------------\n')
    brokenLog.write(
        '--------------------------------------------------------------------------------\n')
    if not chapterNum == -1 and not chapterName == '':
        brokenLog.writelines(
            '>>>>>>>> #' + str(chapterNum) + ' #' + chapterName)
    if not pageNum == -1:
        brokenLog.writelines('>>>>>>>> #'+str(pageNum))
    brokenLog.writelines('>>>>>>>> #' + url)
    brokenLog.write(
        '--------------------------------------------------------------------------------\n')
    brokenLog.write(
        '--------------------------------------------------------------------------------\n')
    brokenLog.write('\n')
    brokenLog.write('\n')


#########MAIN STARTS HERE#########
driver = webdriver.Firefox(
    executable_path='/usr/local/bin/drivers/geckodriver_0_26_0')
logprint('@@@@@@START@@@@@@')
allChapter = getAllPages(driver=driver)
URL_b = 'http://www.mangabz.com/'
if allChapter == ['timeout']:
    saveBrokenLog(url='none is got')
else:
    # get the chapter
    for ss in range(0, 5):
        currentChapter = allChapter[ss]
        chapterURLhref = currentChapter[2]
        chapterURL = ''
        for i in chapterURLhref:
            if not i == '/':
                chapterURL += i
        chapterTotalPages = currentChapter[3]
        chapterName = currentChapter[1]
        chapterNum = currentChapter[0]
        # get single page
        for currentPageIndex in range(chapterTotalPages):
            currentPageIndex += 1
            currentPageURL = URL_b + chapterURL + \
                '/#ipg{}'.format(currentPageIndex)
            logprint('######## '+str(currentPageIndex)+'  '+currentPageURL)
            info = getInfo(currentPageURL, driver)
            currentImgURL = info[1]
            currentImgNum = info[0]
            currentImgName = info[2]
            logprint('>>>>当前章名: #' + currentImgName)
            logprint('>>>>当前页数: #' + str(currentImgNum))
            logprint('>>>>当前URL: #' + str(currentImgURL))
            if currentImgURL == 'timeout':
                logprint('>>>>获取页面失败')
                saveBrokenLog(currentImgURL, chapterNum, currentPageIndex, currentImgName)
            else:
                chapterRootPath = root + 'bilibili/content/' + str(chapterNum) + '-' + currentImgName+'/'
                if not os.path.exists(root + 'bilibili/'):
                    os.mkdir(root + 'bilibili/')
                if not os.path.exists(root + 'bilibili/content/'):
                    os.mkdir(root + 'bilibili/content/')
                if not os.path.exists(chapterRootPath):
                    os.mkdir(chapterRootPath)
                    logprint('>>>>章节路径: #{} 创建好了'.format(chapterRootPath))
                if currentPageIndex == currentImgNum:
                    logprint('>>>>序号是一致的')
                else:
                    logprint('>>>>序号不一致')
                fileName = str(chapterNum) + '-' + str(currentImgName) + '_p_' + str(currentPageIndex)+'.jpeg'
                imgPath = chapterRootPath + fileName
                if os.path.exists(imgPath):
                    logprint('>>>>file #{} already existed'.format(fileName))
                else:
                    saveImage(currentImgURL, imgPath, fileName)
        logprint('--------------------------------------------------------------------------------')
        logprint('--------------------------------------------------------------------------------')
        logprint('######NEXT######')
        logprint('--------------------------------------------------------------------------------')
driver.close()
brokenLog.write('@@@@@@OVER@@@@@@')
logprint('@@@@@@OVER@@@@@@')
