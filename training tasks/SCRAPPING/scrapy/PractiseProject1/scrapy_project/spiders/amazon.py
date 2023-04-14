import scrapy
from ..items import AmazonItem


class AmazonSpider(scrapy.Spider):
    name = 'amazon'
    start_urls = [
        'https://www.amazon.com/s?k=phone+case&page=1'
    ]
    page_number = 2

    def parse(self, response, **kwargs):
        items = AmazonItem()

        product_title = response.css('.a-text-normal .a-text-normal').css('::text').extract()
        product_rating = response.css('.aok-align-bottom span').css('::text').extract()
        product_price = response.css('.a-price-whole').css('::text').extract()
        product_image_link = response.css('.sbv-product-img , .s-image').css('::attr(src)').extract()

        items['product_title'] = product_title
        items['product_rating'] = product_rating
        items['product_price'] = product_price
        items['product_image_link'] = product_image_link

        yield items

        next_page = f'https://www.amazon.com/s?k=phone+case&page={AmazonSpider.page_number}'

        if AmazonSpider.page_number <= 20:
            AmazonSpider.page_number += 1
            yield response.follow(next_page, callback=self.parse)
