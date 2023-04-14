# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class ScrapyProjectItem(scrapy.Item):
    # define the fields for your item here like:
    title = scrapy.Field()
    author = scrapy.Field()
    tag = scrapy.Field()


class AmazonItem(scrapy.Item):
    # define the fields for your item here like:
    product_title = scrapy.Field()
    product_rating = scrapy.Field()
    product_price = scrapy.Field()
    product_image_link = scrapy.Field()
