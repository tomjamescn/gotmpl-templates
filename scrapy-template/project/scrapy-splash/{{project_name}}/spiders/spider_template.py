# -*- coding: utf-8 -*-
import scrapy
from scrapy_splash import SplashRequest

class TemplateSpider(scrapy.Spider):
    name = 'baobao.baidu.com'
    allowed_domains = ['baobao.baidu.com']
    custom_settings = {
        'CONCURRENT_REQUESTS': 2,
        'DOWNLOAD_DELAY': 0.25
    }
    defaultSplashArgs = {
        'wait': 0.5,
        'proxy': 'http://45.32.57.99:12345',
        'headers': {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.181 Safari/537.36'
        }
    }
    defaultHeaders = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.181 Safari/537.36'
    }
    
    def start_requests(self):
        list_urls = [
            'https://baobao.baidu.com/dailyjnl/list/56.html',
            'https://baobao.baidu.com/dailyjnl/list/5.html',
            'https://baobao.baidu.com/dailyjnl/list/6.html',
            'https://baobao.baidu.com/dailyjnl/list/7.html',
            'https://baobao.baidu.com/dailyjnl/list/53.html',
            'https://baobao.baidu.com/dailyjnl/list/8.html',
            'https://baobao.baidu.com/dailyjnl/list/4.html',
            'https://baobao.baidu.com/dailyjnl/list/16.html',
            'https://baobao.baidu.com/dailyjnl/list/14.html',
            'https://baobao.baidu.com/dailyjnl/list/15.html',
            'https://baobao.baidu.com/dailyjnl/list/57.html',
            'https://baobao.baidu.com/dailyjnl/list/17.html',
            'https://baobao.baidu.com/dailyjnl/list/13.html',
            'https://baobao.baidu.com/dailyjnl/list/19.html',
            'https://baobao.baidu.com/dailyjnl/list/59.html',
            'https://baobao.baidu.com/dailyjnl/list/22.html',
            'https://baobao.baidu.com/dailyjnl/list/21.html',
            'https://baobao.baidu.com/dailyjnl/list/29.html',
            'https://baobao.baidu.com/dailyjnl/list/30.html',
            'https://baobao.baidu.com/dailyjnl/list/31.html',
            'https://baobao.baidu.com/dailyjnl/list/32.html',
            'https://baobao.baidu.com/dailyjnl/list/54.html',
            'https://baobao.baidu.com/dailyjnl/list/78.html',
            'https://baobao.baidu.com/dailyjnl/list/83.html',
        ]

        for url in list_urls:
            yield SplashRequest(url, self.parseToList, args=self.defaultSplashArgs)

        #debug
        #yield SplashRequest('https://baobao.baidu.com/dailyjnl/list/83.html', self.parseToList, args=self.defaultSplashArgs)
        #yield SplashRequest('https://baobao.baidu.com/dailyjnl/list/30.html', self.parseList, args=self.defaultSplashArgs)

    def parseToList(self, response):
        max_page = 1
        tag_len = len(response.css('.pTag'))
        #3是因为prev和next被disable了
        if tag_len > 3:
            max_page = int(response.css('a.pTag::text')[tag_len - 2].extract())
            if max_page <= 1:
                yield {
                    'title': 'error',
                    'content': 'error',
                    'tag': 'error'
                }
            for i in range(2, max_page+1):
                url = "%s?pn=%d" % (response.url, (i-1)*6)
                #yield {
                #    'url': "%s?pn=%d" % (response.url, (i-1)*6),
                #}
                yield scrapy.Request(url, self.parseList, headers=self.defaultHeaders)
        else:
            #只有一页的情况
            yield scrapy.Request(response.url, self.parseList, headers=self.defaultHeaders)
            
    def parseList(self, response):
        for a in response.css('.jnl-list .jnl-i-body'):
            url = 'https://baobao.baidu.com' + a.css('a.link-default::attr(href)')[0].extract()
            #yield {'url': url}
            yield scrapy.Request(url, self.parseArticle, headers=self.defaultHeaders)

    def parseArticle(self, response):
        yield {
            'title': response.css('.jnv-title::text')[0].extract().strip(' \t\n\r'),
            'content': "".join(response.css('.jnv-content *::text').extract()).strip(' \t\n\r'),
            'tag': response.css('.jnv-i-period::text')[0].extract().strip(' \t\n\r'),
        }

