import scrapy
from datetime import datetime


class CricketSpider(scrapy.Spider):
    name = "cricket"
    start_urls = [
        'https://indianexpress.com/section/sports/cricket/page/1/',
    ]

    def parse(self, response, **kwargs):
        today_news_end = False
        for news in response.css('div.articles'):
            result = {
                'title': news.css('.title a::text').get(),
                'date': news.css('.date::text').get(),
                'a': news.css('.title a::attr(href)').get(),
            }
            if result['date'].split(',')[0].strip() != datetime.now().strftime('%B %d'):
                today_news_end = True
                break
            request = scrapy.http.Request(
                url=result['a'],
                callback=self.parse_details,
                meta={"result": result}
            )
            yield request

        next_page = response.css('a.next::attr(href)').get()
        if next_page is not None and not today_news_end:
            yield response.follow(next_page, callback=self.parse)

    def parse_details(self, response):
        result = response.meta.get('result')
        lis_of_string = response.css(
            ''' #pcl-full-content>p::text, 
            #pcl-full-content>.ev-meter-content > p::text , 
            .custom-caption+ p::text , 
            .hlt-bot-text p~ p+ p::text , 
            .ev-meter-content .ev-meter-content p::text '''
        ).getall()
        content = '\n\n'.join(lis_of_string)
        image_url = response.css('.custom-caption img::attr(src)').getall()

        for url in image_url:
            if '.jpg' in url:
                image_url = url
                break
        else:
            image_url = image_url[:1]

        result['content'] = content
        result['image_url'] = image_url

        yield dict(result)

