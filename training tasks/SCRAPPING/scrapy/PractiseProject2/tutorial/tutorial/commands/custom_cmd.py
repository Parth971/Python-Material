from scrapy.commands import ScrapyCommand


class Command(ScrapyCommand):
    requires_project = True
    default_settings = {"LOG_ENABLED": False}

    def short_desc(self):
        return "List available spiders"

    def run(self, args, opts):
        print('############### Started custom command ###############')
        print(f"args: {args}")
        print(f"opts: {opts}")
        print('\nPrinting list of spider available:')
        for count, spider_name in enumerate(self.crawler_process.spider_loader.list()):
            print(f"{count+1}. {spider_name}")

