# Proj-1

## Python 图片爬虫

### 使用的库

> etree from lxml
>
> requests

### 爬取的内容
[https://bing.ioliu.cn/](https://bing.ioliu.cn/) 网站上的必应壁纸

### 分析网页

#### 页面
第1页：[https://bing.ioliu.cn/?p=1](https://bing.ioliu.cn/?p=1)

第2页：[https://bing.ioliu.cn/?p=2](https://bing.ioliu.cn/?p=2)

第3页：[https://bing.ioliu.cn/?p=3](https://bing.ioliu.cn/?p=3)

我们可以看到，翻页的方式是通过 `?p=` 给的参数，一共120页。

```python
for i in range(1,121):
    urls = 'https://bing.ioliu.cn/?p={}'.format(i)
```

#### 图片链接、名称及版权、日期

敲黑板，这是重点！（毕竟我们是来下载图片的嘛）

<img src="./img/img_xpath_of_pic_url.png" />

这个时候我们可以引用一句数学老师们最讨厌的话

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

<img src="./img/img_xpath_of_pic_name_and_copyright.png"/>

<img src="./img/img_xpath_of_pic_date.png"/>

这是我们在用一句学生们们最喜欢的话：

> 同理可得：

```python
xpath_of_name = '/html/body/div[3]/div/div/div[1]/h3/text()'
xpath_of_date = '/html/body/div[3]/div/div/div[1]/p[1]/em/text()'
```
------
如果你没有`由图知`的能力，这里是获取 XPath 的正经方法：

##### **`右键 ⇒ 'Copy' ⇒ 'Copy XPath'`**

<img src="./img/img_copy_xpath.png"/>

> 综上所述：

```python
xpath_of_pictures_url = '/html/body/div[3]/div/div/img/@src'
xpath_of_name = '/html/body/div[3]/div/div/div[1]/h3/text()'
xpath_of_date = '/html/body/div[3]/div/div/div[1]/p[1]/em/text()'
```
> 删去了迭代的部分，etree 会帮我们自动迭代，也不需要用for-in
> Etree 会迭代所有内容，你可以用以下方式自定义范围

> ```python
> for i in range(1,8):
>     xpaths_of_pictures_url = '/html/body/div[3]/div[{}]/div/img/@src'.format(i)
>     xpaths_of_name = '/html/body/div[3]/div[{}]/div/div[1]/h3/text()'.format(i)
>     xpaths_of_date = '/html/body/div[3]/div[{}]/div/div[1]/p[1]/em/text()'.format(i)
> # 传给 etree.xpath() 的只能是String.
> ```

### 开始CODE

终于到上代码的时间了！🎉

首先，我们来一点`import` ：

```python
import requests # 获取文件
from lxml import etree # 分析HTML
import time # 用于暂停一段时间
import os # 调用系统功能
```

获取当前工作路径，用于保存文件：

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

主体代码

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

一些函数

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
        # 不要放弃，再试几次 # 我设置的20次，可以在参数设置
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

仔细观察发现，copyright 里面竟然有个`/`。去访达里看看，会发现一个神奇的事情，<img src="./img/img_slash.png" style="zoom:35%;" /> ，访达怎么会支持这种东东！？

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
现在运行就应该是OK👌的了。

### 大功告成

至此，第一个项目就结束了。在这里查看<a src="./bingWallpapers.py">完整代码</a>。
