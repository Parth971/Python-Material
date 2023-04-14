import scrapy
from itemloaders import ItemLoader
from itemloaders.processors import TakeFirst, MapCompose, Join


class QuoteItem(scrapy.Item):
    name = scrapy.Field()
    page = scrapy.Field()


def remove_quoatation_mark(value):
    return value.replace('“', '').replace('”', '')


def fetch_page_number(value):
    return int(value.split('/')[-2])


class QuoteItemLoader(ItemLoader):
    # default_output_processor = TakeFirst()
    name_in = MapCompose(remove_quoatation_mark)
    # name_out = Join(separator=' | ')
    # page_in = MapCompose(str.strip)
    page_in = MapCompose(fetch_page_number)
    page_out = TakeFirst()


