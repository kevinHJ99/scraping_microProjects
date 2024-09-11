from scrapy.spiders import Spider
from scrapy.item import Item, Field
from scrapy.selector import Selector
from scrapy.loader import ItemLoader 
from scrapy.crawler import CrawlerProcess

class Quote(Item): 
    id = Field()
    url = Field()
    quote = Field()
    description = Field()

class StackOverflowSpider(Spider):
    name = "MySpider"
    custom_settings = {
        "USER_AGENT": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36"
    }

    start_urls = ['https://stackoverflow.com/questions']

    def parse(self, response):
        sel = Selector(response)
        quotes = sel.xpath('//*[@id="questions"]//div[@class="s-post-summary    js-post-summary"]')

        for quote in quotes:
            item = ItemLoader(Quote(), quote)
            item.add_xpath('description', './/div[@class="s-post-summary--content-excerpt"]/text()')
            item.add_xpath('quote', './/h3/a/text()')
            item.add_xpath('url', './/h3/a/@href')
            item.add_value('id', 1)

            yield item.load_item()
            

#comando para ejecutar scrapy
# scrapy runspider practice_1.py -o output.csv -t csv
