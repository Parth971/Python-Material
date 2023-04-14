from scrapy.spiders import CSVFeedSpider


class CsvSpider(CSVFeedSpider):
    name = 'csv_spider'
    allowed_domains = ['stats.govt.nz']
    start_urls = [
        'https://www.stats.govt.nz/assets/Uploads/Annual-enterprise-survey/Annual-enterprise-survey-2021-financial-year-provisional/Download-data/annual-enterprise-survey-2021-financial-year-provisional-csv.csv'
    ]
    # delimiter = ','
    # quotechar = "'"
    total = 0
    headers = [name.strip() for name in "Year, Industry_aggregation_NZSIOC, Industry_code_NZSIOC, Industry_name_NZSIOC, Units, Variable_code, Variable_name, Variable_category, Value, Industry_code_ANZSIC06".split(',')]

    def parse_row(self, response, row):
        if self.total == 10:
            CsvSpider.close(self, 'More than 10 rows')
            return
        self.total += 1
        return row
