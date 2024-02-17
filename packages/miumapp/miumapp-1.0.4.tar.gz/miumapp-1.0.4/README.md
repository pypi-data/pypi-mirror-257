# 项目描述

一个使用 Python + HTML + CSS + JavaScript 开发桌面应用的框架。

功能：

* 可在 HTML 中调用后端的 Python 函数。
* 可在 Python 上下文中调用窗口内的 JavaScript 对象。
* 可在 Python 上下文中对窗口发送操纵指令，执行包括但不限于：URL跳转、关闭窗口、JS注入、最大化等操作。
* 可开启多个窗口。
* 由于每个窗口可与 Python 双向调用，因此不同窗口之间可通过【窗口A → Python → 窗口B】的途径相互调用。
* 可指定窗口标题。
* 可指定窗口图标。
* 可通过传递 URL 或 HTML 文本这两种数据之一来决定窗口内容。
* 可通过 Nuitka 打包成二进制文件。

我们所采用的技术栈组合是经过深思熟虑的，通过结合 **Python** 的高效性和易用性，以及  **HTML** 、**CSS** 和 **JavaScript** 的前端技术，意味着您正在选择一个能够大大减少开发时间、简化开发流程、拥有丰富的第三方扩展的解决方案。与其它工具相比，我们的优势在于对新技术的快速适应、更为强大的社区支持，以及持续的更新和改进。

# 作者信息

昵称：江南雨上

