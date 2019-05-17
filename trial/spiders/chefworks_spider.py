import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from scrapy.crawler import CrawlerProcess
from trial.items import ProductLoader


class ChefSpider(CrawlSpider):
    name = 'chef'
    allowed_domains = ['chefworks.com.au']
    start_urls = ['https://www.chefworks.com.au']
    deny_urls = ('best-sellers', 'new', 'urban-collection', )

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

        i.add_css('name', 'h1::text')
        i.add_xpath(
            'brand', 
            "//div[@id='specifications']//strong[contains(., 'Brand')]/../\
                following-sibling::td/text()"
        )
        i.add_xpath('category', "//ul[@class='breadcrumb']/li[2]/a/@href")
        i.add_xpath('price', "//div[@class='productprice productpricetext']/text()")
        
        # there is no sale price value on chefworks, set default
        i.add_value('sale_price', None)
        
        image_urls = response.xpath("//div[@id='_jstl__images_r']//a/@href").extract()
        i.add_value('image_urls', self.join_links(image_urls, response))

        self.logger.info('Parse function called on %s', response.url)
        yield i.load_item()

    def join_links(self, urls, response):
        links = [response.urljoin(url) for url in urls]
        return links


# run scrapy from the script
# process = CrawlerProcess()
# process.crawl(ChefSpider)
# process.start()