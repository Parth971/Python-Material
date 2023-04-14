from scrapy.http import HtmlResponse
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule


class QuoteCrawlSpider(CrawlSpider):
    name = "quote_crawl_spider"
    allowed_domains = ["quotes.toscrape.com"]
    start_urls = ["https://quotes.toscrape.com/"]

    rules = (
        Rule(
            LinkExtractor(
                allow=('/author/',)
            ),
            callback="parse_author",
            follow=True,
            process_links='process_links__'
        ),
        Rule(
            LinkExtractor(
                allow=('quotes.toscrape.com/page/',),
                deny=('quotes.toscrape.com/page/1/',),
            ),
            process_links='process_links_'
        ),
    )

    def process_links_(self, x):
        return x

    def process_links__(self, x):
        return x

    def parse_author(self, response: HtmlResponse):
        def extract_with_css(query):
            return response.css(query).get(default='').strip()

        yield {
            'name': extract_with_css('h3.author-title::text'),
            'birthdate': extract_with_css('.author-born-date::text'),
            'bio': extract_with_css('.author-description::text'),
        }
        response.css('.quote >span, .tags>meta').xpath('@class').get()