[主页](https://lcctoor.github.io/arts/) \| [微信](https://lcctoor.github.io/arts/arts/ip_static/WeChatQRC.jpg) \| [Github](https://github.com/lcctoor) \| [PyPi](https://pypi.org/user/lcctoor) \| [邮箱](mailto:lcctoor@outlook.com) \| [捐赠](https://lcctoor.github.io/arts/arts/ip_static/DonationQRC-0rmb.jpg)

# Bug提交、功能提议

您可以通过 [Github-Issues](https://github.com/lcctoor/arts/issues)、[微信](https://lcctoor.github.io/arts/arts/ip_static/WeChatQRC.jpg) 与我联系。

# 安装

```
pip install miumapp
```

# 教程 ([查看美化版](https://lcctoor.github.io/arts/arts/miumapp) 👈)

本文将以最简洁的方式向你介绍核心知识，而不会让你被繁琐的术语所淹没。

## 运行内置Demo

```python
import asyncio
from pathlib import Path
from miumapp.demo import demo_app


# 指定chromium浏览器路径
# chromium官网下载地址：https://www.chromium.org/getting-involved/download-chromium/
# 在此示例中，我们直接使用Windows自带的Edge浏览器，由于Edge浏览器是基于chromium内核开发的，因此使用Edge浏览器也能达到几乎相同的效果
chrome = r'C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe'

# 指定chromium缓存路径
cache_dir = Path('~/.miumapp/demo').expanduser()

# 运行demo
task = demo_app(chrome=chrome, chrome_cache_dir=cache_dir)
asyncio.run(task)
```

[demo效果图](https://lcctoor.github.io/arts/arts/miumapp/ip_static/DemoUI.png) 👈

## 导入

```python
import asyncio
from pathlib import Path
from miumapp import App, allow_callpy
```

## 创建 APP

```python
class my_app(App):
  
    async def main(self):
        ...

# 指定chromium浏览器路径
# chromium官网下载地址：https://www.chromium.org/getting-involved/download-chromium/
# 在此示例中，我们直接使用Windows自带的Edge浏览器，由于Edge浏览器是基于chromium内核开发的，因此使用Edge浏览器也能达到几乎相同的效果
chrome = r'C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe'

# 运行APP
task = my_app(chrome=chrome).start()
asyncio.run(task)
```

由于我们在主任务 main 中未定义任何代码，因此这个 APP 是一个空 APP，运行后看不到任何效果。

## 创建窗口

创建一个窗口时，必须指定【窗口内容源】和【窗口缓存文件夹】。

```python
class my_app(App):
  
    async def main(self):
        html = 'Hello, miumapp !'
        cache_dir = Path('~/.miumapp/cache_dir/1').expanduser()  # 相当于 'C:/Users/<当前用户名>/.miumapp/cache_dir/1'
        await self.create_window(html=html, cache_dir=cache_dir)

chrome = r'C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe'
task = my_app(chrome=chrome).start()
asyncio.run(task)
```

此时，我们将能看到屏幕上打开了一个窗口，其内容为“Hello, miumapp !”。

### 指定窗口内容源

可通过传递 URL 或 HTML 文本这两种数据之一来决定窗口内容，例如：

```python
await self.create_window(html='你好!', cache_dir=cache_dir)
```

```python
await self.create_window(url='https://www.baidu.com/', cache_dir=cache_dir)
```

### 指定窗口标题

```python
await self.create_window(html='你好!', cache_dir=cache_dir, title='第一个窗口')
```

### 窗口缓存文件夹

不同的窗口实例不能同时使用同一个缓存文件夹。

以下示例是错误的：

```python
window1 = await self.create_window(html='你好!', cache_dir='C:/miumapp_cache_dir/1')
window2 = await self.create_window(html='你好!', cache_dir='C:/miumapp_cache_dir/1')
```

以下示例是可行的：

```python
window1 = await self.create_window(html='你好!', cache_dir='C:/miumapp_cache_dir/1')
window2 = await self.create_window(html='你好!', cache_dir='C:/miumapp_cache_dir/2')
```

以下示例也是可行的：

```python
window1 = await self.create_window(html='你好!', cache_dir='C:/miumapp_cache_dir/1')
await window1.close()  # 关闭第一个窗口
window2 = await self.create_window(html='你好!', cache_dir='C:/miumapp_cache_dir/1')
```

## 关闭窗口

可通过对窗口对象执行 `await window.close()` 或者点击窗口右上角的 `×` 图标来关闭窗口。

## 在 HTML 中调用 Python 函数

使用 allow_callpy 装饰的 Python 异步函数将能够在 HTML 中被调用，例如：

```python
class my_app(App):
  
    async def main(self):
        html = 'Hello, miumapp !'
        cache_dir = Path('~/.miumapp/cache_dir/1').expanduser()
        await self.create_window(html=html, cache_dir=cache_dir)

    @allow_callpy
    async def addition(self, a, b):
        return a + b

    async def sub(self, a, b):
        return a - b

chrome = r'C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe'
task = my_app(chrome=chrome).start()
asyncio.run(task)
```

在这个例子中，方法 sub 只能在 Python 层面被调用，而方法 addition 既能在 Python 层面被调用，也能在 HTML 中被调用。

在 HTML 中调用 addition 方法：

```JavaScript
async function sum() {
    let a = parseInt( document.getElementById('a').value )  // 30
    let b = parseInt( document.getElementById('b').value )  // 50
    let kwargs = {a:a, b:b}
    let result = await miumapp.callpy(method='addition', kwargs=kwargs)
    console.log(result)  // {"code":0, "msg":"", "data":80}
}
```

## 在 Python 中调用 JavaScript 对象

### 一些示例

执行 JavaScript 代码：

```python
await window.evaluate("document.title = '第一个APP'", force_expr=True)
```

```python
await window.evaluate("alert(1)", force_expr=True)
```

获取变量值：

```python
CityName = await window.evaluate("CityName")  # 假设窗口中有一个叫 CityName 的变量
print(CityName)  # >>> '北京市'
```

调用函数并获取返回值：

```python
city_name = await window.evaluate("get_city_name()", force_expr=True)  # 假设窗口中有一个叫 get_city_name 的函数
print(city_name)  # >>> '上海市'
```

由于 window 对象继承自 pyppeteer.page.Page，因此 window.evaluate 支持 pyppeteer.page.Page.evaluate 的所有用法。关于 window.evaluate 的更多用法，请参考 [pyppeteer.page.Page.evaluate](https://pyppeteer.github.io/pyppeteer/reference.html#pyppeteer.page.Page.evaluate) 。

## window 对象的更多方法

由于 window 对象继承自 pyppeteer.page.Page，因此 window 支持 pyppeteer.page.Page 的所有方法，例如页面跳转、点击按钮、输入等。关于 window 的更多方法，请参考 [pyppeteer.page.Page](https://pyppeteer.github.io/pyppeteer/reference.html#pyppeteer.page.Page) 。
