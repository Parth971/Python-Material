import scrapy
from scrapy.http.response.html import HtmlResponse


class JsonSpider(scrapy.spiders.Spider):
    name = 'json_spider'
    start_urls = ['https://www.7timer.info/bin/astro.php?lon=113.2&lat=23.1&ac=0&unit=metric&output=json&tzshift=0']

    def parse(self, response: HtmlResponse, **kwargs):
        print(response.json())
