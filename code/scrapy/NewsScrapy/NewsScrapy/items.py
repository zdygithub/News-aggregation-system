# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class NewsscrapyItem(scrapy.Item):
    title = scrapy.Field()
    original_title = scrapy.Field()
    post_time = scrapy.Field()
    original_url = scrapy.Field()
    original_site = scrapy.Field()
    content_html = scrapy.Field()
    content_html1 = scrapy.Field()
