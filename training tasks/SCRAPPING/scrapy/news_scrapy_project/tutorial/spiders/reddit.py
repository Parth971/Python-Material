import scrapy


class RedditSpider(scrapy.Spider):
    name = 'reddit'
    start_urls = [
        'https://www.reddit.com'
    ]

    def parse(self, response, **kwargs):
        links = response.xpath('//img/@src')
        html = ''

        for link in links:
            url = link.get()
            if any(extension in url for extension in ['.jpg', '.gif', '.png']) \
                    and not any(domain in url for domain in ['redditstatic.com', 'redditmedia.com']):
                html += f'''
                        < a href="{url}" target="_blank">
                             < img src="{url}" height="33%" width="33%" />
                        < /a>'''

                with open('frontpage.html', 'a') as page:
                    page.write(html)
                    page.close()


