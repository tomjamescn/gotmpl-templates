# -*- coding: utf-8 -*-
import scrapy

class {{class_prefix}}Spider(scrapy.Spider):
    name = '{{spider_name}}'
    allowed_domains = ['{{spider_name}}']
    custom_settings = {
        'CONCURRENT_REQUESTS': 2,
        'DOWNLOAD_DELAY': 0.25
    }
    defaultHeaders = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.181 Safari/537.36'
    }

    def start_requests(self):
        urls = [
            'https://xxxx.com',
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parseList, headers=self.defaultHeaders)
        
    def parseList(self, response):
        blocks = response.css('.pic-txt')
        for b in blocks:
            url = 'https:' + b.css('.tit a::attr(href)')[0].extract()
            #yield {'url': url}
            yield scrapy.Request(url=url, callback=self.parseArticle, headers=self.defaultHeaders)
    
    def parseArticle(self, response):
        yield {
            'title': response.css('.artTit::text')[0].extract(),
            'content': "".join(response.css('.artText *::text').extract()),
            'tag': " ".join(response.css('.artLabel a::text').extract()),
        } 
