import scrapy
from ..items import ScrapyProjectItem
from scrapy.http import FormRequest
from scrapy.utils.response import open_in_browser

class QuotesSpider(scrapy.Spider):
    name = 'quotes'
    page_number = 2
    start_urls = [
        'https://quotes.toscrape.com/login',
    ]

    def parse(self, response):
        token = response.css('form input::attr(value)').extract_first()
        return FormRequest.from_response(
            response,
            formdata={
                'csrf_token': token,
                'username': 'parth',
                'password': 'parth123'
            },
            callback=self.start_scraping
        )

    def start_scraping(self, response):
        open_in_browser(response)
        items = ScrapyProjectItem()

        all_div_quotes = response.css('div.quote')

        for quote in all_div_quotes:
            items['title'] = quote.css('span.text::text').extract()
            items['author'] = quote.css('.author::text').extract()
            items['tag'] = quote.css('.tag::text').extract()

            yield items

        next_page = f'https://quotes.toscrape.com/page/{QuotesSpider.page_number}/'

        if QuotesSpider.page_number < 11:
            QuotesSpider.page_number += 1
            yield response.follow(next_page, callback=self.start_scraping)
