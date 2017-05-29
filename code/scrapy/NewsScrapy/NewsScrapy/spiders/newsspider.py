# -*- coding: utf-8 -*-
import scrapy
import re
import datetime, time
from scrapy.selector import Selector
from scrapy.http import Request
from NewsScrapy.items import NewsscrapyItem


# 爬取网易新闻
class NeteaseNewsSpider(scrapy.Spider):
    name = "netease_uews"
    allowed_domains = ["news.163.com"]
    start_urls = ['http://www.163.com/']

    # 爬取要闻连接
    def parse(self, response):
        selector = Selector(response)
        urls = selector.xpath('//div[@class="news_default_yw"]/ul/li/a/@href').extract()
        # 对获取到的URL进行清理
        for each in urls:
            if re.search('http://news.*?', each, re.S):
                yield Request(each, callback=self.newsparse)

    # 爬取新闻内容
    def newsparse(self, response):
        selector = Selector(response)
        news = selector.xpath('//div[@class="post_content_main"]')
        title_original = news.xpath('h1/text()').extract()[0]  # 提取标题
        newstime = news.xpath('div[@class="post_time_source"]/text()').extract()[0]  # 提取发布时间
        newstime = re.search('\d.*\d', newstime).group()
        try:
            newstime = datetime.datetime.strptime(newstime, '%Y-%m-%d %X')
        except Exception as e:
            newstime = datetime.datetime.now()

        content_html = news.xpath('div[@class="post_body"]/div[@class="post_text"]').extract()[0] # 提取内容

        content = news.xpath('div[@class="post_body"]/div[@class="post_text"]/p/text()').extract() # 获取文章简介
        for con in content:
            if re.search('.*', con).group():
                content = re.search('.{0,140}', con).group()
                break

        front_image = news.css('.post_text img::attr(src)').extract()  # 获取文章简介
        if front_image:
            front_image_url = front_image[0]
        else:
            front_image_url = 'http://i.guancha.cn/news/2017/05/20/20170520191531644.jpg'

        item = NewsscrapyItem()
        item['title'] = title_original
        item['title_original'] = title_original
        item['site_original'] = '网易'
        item['url_original'] = response.url
        item['newstime'] = newstime
        item['content'] = content
        item['content_html'] = content_html
        item['front_image_url'] = front_image_url
        item['similar'] = 0
        item['click'] = 0
        item['keyword'] = '0'

        yield item


# 爬取海外网新闻
class HiwainetNewsSpider(scrapy.Spider):
    name = "hiwaine_uews"
    allowed_domains = ["news.haiwainet.cn"]
    start_urls = ['http://www.haiwainet.cn/']

    # 爬取要闻连接
    def parse(self, response):
        selector = Selector(response)
        urls1 = selector.xpath('//div[@class="c"]/div[@class="box mt-bg"]/div[@class="k"]/h4/a/@href').extract()
        urls2 = selector.xpath('//div[@class="c"]/div[@class="box mt-bg"]/div[@class="k"]/ul/li/a/@href').extract()
        urls = urls1 + urls2
        for each in urls:
            yield Request(each, callback=self.newsparse)


    # 爬取新闻内容
    def newsparse(self, response):
        selector = Selector(response)
        title_original = selector.xpath('//div[@class="show_text fl"]/h1/text()').extract()[0] # 提取标题
        newstime = selector.xpath('//div[@class="show_text fl"]/div[@class="contentExtra"]/span[@class="first"]/text()').extract()[0]  # 提取发布时间
        try:
            newstime = datetime.datetime.strptime(newstime, '%Y-%m-%d %X')
        except Exception as e:
            newstime =  datetime.datetime.now()

        content_html = selector.xpath('//div[@class="contentMain"]').extract()[0]  # 提取内容

        content = selector.xpath('//div[@class="contentMain"]/p/text()').extract()  # 获取文章简介
        for con in content:
            if re.search('.*', con).group():
                content = re.search('.{0,140}', con).group()
                break

        front_image = selector.css('.contentMain img::attr(src)').extract()  # 获取封面图
        if front_image:
            front_image_url = front_image[0]
        else:
            front_image_url = 'http://i.guancha.cn/news/2017/05/20/20170520191531644.jpg'

        item = NewsscrapyItem()
        item['title'] = title_original
        item['title_original'] = title_original
        item['site_original'] = '海外网'
        item['url_original'] = response.url
        item['newstime'] = newstime
        item['content'] = content
        item['content_html'] = content_html
        item['front_image_url'] = front_image_url
        item['similar'] = 0
        item['click'] = 0
        item['keyword'] = '0'

        yield item


# # 爬取观察者网新闻
# class GuanchaNewsSpider(scrapy.Spider):
#     name = "guancha_uews"
#     allowed_domains = ["www.guancha.cn"]
#     start_urls = ['http://www.guancha.cn/politics/2017_05_21_409319.shtml']
#
#     # 爬取要闻连接
#     def parse(self, response):
#         selector = Selector(response)