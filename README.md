# 高一寒假的研究性学习

当今，互联网已经将全世界十亿个人计算机用户联结在了一起。我们为了更加了解互联网的组成与功能，这个寒假，（也有疫情只能呆在家中的缘故），我们打算初步探究互联网前端网页的自动化操作的实现。为了研究的趣味性与实用性，我们选择从最近很火的“爬虫”入手，进行我们的研究。

# 严正声明

本次研究性学习的一切内容仅供用于学习交流，严禁用于商业用途。

文章以 CC BY-NA-SA 共享，代码以 MIT License 开源。

-------

# 正文开始了

# 研究目的

初步了解互联网爬虫，感受计算机带来的便捷操作。

# 研究方式、步骤

使用Python爬虫，依次对1. 静态网页2. 动态网页 进行“图片”爬取。

使用Swift程序，对爬取的图片进行处理。

1. 爬取一个“Bing必应壁纸大全”网页
2. 爬取一个“漫画网页”
3. 对爬取的图片进行简单的整理并提高画质

# Get Started

### 环境

电脑：

> MacBook Pro (13-inch, 2017, Four Thunderbolt 3 Ports)
>
> 3.1 GHz 双核Intel Core i5
>
> 8 GB 2133 MHz LPDDR3
>
> Intel Iris Plus Graphics 650 1536 MB
>

系统：

> macOS Catalina(10.15.3)

编译环境：

> Python 3.8.0 (v3.8.0:fa919fdf25, Oct 14 2019, 10:23:27) 
>
> [Clang 6.0 (clang-600.0.57)] on darwin

### 下载Xcode

从 App Store 上下载Xcode即可。

### 安装Python

从官网上下载：

<a href="https://www.python.org/downloads/">https://www.python.org/downloads/</a>

> 下载最新版 `python3` 就好，⚠️注意 `python3` 和 `python2` 不一样，本文全部使用 `python3` 。（注：macOS自带`python2`，但也不是最新版）

<img src="./img/img_python_download.png" style="zoom:60%;" />

### 安装库

使用`pip3`，不要用`pip`。`pip3`安装`Python3`才读得到。

> `python3` 自带了`pip3`，不用在另外下载。

```
# Proj-1
$ pip3 install lxml
$ pip3 install requests
$ pip3 install selenium
```



# Proj-1：Python 图片爬虫

## 开始准备

我们在网上找了一下这个网站上有许多Bing的图片，很集中，很适合自动化操作。

### 爬取的内容

