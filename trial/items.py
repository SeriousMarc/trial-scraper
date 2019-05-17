import scrapy
import re
from scrapy.loader import ItemLoader
from scrapy.loader.processors import (
    TakeFirst, Join, Compose, Identity
)

class ProductItem(scrapy.Item):
    name = scrapy.Field()
    brand = scrapy.Field()
    category = scrapy.Field()
    images = scrapy.Field()
    price = scrapy.Field()
    sale_price = scrapy.Field()

def string_to_number(_str):
    print('STRRRRRRR----------', _str)
    _str = ''.join(re.findall(r'\d+', _str))
    if _str.isdigit():
        return int(_str)
    return None

class ProductLoader(ItemLoader):
    default_item_class = ProductItem
    default_input_processor = TakeFirst()

    # name_out = Compose(str.title)
    # name_out = Compose(str.upper)
    category_in = Identity()
    category_out = Join('>>')
    price_out = Compose(string_to_number)

    # sale_price_out = Compose()

    

    def get_collected_values(self, field_name):
        return (self._values[field_name]
                if field_name in self._values
                else self._values.default_factory())


    def add_fallback_xpath(self, field_name, xpath, *processors, **kw):
        if not any(self.get_collected_values(field_name)):
            self.add_xpath(field_name, xpath, *processors, **kw)