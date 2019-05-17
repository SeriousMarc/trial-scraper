import scrapy
from scrapy.loader import ItemLoader
from scrapy.loader.processors import (
    TakeFirst, Join, Compose, MapCompose, Identity
)
from .utils import (
    string_to_number, replace_slash, get_first_if_exists
)


class ProductItem(scrapy.Item):
    name = scrapy.Field()
    brand = scrapy.Field()
    category = scrapy.Field()
    images = scrapy.Field()
    image_urls = scrapy.Field()
    price = scrapy.Field()
    sale_price = scrapy.Field()


class ProductLoader(ItemLoader):
    default_item_class = ProductItem
    default_output_processor = TakeFirst()

    name_in = Compose(get_first_if_exists, str.title)
    brand_in = Compose(get_first_if_exists, str.upper)
    category_in = MapCompose(replace_slash)
    category_out = Join('>>')
    price_out = Compose(get_first_if_exists, string_to_number)
    sale_price_out = Compose(get_first_if_exists, string_to_number)
    image_urls_out = Identity()
    
    def get_collected_values(self, field_name):
        return (self._values[field_name]
                if field_name in self._values
                else self._values.default_factory())


    def add_fallback_xpath(self, field_name, xpath, *processors, **kw):
        if not any(self.get_collected_values(field_name)):
            self.add_xpath(field_name, xpath, *processors, **kw)