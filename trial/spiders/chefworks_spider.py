import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor

from trial.items import ProductItem

class MySpider(CrawlSpider):
    name = 'chefworks'
    allowed_domains = ['chefworks.com.au']
    start_urls = ['https://www.chefworks.com.au']

    # start_urls = [
    #     'https://www.chefworks.com.au/chef-jackets/',
    #     'https://www.chefworks.com.au/aprons/',
    #     'https://www.chefworks.com.au/chef-pants/',
    #     'https://www.chefworks.com.au/shirts/',
    #     'https://www.chefworks.com.au/headwear/',
    #     'https://www.chefworks.com.au/accessories/'
    # ]


    rules = (
        Rule(LinkExtractor(allow=('', ))),
        Rule(
            LinkExtractor(allow=r'questions\?page=[0-9]&sort=newest'),
            callback='parse_item', 
            follow=True
        ),
    )
    

    def parse_item(self, response):
        questions = response.xpath('//div[@class="summary"]/h3')

        for question in questions:
            item = ProductItem()
            item['name'] = question.xpath(
                'a[@class="question-hyperlink"]/@href').extract()[0]
            item['brand'] = question.xpath(
                'a[@class="question-hyperlink"]/text()').extract()[0]
            print(item)
            yield item