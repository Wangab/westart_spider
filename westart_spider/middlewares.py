# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/spider-middleware.html
import json
import urllib

import requests
from scrapy import signals
import signal
from selenium import webdriver
from scrapy.http import HtmlResponse, TextResponse
from selenium.webdriver.remote.command import Command


class WestartSpiderSpiderMiddleware(object):
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

        # Must return an iterable of Request, dict or Item objects.
        for i in result:
            yield i

    def process_spider_exception(self, response, exception, spider):
        # Called when a spider or process_spider_input() method
        # (from other spider middleware) raises an exception.

        # Should return either None or an iterable of Response, dict
        # or Item objects.
        pass

    def process_start_requests(self, start_requests, spider):
        # Called with the start requests of the spider, and works
        # similarly to the process_spider_output() method, except
        # that it doesn’t have a response associated.

        # Must return only requests (not items).
        for r in start_requests:
            yield r

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)


    def process_request(self, request, spider):
        url = request.url
        if str(url).find("&pp=")>-1:
            json_prap = json.loads(urllib.unquote(url.split("&pp=")[1]))
            url = str(url).split("&pp=")[0]
            response = requests.post(url=url, data=json_prap)
            return TextResponse(url=url, body=bytes(json.dumps(response.json())))
        else:
            browser = webdriver.PhantomJS(
                service_args=['--load-images=false', '--ssl-protocol=any', '--ignore-ssl-errors=true'])
            browser.start_session(webdriver.DesiredCapabilities.PHANTOMJS)
            try:
                browser.execute(Command.POST, {'url': url})
                res = HtmlResponse(url, encoding='utf-8', status=200, body=browser.page_source)
                browser.close()
                browser.service.process.send_signal(signal.SIGTERM)
                browser.quit()
                return res
            except Exception, e:
                browser.service.process.send_signal(signal.SIGTERM)
                browser.quit()
