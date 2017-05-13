import scrapy
import re
import datetime
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
            newstime = datetime.datetime.strptime(newstime, '%y/%m/%d').date()
        except Exception as e:
            newstime = datetime.datetime.now().date()

        content_html = news.xpath('div[@class="post_body"]/div[@class="post_text"]').extract()[0].strip()  # 提取内容
        c = content_html.encode('utf-8')

        item = NewsscrapyItem()
        item['title'] = title_original
        item['title_original'] = title_original
        item['url_original'] = response.url
        item['site_original'] = '网易'
        item['newstime'] = newstime
        item['content'] = c
        item['content_html'] = content_html
        yield item
