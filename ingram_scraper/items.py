# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class IngramItem(scrapy.Item):
    title = scrapy.Field()
    vpn = scrapy.Field()

    description = scrapy.Field()
    full_description = scrapy.Field()

    category = scrapy.Field()
    sub_category = scrapy.Field()

    image_urls = scrapy.Field()
    images = scrapy.Field()
    image_paths = scrapy.Field()

    product_id = scrapy.Field()
    url = scrapy.Field()
