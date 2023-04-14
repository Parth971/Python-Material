import scrapy
from itemloaders import ItemLoader
from scrapy.http.response.html import HtmlResponse

from ..items import QuoteItem, QuoteItemLoader


class AuthorSpider(scrapy.spiders.Spider):
    name = 'author_spider'
    start_urls = ['https://quotes.toscrape.com/']

    def parse(self, response: HtmlResponse, **kwargs):
        loader = QuoteItemLoader(item=QuoteItem(), selector=response.selector)
        loader.add_xpath('name', '//span[@class="text"]/text()')
        loader.add_css('page', 'li.next a::attr(href)')
        yield loader.load_item()

        author_page_links = response.css('.author + a')
        yield from response.follow_all(author_page_links, self.parse_author)

        pagination_links = response.css('li.next a')
        yield from response.follow_all(pagination_links, self.parse)

    def parse_author(self, response: HtmlResponse):
        def extract_with_css(query):
            return response.css(query).get(default='').strip()

        # yield {
        #     'name': extract_with_css('h3.author-title::text'),
        #     'birthdate': extract_with_css('.author-born-date::text'),
        #     'bio': extract_with_css('.author-description::text'),
        # }
