from scrapy.cmdline import execute

import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.system('scrapy crawl netease_uews')
# os.system('scrapy crawl hiwaine_uews')