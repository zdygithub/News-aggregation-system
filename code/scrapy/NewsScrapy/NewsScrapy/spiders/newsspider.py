import scrapy
import re
import datetime
from scrapy.selector import Selector
from scrapy.http import Request
from NewsScrapy.items import NewsscrapyItem


# 爬取网易新闻
class NeteaseUewsSpider(scrapy.Spider):
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
        original_title = news.xpath('h1/text()').extract()[0]  # 提取标题
        post_time = news.xpath('div[@class="post_time_source"]/text()').extract()[0]  # 提取发布时间
        post_time = re.search('\d.*\d', post_time).group()
        try:
            post_time = datetime.datetime.strptime(post_time, '%y/%m/%d').date()
        except Exception as e:
            post_time = datetime.datetime.now().date()

        content_html = news.xpath('div[@class="post_body"]/div[@class="post_text"]').extract()[0].strip()  # 提取内容
        c = content_html.encode('utf-8')

        item = NewsscrapyItem()
        item['title'] = original_title
        item['original_title'] = original_title
        item['original_url'] = response.url
        item['original_site'] = '网易'
        item['post_time'] = post_time
        item['content_html'] = content_html
        item['content_html1'] = c
        yield item
