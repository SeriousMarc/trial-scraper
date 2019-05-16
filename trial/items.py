import scrapy


class ProductItem(scrapy.Item):
    name = scrapy.Field()
    brand = scrapy.Field()
    category = scrapy.Field()
    images = scrapy.Field()
    price = scrapy.Field()
    sale_price = scrapy.Field()
