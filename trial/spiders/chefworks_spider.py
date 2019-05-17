import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from scrapy.loader import ItemLoader

from trial.items import ProductItem, ProductLoader

class MySpider(CrawlSpider):
    name = 'chefworks'
    allowed_domains = ['chefworks.com.au']
    start_urls = ['https://www.chefworks.com.au']
    deny_urls = ('best-sellers', 'womens', 'new', 'urban-collection', )

    rules = (
        Rule(
            LinkExtractor(
                restrict_xpaths=("//ul[@class='nav navbar-nav dmenu']/li/a", ),
                deny=deny_urls
            )
        ),
        Rule(
            LinkExtractor(
                allow='\?pgnum=\d',
                restrict_xpaths=("//i[@class='fa fa-chevron-right']/..", ),
            )
        ),
        Rule(
            LinkExtractor(
                restrict_xpaths=("//div[@itemtype='http://schema.org/Product']/a", ),
            ),
            callback='parse_item'
        ),
    )


    def parse_item(self, response):
        i = ProductLoader(response=response)
        i.add_xpath('category', "//ul[@class='breadcrumb']/li[2]/a/@href")
        i.add_xpath('price', "//div[@class='productprice productpricetext']/text()")
        # category = response.xpath(
        #     '//ul[@class="breadcrumb"]/li[2]/a/@href'
        # ).extract_first().replace('/', '')
        result = i.load_item()
        print('LOADED ITEM-------------:', result)
        from scrapy.shell import inspect_response
        inspect_response(response, self)
        yield i.load_item()

        print('-----------PARSE ITEM')
        questions = []

        for question in questions:
            item = ProductItem()
            yield item