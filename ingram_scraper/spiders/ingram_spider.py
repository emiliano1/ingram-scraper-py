# -*- coding: utf-8 -*-
import scrapy
import json
import csv
from pprint import pprint

from ingram_scraper.items import IngramItem


class IngramSpider(scrapy.Spider):
    name = 'ingram'

    def __init__(self, name=None, **kwargs):
        super(IngramSpider, self).__init__(name, **kwargs)

        self.load_csv('NEW.csv')
        # self.load_csv('TEST.csv')
        # pprint(self.existing_products)

        self.url = 'https://be.ingrammicro.com/_layouts/CommerceServer/IM/SearchService.svc/Search'

    def generate_request(self, page):
        # 9931 pages in total
        search_data = {
            'request': {
                'PageLayout': 0,
                'ExchangeRate': None,
                'State': 'PNavDS=N:0&mnc=true',
                'Mode': 12,
                'Keywords': '',
                'Page': 0,
                'Term': page
            }
        }

        request = scrapy.Request(
            url=self.url,
            callback=self.parse,
            method='POST',
            body=json.dumps(search_data),
            headers={'Content-Type': 'application/json'})
        request.meta['page'] = page

        return request

    def start_requests(self):
        yield self.generate_request(1)

    def parse(self, response):
        jsonresponse = json.loads(response.body_as_unicode())

        products = jsonresponse['SearchResult']['ProductSummary']['Data']['Products']

        page = response.meta['page']
        len_products = len(products)
        print('Page {0}: {1} products'.format(page, len_products))

        # print '== PRODUCTS =='
        # pprint(products)
        # print '== PRODUCTS =='

        for product_attrs in products:
            image_urls = [url for url in product_attrs['ImageGalleryURLHigh'] if not url.startswith('/')]

            attrs = {
                'title': product_attrs['Title'],
                'description': product_attrs['Description'],
                'image_urls': image_urls,
                'category': product_attrs['Category'],
                'sub_category': product_attrs['SubCategory'],
                'vpn': product_attrs['Vpn'],
                'product_id': product_attrs['ProductId'],
                'url': 'https://be.ingrammicro.com/_layouts/CommerceServer/IM/ProductDetails.aspx?id={0}'.format(product_attrs['ProductId']),
            }

            yield IngramItem(attrs)

        if len_products >= 10:
            yield self.generate_request(page + 1)

    def load_csv(self, filepath):
        self.existing_products = {}

        with open(filepath, 'rb') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                product = {}
                for column in row:
                    if len(column) == 0: continue
                    product[column] = row[column].strip()

                vpn = product['VPN']
                if vpn in self.existing_products: continue

                self.existing_products[vpn] = product

