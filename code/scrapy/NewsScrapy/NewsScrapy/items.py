# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class NewsscrapyItem(scrapy.Item):
    title = scrapy.Field()
    title_original = scrapy.Field()
    url_original = scrapy.Field()
    site_original = scrapy.Field()
    newstime = scrapy.Field()
    content = scrapy.Field()
    content_html = scrapy.Field()
