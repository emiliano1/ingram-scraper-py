# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import scrapy
from scrapy.exceptions import DropItem


class IngramPipeline(object):
    def process_item(self, item, spider):
        item['image_paths'] = [image['path'] for image in item['images']]

        request = scrapy.Request(item['url'])
        dfd = spider.crawler.engine.download(request, spider)
        dfd.addBoth(self.return_item, item)

        return dfd


    @staticmethod
    def return_item(response, item):
        item['full_description'] = response.css('#pnl_AbridgedDescription span::text').extract_first()
        if not item['full_description']:
            item['full_description'] = response.css('#pnl_FullDescription .product-detail-description span::text').extract_first()

        return item


class IngramExistingCSVPipeline(object):
    def process_item(self, item, spider):
        try:
            existing_product = spider.existing_products[item['vpn']]
            # existing_product = spider.existing_products[spider.existing_products.keys()[0]]
        except KeyError:
            raise DropItem("%s (%s)" % (item['title'], item['vpn']))

        if item['vpn'] not in spider.existing_products.keys():
            raise DropItem("%s (%s)" % (item['title'], item['vpn']))

        for key in existing_product.keys():
            item.fields[key] = scrapy.Field()
            item[key] = existing_product[key]

        return item
