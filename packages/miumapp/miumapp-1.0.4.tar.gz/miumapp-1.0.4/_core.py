import asyncio, socket, os
from os.path import abspath
from pathlib import Path
from json import loads as json_loads
from json import dumps as json_dumps
from typing import Dict, Any
from tornado.web import RequestHandler, Application
from pyppeteer.launcher import Launcher, DEFAULT_ARGS
from pyppeteer.page import Page


# 使不会提示'缺少 Google API 密钥, 因此 Chromium 的部分功能将不可使用。'
os.environ["GOOGLE_API_KEY"] = "no"
os.environ["GOOGLE_DEFAULT_CLIENT_ID"] = "no"
os.environ["GOOGLE_DEFAULT_CLIENT_SECRET"] = "no"

# 为 Page.goto 添加 title 参数
native_goto = Page.goto
async def goto(self:Page, url:str, title='', options=None, **kwargs):
    r = await native_goto(self, url, options, **kwargs)
    if title:
        await self.evaluate(f"document.title = '{title}'")
    return r
Page.goto = goto

# 优化启动参数
DEFAULT_ARGS[:] = [
    '--disable-background-networking',
    '--disable-background-timer-throttling',
    '--disable-breakpad',
    '--disable-browser-side-navigation',
    '--disable-client-side-phishing-detection',
    '--disable-sync',
    '--disable-translate',
    '--start-maximized',
    '--disable-infobars',
    '--no-default-browser-check',
    '--metrics-recording-only',
    '--safebrowsing-disable-auto-update',
    '--password-store=basic',
    '--use-mock-keychain',
    '--disable-dev-shm-usage',
    '--disable-prompt-on-repost',
    '--disable-features=site-per-process',
    '--disable-hang-monitor',
    '--disable-default-apps',
    '--no-first-run',
    '--disable-popup-blocking',
    '--disable-session-crashed-bubble',
]

# 创建代码提示
class window(Page):
    async def goto(self, url:str, title='', options=None, **kwargs):
        return Page.goto(...)

# 仅被该装饰器装饰过的方法支持被JS调用
# 该装饰器只能修饰异步方法
_allow_callpy_funcs = set()
def allow_callpy(func):
    _allow_callpy_funcs.add(func.__func__ if hasattr(func, '__func__') else func)
    return func


class App:

    def __init__(self, chrome:str|Path):
        self.chrome = abspath(chrome)
        self._sys_pages: Dict[Page, Any] = {}

    async def main(self):
        '''
        启动 APP 时会自动执行此 main 函数
        
        请在子类中覆盖此方法
        '''
    
    async def create_window(self, *, url: str='', html: str='', cache_dir: str|Path, title='', as_app=True) -> window:
        cache_dir = Path(cache_dir)
        cache_dir.mkdir(parents=True, exist_ok=True)

        # 以下内容为miumapp开源项目维护者自己看的笔记, 调用者请忽略：
            # 创建新窗口的指令, 要么是由活跃窗口创建的, 要么是由主任务 main 创建的
            # 如果是由活跃窗口创建的, 说明 _sys_pages 还有活跃窗口, 此时清理已关闭的窗口不会使 _sys_pages 变空.
            # 如果是由主任务 main 创建的, 说明主任务 main 还没结束, 此时即使清空 _sys_pages 也不会导致程序退出.
            # 先清理 _sys_pages 中的旧窗口, 再创建新窗口, 可防止由于 _sys_pages 的清理速度跟不上窗口创建速度导致 _sys_pages 容量越来越大.
        for x in self._sys_pages.copy():
            if x.isClosed():
                self._sys_pages.pop(x, 0)
        if not url:
            url, self._home_text = f'http://localhost:{self._server_port}', html
        browser = await Launcher(
            executablePath = self.chrome,
            userDataDir = cache_dir.absolute(),
            headless = False,
            args = [f'--app={url}'] if as_app else [],  # 访问的页面不能是'about:blank'
            defaultViewport = {},
            timeout = 15 * 1000
        ).launch()
        page = (await browser.pages())[0]
        if not as_app:
            await page.goto(url)
        self._sys_pages[page] = 1
        if title:
            await page.evaluate(f"document.title = '{title}'", force_expr=True)
        # 使支持callpy
        js_content = ['() => {', 'window.miumapp = {}', '}']
        js_content.insert(-1, f'''
            miumapp.callpy = async (method_name, kwargs={{}}) => {{
                let body = JSON.stringify( {{method_name:method_name, kwargs:kwargs}} )
                let response = await fetch('http://localhost:{self._server_port}/callpy/', {{method:'POST', body:body}})
                return await response.json()
            }}
        ''')
        if as_app:
            js_content.insert(-1, f'''
                document.addEventListener('keydown', function(e) {{if (e.keyCode == 123) {{e.preventDefault()}}}})  // F12
                document.addEventListener('keydown', function(e) {{if (e.keyCode == 116) {{e.preventDefault()}}}})  // F5
                document.addEventListener('contextmenu', function(e) {{e.preventDefault()}})  // 右键
                document.addEventListener('keydown', function(event) {{if (event.ctrlKey && (event.key === 's' || event.key === 'S')) {{event.preventDefault()}}}})  // Ctrl+S
            ''')
        js_content = '\n'.join(js_content)
        await page.evaluate(js_content)
        await page.evaluateOnNewDocument(js_content)
        return page

    async def start(self):

        class home_text(RequestHandler):
            async def get(TorSelf):
                TorSelf.set_header("Access-Control-Allow-Origin", "*")
                return TorSelf.write( self._home_text )
        
        class callpy(RequestHandler):            
            async def post(TorSelf):
                try:
                    try:
                        TorSelf.set_header("Access-Control-Allow-Origin", "*")
                        body: dict = json_loads(TorSelf.request.body)
                        method_name = body['method_name']
                        kwargs = body['kwargs'] or {}
                        if method_name[:1] == '_':
                            code, msg, data = 2, "For the server's security, calling methods starting with '_' is prohibited.", None
                        else:
                            func = getattr(self, method_name)
                            __func__ = func.__func__ if hasattr(func, '__func__') else func
                            if __func__ in _allow_callpy_funcs:
                                code, msg, data = 0, '', await func(**kwargs)
                            else:
                                code, msg, data = 3, 'This method does not allow calling.', None
                        try:
                            r = json_dumps({'code':code, 'msg':msg, 'data':data}, ensure_ascii=False)
                        except:
                            r = json_dumps({'code':code, 'msg':msg, 'data':str(data)}, ensure_ascii=False)
                        return TorSelf.write(r)
                    except Exception as e:
                        return TorSelf.write( json_dumps({'code':1, 'msg':str(e), 'data':None}, ensure_ascii=False) )
                except Exception as e:
                    print(e)
        
        # 查找一个空闲端口
        sock = socket.socket()
        sock.bind(('localhost', 0))
        self._server_port = sock.getsockname()[1]
        sock.close()

        Application(handlers=[
            ('/callpy/?', callpy),
            ('/?', home_text),
        ], debug=False).listen(port=self._server_port, address="localhost")

        await self.main()
        print('\n主任务 "main" 已完成.')
        print('从此刻开始, 一旦所有窗口都被关闭, 程序将在 30 秒内自动退出.\n')
        for x in self._sys_pages.copy():
            if x.isClosed():
                self._sys_pages.pop(x, 0)
        while _sys_pages := self._sys_pages.copy():
            for x in _sys_pages:
                if x.isClosed():
                    self._sys_pages.pop(x, 0)
                else:
                    await asyncio.sleep(30)
        print('\n\n所有窗口均已关闭, 程序即将退出.\n')