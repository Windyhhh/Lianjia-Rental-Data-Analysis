# Define here the models for your spider middleware
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/spider-middleware.html

from scrapy import signals
from scrapy.http import HtmlResponse
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

# useful for handling different item types with a single interface
from itemadapter import is_item, ItemAdapter


class SeleniumMiddleware:
    """Selenium中间件 - 处理需要登录的页面"""

    def __init__(self):
        self.driver = None
        self.login_prompted = False

    @classmethod
    def from_crawler(cls, crawler):
        middleware = cls()
        crawler.signals.connect(middleware.spider_opened, signal=signals.spider_opened)
        crawler.signals.connect(middleware.spider_closed, signal=signals.spider_closed)
        return middleware

    def spider_opened(self, spider):
        """爬虫开启时初始化Selenium"""
        spider.logger.info('初始化Selenium WebDriver...')

        chrome_options = Options()
        # 禁用自动化特征
        chrome_options.add_argument('--disable-blink-features=AutomationControlled')
        chrome_options.add_experimental_option('excludeSwitches', ['enable-automation'])
        chrome_options.add_experimental_option('useAutomationExtension', False)

        # 设置User-Agent
        chrome_options.add_argument('--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36')

        self.driver = webdriver.Chrome(options=chrome_options)

        # 隐藏webdriver特征
        self.driver.execute_cdp_cmd('Page.addScriptToEvaluateOnNewDocument', {
            'source': '''
                Object.defineProperty(navigator, 'webdriver', {
                    get: () => undefined
                });
            '''
        })

        spider.logger.info('Selenium WebDriver 初始化完成')

    def spider_closed(self, spider):
        """爬虫关闭时关闭Selenium"""
        if self.driver:
            spider.logger.info('关闭Selenium WebDriver...')
            self.driver.quit()

    def process_request(self, request, spider):
        """使用Selenium处理请求"""
        if not self.driver:
            return None

        spider.logger.info(f'使用Selenium访问: {request.url}')

        try:
            self.driver.get(request.url)
            time.sleep(3)  # 等待页面加载

            # 检查是否需要登录或验证码
            current_url = self.driver.current_url

            if 'captcha' in current_url or 'login' in current_url:
                if not self.login_prompted:
                    spider.logger.warning('⚠️ 检测到需要登录或验证码！')
                    spider.logger.warning('请在浏览器中完成登录，您有60秒时间...')
                    self.login_prompted = True

                    # 等待60秒让用户登录
                    time.sleep(60)

                    # 重新访问原始URL
                    self.driver.get(request.url)
                    time.sleep(3)

            # 获取页面源码
            body = self.driver.page_source.encode('utf-8')

            # 返回HtmlResponse
            return HtmlResponse(
                url=self.driver.current_url,
                body=body,
                encoding='utf-8',
                request=request
            )

        except Exception as e:
            spider.logger.error(f'Selenium处理请求时出错: {e}')
            return None


class LianjiaSpiderSpiderMiddleware:
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the spider middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_spider_input(self, response, spider):
        # Called for each response that goes through the spider
        # middleware and into the spider.

        # Should return None or raise an exception.
        return None

    def process_spider_output(self, response, result, spider):
        # Called with the results returned from the Spider, after
        # it has processed the response.

        # Must return an iterable of Request, or item objects.
        for i in result:
            yield i

    def process_spider_exception(self, response, exception, spider):
        # Called when a spider or process_spider_input() method
        # (from other spider middleware) raises an exception.

        # Should return either None or an iterable of Request or item objects.
        pass

    def process_start_requests(self, start_requests, spider):
        # Called with the start requests of the spider, and works
        # similarly to the process_spider_output() method, except
        # that it doesn’t have a response associated.

        # Must return only requests (not items).
        for r in start_requests:
            yield r

    def spider_opened(self, spider):
        spider.logger.info("Spider opened: %s" % spider.name)


class LianjiaSpiderDownloaderMiddleware:
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the downloader middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_request(self, request, spider):
        # Called for each request that goes through the downloader
        # middleware.

        # Must either:
        # - return None: continue processing this request
        # - or return a Response object
        # - or return a Request object
        # - or raise IgnoreRequest: process_exception() methods of
        #   installed downloader middleware will be called
        return None

    def process_response(self, request, response, spider):
        # Called with the response returned from the downloader.

        # Must either;
        # - return a Response object
        # - return a Request object
        # - or raise IgnoreRequest
        return response

    def process_exception(self, request, exception, spider):
        # Called when a download handler or a process_request()
        # (from other downloader middleware) raises an exception.

        # Must either:
        # - return None: continue processing this exception
        # - return a Response object: stops process_exception() chain
        # - return a Request object: stops process_exception() chain
        pass

    def spider_opened(self, spider):
        spider.logger.info("Spider opened: %s" % spider.name)
