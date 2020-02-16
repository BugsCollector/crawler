## 概念

selnium是一个自动化测试框架，我们主要用它的webdriver。



## webdriver

支持各大主流浏览器

### chromedriver安装:

安装chromedriver,下载压缩包，解压以后，把可执行文件所在的目录放到PATH环境变量里，比如，chromedriver在/home/user/

```bash
export PATH="$PATH:/home/user"
```

如果不设置环境变量，则需要在启动的时候指定chromedriver的路径。



### 启动浏览器

```python
from selenium import webdriver
# 启动chrome浏览器
driver = webdriver.Chrome()
# 指定chromedriver的路径并启动Chrome
driver = webdriver.Chrome(executable_path='/home/user/chromedirver')
#启动chrome-headless
from selenium.webdriver.chrome.options import Options
option = Options()
option.add_argument('--headless')
driver = webdriver.Chrome(chrome_options=option)

# 启动phantomjs
driver = webdriver.PhantomJs()
```

chrome-headless是无界面版的chrome，它替代了停止维护的phantomjs.

### 控制浏览器

```python
# 访问某个url
driver.get('https://www.baidu.com')
# 刷新
driver.refersh()
# 前进
driver.forward()
# 后退
driver.back()
#退出
driver.quit()
# 当前的url
driver.current_url
# 截图
driver.save_screenshot('/tmp/test.png')
```



### 元素查找

18个find函数

```python
# 根据元素的class属性的值查找 
driver.find_element_by_class_name
# 用CSS选择器查找
driver.find_element_by_css_selector
# 根据元素的ID
 driver.find_element_by_id
# 根据链接内的文本查找
find_element_by_link_text
# 根据元素的name属性查找 
find_element_by_name
# 根据链接内的文本是否包含指定的查找文字
find_element_by_partial_link_text
# 根据标签名查找
find_element_by_tag_name
# 根据xpath表达示查找 
find_element_by_xpath
```

另外，以上函数分别还有个查找多个元素的对应函数，把element变成复数，比如: find_elements_by_xpath,
注意：find_element函数返回单个WebElement对象，
而所有的find_elements则返回一个列表，包含若干个WebElement对象
如果查找不到，则抛出异常



### page_source

获取整个页面的源码

### get_cookie/get_cookies

获取服务器返回的cookie



### 执行javascript

```python
# 将网页滚动到最底部
driver.execute('window.scrollTo(0, document.body.scrollHeight)')
# 执行异步的js函数
driver.execute_async_script('send_xml_request()')
```



### 等待,wait

#### 隐式等待

```python
# 查找某个(某些)元素，如果没有立即查找到，则等待10秒
driver.implicityly_wait(10)
```

#### 显式等待

```python
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
# 查找一个按钮
# 最长等待10秒，直到找到查找条件中指定的元素
sort_btn = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, './/div[@class="f-sort"]/a[2]'))
    )

```

这两个等待，显示等待通常更符合我们的程序逻辑。当我们对页面的加载方式还不太确定的时候，也可以隐式等待。

## WebElement



也有一堆的find函数，用法和之前一样。

### click

点击某个具体的元素

### send_keys

向某个元素（通常是可输入的标签，比如input）发送键盘事件

```python
# 向input元素内输入iphone
input.send_keys('iphone')
# 向input发送一个回车键
from selenium.webdriver.common.keys import Keys
input.send_keys(Keys.RETURN)
```

### rect

返回元素的宽和高，以及在屏幕上的坐标

```python
# 返回结果
{u'height': 24, u'width': 26, u'x': 347.1875, u'y': 19}
```

### location

返回在屏幕上的坐标

### text

返回元素内的文本信息、

注意：我们在selenium内查找元素时，不可以直接查找它的文本，比如写xpath表达式的时候， 不可以用text()函数，要先取到节点，然后再用它的text属性取出文本。



get_attribute

get_proerty

获取元素的属性值，同上，它也不可以在选择器里直接写，需要先取到节点，然后再调用这俩方法去获取属性值。

value_of_css_property

获取节点的CSS样式属性