[https://bing.ioliu.cn/](https://bing.ioliu.cn/) 网站上的必应壁纸

然后我们在网上又找了一下（网上寻找资料的过程太冗长了，最近一段时间“爬虫”、“Python”都是热门话题，搜出来好多是广告。所以，具体的过程就不细说了），找到了我们需要用到的“Python 库”（理解为一些开箱即用的“工具包“就行了）

### 使用的库

就是一些别人写好的工具包啦，”不重复造轮子“是基本素养。

1. etree from lxml（分析HTML）
2. requests（获取数据）

## 分析网页

点开网页的检查器，我们能够发现一大堆“HTML源码”，这些HTML描述了网页的骨架、即网页基本长什么样子（具体的一些东西得让CSS（Cascading Style Sheets 层叠样式表）去描述）。

HTML，全称呢Hypertext Markup Language，超文本标记语言。使用的语法结构和XML（Extensible Markup Language可扩展标记语言）很相像（毕竟它们互相学习、一起发展），即是由一个一个标签组成的。

为了让计算机知道我们要的标签在哪里，我们通过标签的父子关系来确定标签的位置，即使用“XPath”来确定位置。

具体的Xpath内容便不细说了，我们只需要知道我们要的元素的Xpath是什么就行了，然而浏览器为我们提供了便利的方法：**`右键 ⇒ 'Copy' ⇒ 'Copy XPath'`**

<img src="./Proj-1/img/img_copy_xpath.png"/>

那么我们正式开始对网页进行分析。

首先是页面。

### 页面

第1页：[https://bing.ioliu.cn/?p=1](https://bing.ioliu.cn/?p=1)

第2页：[https://bing.ioliu.cn/?p=2](https://bing.ioliu.cn/?p=2)

第3页：[https://bing.ioliu.cn/?p=3](https://bing.ioliu.cn/?p=3)

我们可以看到，翻页的方式是通过 `?p=` 给的参数，一共120页。

```python
for i in range(1,121):
    urls = 'https://bing.ioliu.cn/?p={}'.format(i)
```

### 图片链接、名称及版权、日期

##### 版权信息是很重要的，我们在下载后，将版权信息加在文件名之后

<img src="./Proj-1/img/img_xpath_of_pic_url.png" />

这个时候我们可以引用一句数学老师们最讨厌的话：

> 由图知：

```python
xpath_1 = '/html/body/div[3]/div[1]/div/img'
url_1 = '/html/body/div[3]/div[1]/div/img/@src'

xpath_2 = '/html/body/div[3]/div[2]/div/img'
url_2 = '/html/body/div[3]/div[2]/div/img/@src'

xpath_3 = '/html/body/div[3]/div[3]/div/img'
url_3 = '/html/body/div[3]/div[3]/div/img/@src'
```

可以看出，第二个`<div>` 的 Index 是迭代的。

> 因此：

```python
xpath_of_pictures = '/html/body/div[3]/div/div/img'
url_of_pictures = '/html/body/div[3]/div/div/img/@src'
```

再看其他内容的XPath：

<img src="./Proj-1/img/img_xpath_of_pic_name_and_copyright.png"/>

<img src="./Proj-1/img/img_xpath_of_pic_date.png"/>

这时我们再引用一句学生们们最喜欢的话：

> 同理可得：

```python
xpath_of_name = '/html/body/div[3]/div/div/div[1]/h3/text()'
xpath_of_date = '/html/body/div[3]/div/div/div[1]/p[1]/em/text()'
```

------



## 开始CODE

终于到上代码的时间了！🎉

### 首先，我们来一点<code>import</code>：

```python
import requests # 获取文件
from lxml import etree # 分析HTML
import time # 用于暂停一段时间
import os # 调用系统功能
```

### 获取当前工作路径，用于保存文件：

```python
root = os.getcwd() + '/'  # 这里加上’/‘是为了后面方便
```

> 手动储存log，我喜欢这么做，方便日后查看失败的请求
>```python
>logPath = root + 'log.txt'
>log = open(logPath, 'a') # 我用续写模式，也可也用'w'
># 开头写一些分隔符
>log.write('#############################################\n')# 
>log.write(time.strftime('%Y-%m-%d %a. %H:%M:%S',time.localtime(time.time()))) # 写入时间
>log.write('#############################################\n')
>
>def logprint(text):
>print(text)
>log.write(text + '\n')
>```

### 主体代码

```python
for i in range(1, 121):
    # 创建当前页面URL
    url = 'https://bing.ioliu.cn/?p={}'.format(i)
    # 获取页面
    page = getPageHTML(url)
    # 判断是不是timeout//函数抛出'timeout'
    if page == 'timeout':
        logprint('>>>>!!!!!!!BROKEN!!!!!!!\n>>>>{}\n>>>>{}\n>>>>!!!!!!!BROKEN!!!!!!!'.format(url, time.strftime('%Y-%m-%d %a. %H:%M:%S',time.localtime(time.time()))))
    else:
        # 获取页面信息
        dataUrl = getInfoUrl(page) # get a string
        dataName = getInfoName(page) # get a list
        dataDate = getInfoDate(page) # get a list
        #依次获取12张图片
        for s in range(0, 12):
            # 读取图片信息
            imgUrl = dataUrl[s]
            imgName = dataDate[s] + '_[' + dataName[s] + '].jpeg'
            # 保存图片
            logprint('>>>>获取 #第 {} 页__第 {} 张'.format(i, s))
            saveImage(imgUrl=imgUrl, path = root + 'IMG/', imgName = imgName)
            # 休息 5 秒
            logprint('>>>>休息 5 秒')
            time.sleep(5)
```

### 一些函数

```python
# MARK: - Get Page HTML
def getPageHTML(url, triedNum=0, sleepTime=5, tryNum=20):
    logprint('>>>>正在访问: {}'.format(url))
    # 获取页面
    data = requests.get(url)
    # 处理状态
    statusCode = data.status_code
    if not statusCode == 200:
        data = 'timeout'
        # 不要放弃，再试几次，我设置的20次，可以在参数设置
        if triedNum <= tryNum:
            logprint('>>>>休息 {} 秒'.format(sleepTime))
            time.sleep(sleepTime)
            logprint('>>>>重新访问: '+url+' : '+str(triedNum))
            triedNum = triedNum + 1
            getPageHTML(url=url, triedNum=triedNum, tryNum=tryNum)
        else:
            logprint('>>>>尝试 {} 次无效'.format(tryNum))
    return data
```

```python
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
    returnData = selector.xpath('/html/body/div[3]/div/div/div[1]/p[1]/em/text()')
    return returnData
######################
# 注意XPath，把递归的部分删去，etree 会自己递归，然后返回一个list
# 后面两个分开写了，这样清楚一些
```

```python
# MARK: - Save Image
def saveImage(imgUrl, path, imgName):
    if not os.path.exists(path):  # 判断文件夹是否已经存在
        os.makedirs(path)
    imgPath = path + imgName
    if not os.path.exists(imgPath):  # 判断文件是否已经存在
        img = requests.get(imgUrl).content # 获取文件的二进制编码
        file = open(imgPath, "wb") # 用二进制模式打开
        file.write(img) # 直接写入二进制文件
        logprint('>>>>file #' + imgName + ' written')
    else:
        logprint('>>>>file #' + imgName + ' already exists')
```

理论上，这就应该能跑了。

可是现实是残酷的。

仔细观察发现，copyright 里面竟然有个`/`。去访达里看看，会发现一个神奇的事情，<img src="./Proj-1/img/img_slash.png" style="zoom:35%;" /> ，访达怎么会支持这种东东！？

在`Terminal`里面`ls`看一下，它原来长这样`./bing:wallpapers.py`，再去访达里把文件命名为`:`，你会神奇的发现这是非法操作。

为了方便，于是我们干脆把正斜杠`/`换成反斜杠`\`，顺便把`©`换成`(c)`：

```python
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
```



# Proj-2：爬取动态网页

由于没有找到其他特别好的网站，只好使用一个动画网站。**我们支持正版，保护作者权利。以下代码仅用于学习目的**

### 爬取网页

“http://www.mangabz.com/287bz/” 的其中几话。

## 分析网页

第一页是目录，是一张静态网页。

然而到了漫画页面是动态加载的。

对于动态页面，一般来说有两种处理方式：

1. 爬取网页后，加载有关 JavaScript 文件；
2. 动态加载完所有内容后，再爬取网页。

后者明显是简单方法，虽然是慢了一点点。

### 使用的库

1. etree from lxml（分析HTML）
2. requests（获取数据）
3. webdriver from selenium（网页自动化操作工具，可以直接调用浏览器，以达到自动加载的目的）

### 目录页面

<img src="./Proj-2/images/img_content.png" />

我们需要获取每一话的“链接”、“名称”、“页数”。

```python
xpath_url = '/html/body/div[5]/div[2]/a/@href')
xpath_names = '/html/body/div[5]/div[2]/a/text()')
xpath_pagenums = '/html/body/div[5]/div[2]/a/span/text()')
```

### 漫画页面

<img src="./Proj-2/images/img_hua.png" />

 我们需要取得当前`page`的“页数”、“名称”、和当前图片的“URL”

```python
xpath_img = '//*[@id="cp_image"]/@src'
xpath_pageNum = '//*[@id="lbcurrentpage"]/text()'
xpath_pageName = '/html/body/div[1]/div/div/p/text()'
```

每一张的翻页的实现：

第1页：<a href="http://www.mangabz.com/m21739/#ipg1" >http://www.mangabz.com/m21739/#ipg1</a>

第2页：<a href="http://www.mangabz.com/m21739/#ipg2" >http://www.mangabz.com/m21739/#ipg2</a>

第3页：<a href="http://www.mangabz.com/m21739/#ipg3" >http://www.mangabz.com/m21739/#ipg3</a>

我们可以看到，翻页的方式是通过 `#ipg?` 给的参数，一共`chapterTotalPages`页。

```python
for currentPageIndex in range(chapterTotalPages):
    currentPageURL = 'http://www.mangabz.com/' + chapterURL + '/#ipg{}'.format(currentPageIndex)
```

------

## 开始CODE

终于到上代码的时间了！🎉

首先，我们来一点<code>import</code>：

```python
import requests # 获取文件
from lxml import etree # 分析HTML
import time # 用于暂停一段时间
import random # 随机数生成
import os # 调用系统功能
from selenium import webdriver # 自动操作工具webdriver
```
#### 获取当前工作路径，用于保存文件：

```python
root = os.getcwd() + '/'  # 这里加上’/‘是为了后面方便
if not os.path.exists(root + 'bilibili/'):
    os.mkdir(root + 'bilibili/')
if not os.path.exists(root + 'bilibili/content/'):
    os.mkdir(root + 'bilibili/content/')
```

> 手动储存log，我喜欢这么做，方便日后查看失败的请求
> ```python
> logPath = root + 'log.txt'
> log = open(logPath, 'a') # 我用续写模式，也可也用'w'
> # 开头写一些分隔符
> log.write('#############################################\n')# 
> log.write(time.strftime('%Y-%m-%d %a. %H:%M:%S',time.localtime(time.time()))) # 写入时间
> log.write('#############################################\n')
> 
> def logprint(text):
> 	print(text)
> 	log.write(text + '\n')
> 
> #储存错误
> brokenLogPath = root + 'bilibili/bilibiliBrokenLog.txt'
> brokenLog = open(brokenLogPath, "a")
> brokenLog.write('\n')
> brokenLog.write('@@@@@@START@@@@@@\n')
> def saveBrokenLog(url, chapterNum=-1, pageNum=-1, chapterName=''):
>     logprint('>>>>存入 bilibiliBrokenLog.txt')
>     logprint('!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!\n')
>     brokenLog.write('--------------------------------------------------------------------------------\n')
>     brokenLog.write('--------------------------------------------------------------------------------\n')
>     if not chapterNum == -1 and not chapterName == '':
>         brokenLog.writelines(
>             '>>>>>>>> #' + str(chapterNum) + ' #' + chapterName)
>     if not pageNum == -1:
>         brokenLog.writelines('>>>>>>>> #'+str(pageNum))
>     brokenLog.writelines('>>>>>>>> #' + url)
>     brokenLog.write('--------------------------------------------------------------------------------\n')
>     brokenLog.write('--------------------------------------------------------------------------------\n')
>     brokenLog.write('\n')
>     brokenLog.write('\n')
> 
> #储存获取的每一页的数据
> pageLogPath = root + 'bilibili/bilibiliPageLog.txt'
> pageLog = open(pageLogPath, "w")
> pageLog.write('\n')
> pageLog.write('@@@@@@START@@@@@@\n')
> ```

#### 主体代码，主要的逻辑部分
“话” 我用 “chapter（章节）”来代替

```python
# 打开webdriver，这里用的是FireFox（也推荐使用Safari）
driver = webdriver.Firefox(executable_path='path/to/your/geckodriver')
# 开始
logprint('@@@@@@START@@@@@@')
# 获取目录里的全部页面信息，返回的是一个list嵌套的list
allChapter = getAllPages(driver=driver)
# 准备基础的URL
URL_b = 'http://www.mangabz.com/'
# 判断是否有返回
if allChapter == ['timeout']:
    saveBrokenLog(url='none is got')
else:
    # 获取每一话（chapter）
    for ss in range(0, 5): # 象征性的只获取 5 个
        currentChapter = allChapter[ss]
        # 处理这一话的URL
        chapterURLhref = currentChapter[2]
        chapterURL = ''
        # 要把多余的'/'删去，没有在获取的时候删是为了函数里的代码更清晰一点
        for i in chapterURLhref:
            if not i == '/':
                chapterURL += i
        # 获取其他信息
        chapterTotalPages = currentChapter[3] # 总页数
        chapterName = currentChapter[1] # 话名称
        chapterNum = currentChapter[0] # 话的编号
        # 获取每一个单页
        for currentPageIndex in range(chapterTotalPages):
            currentPageIndex += 1 # list是从0开始的，所以这里要转换一下
            # 当前“页”的URL
            currentPageURL = URL_b + chapterURL + '/#ipg{}'.format(currentPageIndex)
            logprint('######## '+str(currentPageIndex)+'  '+currentPageURL)
            # 获取当前“页”的信息
            info = getInfo(currentPageURL, driver)
            currentImgURL = info[1]
            currentImgNum = info[0]
            currentImgName = info[2]
            # 打印每一页的数据
            logprint('>>>>当前章名: #' + currentImgName)
            logprint('>>>>当前页数: #' + str(currentImgNum))
            logprint('>>>>当前URL: #' + str(currentImgURL))
            if currentImgURL == 'timeout':
                logprint('>>>>获取页面失败')
                saveBrokenLog(currentImgURL, chapterNum, currentPageIndex, currentImgName)
            else:
                # 储存路径的创立
                chapterRootPath = root + 'bilibili/content/' + str(chapterNum) + '-' + currentImgName+'/'
                if not os.path.exists(chapterRootPath):
                    os.mkdir(chapterRootPath)
                    logprint('>>>>章节路径: #{} 创建好了'.format(chapterRootPath))
                # 判断是编号是否一致，以免错误的出现
                if currentPageIndex == currentImgNum:
                    logprint('>>>>序号是一致的')
                else:
                    logprint('>>>>序号不一致')
                # 文件路径
                fileName = str(chapterNum) + '-' + str(currentImgName) + '_p_' + str(currentPageIndex)+'.jpeg'
                imgPath = chapterRootPath + fileName
                # 是否已经存在，不要重复获取
                if os.path.exists(imgPath):
                    logprint('>>>>file #{} already existed'.format(fileName))
                else:
                    # 获取图片
                    saveImage(currentImgURL, imgPath, fileName)
        # 下一话
        logprint('--------------------------------------------------------------------------------')
        logprint('--------------------------------------------------------------------------------')
        logprint('######NEXT######')
        logprint('--------------------------------------------------------------------------------')
# 结束了，退出
driver.close()
brokenLog.write('@@@@@@OVER@@@@@@')
logprint('@@@@@@OVER@@@@@@')
```

#### 一些函数
##### 获取页面

```python
def getPage(url, driver, tryNum=0):
    print('>>>>正在访问: {}'.format(url))
    # 这里我们用到了webdriver
    driver.get(url)
    # 等待动态加载，网速不好的可以等的时间长一点
    logprint(">>>>睡 5 秒")
    time.sleep(5)
    data = driver.page_source
    dataInfo = etree.HTML(data)
    # 这里是判断是否是404，由于用了webdriver，手动判断会方便一点
    is404 = dataInfo.xpath('/html/body/div[3]/img/@class')
    logprint(">>>>得到 #{}".format(url))
    if is404 == ['img-404']:
        data = 'timeout'
        # 尝试 20 次
        if tryNum <= 20:
            logprint('>>>>休息10s')
            time.sleep(10)
            logprint('>>>>重新访问: '+url+' : '+str(tryNum))
            tryNum = tryNum + 1
            getPage(url=url, driver=driver, tryNum=tryNum) # 这里有个迭代
        else:
            logprint('>>>>尝试20次无效')
    return data # driver.page_source，或'timeout'（我全部使用字符串'timeout'来进行错误处理，方便一点）
```

##### 获取全部页面信息

```python
def getAllPages(driver):
    url = 'http://www.mangabz.com/287bz/' # 写死的
    data = getPage(url=url, driver=driver)
    # 进行错误判断
    if not data == 'timeout':
        把数据交给etree
        selector = etree.HTML(data)
        获取信息
        urls = selector.xpath('/html/body/div[5]/div[2]/a/@href')
        names = selector.xpath('/html/body/div[5]/div[2]/a/text()')
        pagenums = selector.xpath('/html/body/div[5]/div[2]/a/span/text()')
        nums = []
        returnData = []
        # 处理页面编号，得把它过滤出来并从 str 改到 int
        count = 0
        for s in pagenums:
            a = ''
            count += 1
            # 简单方法，硬上
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
    return(returnData) # 返回一个list，或'timeout'
```

##### 获取每一“页”的信息

```python
def getInfo(url, driver, tryNum=0):
    logprint('>>>>正在获取页面信息')
    data = getPage(url=url, driver=driver)
    # 进行错误处理
    if data == 'timeout':
        logprint('data of getinfo is timeout')
        imgURL = 'timeout'
        pageNum = 404
        pageName = 'timeout'
    else:
        # 把数据交给etree
        selector = etree.HTML(data)
        imgURL = selector.xpath('//*[@id="cp_image"]/@src')
        # 如果是加载出了问题，图片还没有加载出来，不要气馁，再试几次
        if imgURL == []:
            if tryNum <= 20:
                logprint('>>>>重新获取页面: '+url+' : '+str(tryNum))
                tryNum = tryNum + 1
                imgURL = 'timeout'
                getInfo(url=url, driver=driver, tryNum=tryNum) # 迭代自己
            else:
                logprint('>>>>尝试 20 次无效')
                imgURL = 'timeout'
                pageNum = 404
                pageName = 'timeout'
                saveBrokenLog(url)
        else:
            imgURL = imgURL[0] # 把URL从 list 转为 str（感谢弱类型）
        # 获取当前的页码
        pageNum = selector.xpath('//*[@id="lbcurrentpage"]/text()')[0] # list 转 str
        pageNum = int(pageNum) # str 转 int
        pageName = selector.xpath('/html/body/div[1]/div/div/p/text()')[0]
        # 把空白字符处理掉
        pageName.replace('\s', '')
        abcd = ''
        for i in pageName:
            if not i == '\t':
                if not i == ' ':
                    abcd += i
        pageName = abcd
        # 
        logprint('>>>> #' + str(pageNum))
        logprint('>>>> #' + pageName)
        logprint('>>>> #' + imgURL)
    return [pageNum, imgURL, pageName]
```
##### 获取图片

```python
def saveImage(imgUrl, path, name):
    img = requests.get(imgUrl, headers=header)
    img = img.content
    file = open(path, "wb") # 二进制输入
    file.write(img)
    logprint('>>>>file #'+name + 'written>>>>>>>')
```



# Proj-3：批量处理获取的图片

好了，我们要打开Xcode了。

我们对图片进行分类和提高画质的处理。

创建一个命令行工具就好了。

<img src="./Proj-2/images/img_xcode_start.png" />

### Swift 运行“命令行工具”

这段代码是通用的，所以对于我们这个程序可能有冗余的部分。

```swift
import Foundation

// MARK: ErroRs
/// This is a customized error enum. It has type of (.allGood), (.notFound), (.httpError)
enum ERRoR: Error {
    case allGood
    case notFound(String)
    case httpError(Int, String)
}

// MARK: runCommand
/// This function will return the command's output,  the  state code and throw  an  ERRoR state
func runCommand(_ bin: String, isPrint: Bool = false, arguments: [String], runtime: Int = 1) throws -> (String, Int) {
    let pipe = Pipe()
    let file = pipe.fileHandleForReading
    var launchPath = bin
    
    if launchPath.first != "/" || launchPath != "/usr/bin/which" {
        launchPath = try! runCommand("/usr/bin/which", arguments: [launchPath], runtime: 2).0
    }
    
    if launchPath.isEmpty || launchPath.first != "/" {
        throw ERRoR.notFound("command not found")
    } else {
        if launchPath.last == "\n" {
            launchPath = String(launchPath.dropLast())
        }
        let task = Process()
        task.launchPath = launchPath
        task.arguments = arguments
        task.standardOutput = pipe
        try! task.run()
        task.waitUntilExit()

        let data = file.readDataToEndOfFile()
        if runtime == 1, isPrint {
            print(String(data: data, encoding: String.Encoding.utf8)!)
        }
        var returnString = String(data: data, encoding: String.Encoding.utf8)!
        if returnString.last == "\n" {
            returnString = String(returnString.dropLast())
        }
        return (returnString, Int(task.terminationStatus))
    }
}

```

### 主体代码

```swift
import Foundation

print("@@@@@@START@@@@@@")

// Basic Settings
let FManager = FileManager.default

//目录 #1: ./bilibili/content/
let rootPath = "./bilibili/content/"
let rootURL = URL(fileURLWithPath: rootPath)
let pianPathSet = try! FManager.contentsOfDirectory(atPath: rootURL.path)
// 第一次循环, ./bilibili/content/, 获取“篇”
for pianSubPath in pianPathSet {
    if pianSubPath != ".DS_Store" { //排除 #系统文件
        //目录 #2: ./bilibili/content/
        let pianPath = rootPath + pianSubPath
        let pianURL = URL(fileURLWithPath: pianPath)
        let volPathSet = try! FManager.contentsOfDirectory(atPath: pianURL.path)
        // 第二次循环，./bilibili/content/篇*, 获取“话”
        for volSubPath in volPathSet {
            if volSubPath != ".DS_Store" {
                let volPath = pianPath + "/" + volSubPath
                let volURL = URL(fileURLWithPath: volPath)
                let chapterPathSet = try! FManager.contentsOfDirectory(atPath: volURL.path)
                // 第三次循环, ./bilibili/content/篇*/话*, 获取"页"
                for chapterSubPath in chapterPathSet {
                    if chapterSubPath != ".DS_Store" {
                        let chapterPath = volPath + "/" + chapterSubPath
                        let chapterURL = URL(fileURLWithPath: chapterPath)
                        var chapterNameS: String = ""
                        var chapterNameT: String = ""
                        var isRecordHua: Bool = false
                        //记录“话”
                        for i in chapterSubPath {
                            if i == "第", !isRecordHua {
                                isRecordHua = true
                            }
                            if isRecordHua {
                                chapterNameS += String(i)
                                //转化为简体
                                if i == "话" {
                                    chapterNameT += "話"
                                } else {
                                    chapterNameT += String(i)
                                }
                            }
                            if isRecordHua, i == "话" || i == "話" {
                                isRecordHua = false
                                break
                            }
                        }
                        let inpagePathSet = try! FManager.contentsOfDirectory(atPath: chapterURL.path)
                        // 第四次循环,./bilibili/content/篇*/话*/"页", 获取每一张图片
                        for pageIndex in 0 ..< inpagePathSet.count {
                            let inputPath = chapterPath + "/" + inpagePathSet[pageIndex]
                            // 输出目录
                            //加上“篇“
                            var outRootPath = "./bilibili/already/" + pianSubPath + "/"
                            if !FManager.fileExists(atPath: outRootPath) {
                                _ = try! runCommand("mkdir", arguments: ["\(outRootPath)"])
                            }
                            //加上”卷“
                            outRootPath += "/" + volSubPath
                            if !FManager.fileExists(atPath: outRootPath) {
                                _ = try! runCommand("mkdir", arguments: ["\(outRootPath)"])
                            }
                            //加上”话“
                            outRootPath += "/" + chapterSubPath
                            if !FManager.fileExists(atPath: outRootPath) {
                               _ = try! runCommand("mkdir", arguments: ["\(outRootPath)"])
                            }
                            //加上“页”
                            let outPath = outRootPath + "/" + "\(chapterNameS)_p\(pageIndex + 1).png" //简体
                            // 开始处理
                            print("########################################")
                            // 不要重复处理
                            if FManager.fileExists(atPath: outPath) {
                                print("##########FILE ALREADY EXISTED##########")
                                print(outPath)
                            } else if FManager.fileExists(atPath: outPathT) {
                                print("##########FILE ALREADY EXISTED##########")
                                print(outPath)
                                let exeNameChange = try! runCommand("mv", arguments: [outPathT, outPath]).1
                                if exeNameChange == 0 {
                                    print("##########FILE NAME is CHANGED##########")
                                } else {
                                    print("!!!!!!!!!!NAME  CHANGE  FAILED!!!!!!!!!!")
                                }
                            } else {
                                print(inputPath)
                                // 这里调用了一个开源软件
                                let exe = try! runCommand("/Users/HUi/bin/waifu2x", arguments: ["--type", "a", "--scale", "2", "--noise", "4", "--input", inputPath, "--output", outPath])
                                print(exe)
                            }
                        }
                    }
                }
            }
        }
    }
}

print("@@@@@@OVER@@@@@@")
```

> 代码重用到了一个“waifu2x”的开源软件，是Metal做的macOS版本的，原作是win专用的。
>
> 本次用到的：https://github.com/safx/waifu2x-metal（只用到了编译好的程序，没用用到代码）
>
> 原作：https://github.com/nagadomi/waifu2x



# 总结

我们着重研究了互联网爬虫以及数据处理的相关应用，是合法的应用，因为爬虫的应用同样可以造成危害。

1. 了解了互联网网页的基本架构，对我们眼前的绚丽网页有了更本质的了解；

2. 对数据进行处理的过程中，我们意识到科技、自动化带来的便利，也认识到其中可能存在的危害（比如侵害他人版权、导致服务器变慢）。

3. 使我们更加意识到，科技的发展是一把双刃剑，我们应当更好的利用科技来为人们服务，科技的最终目的是造福人类。作为使用者，应该健全法律意识，合理使用技术。作为开发者，应该频繁检查修理可能存在的漏洞，确保软件架构的安全完整性。作为政策制定的人，应该明确需求，合理制定相关法规。