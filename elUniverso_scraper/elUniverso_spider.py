from scrapy.spiders import Spider
from scrapy.item import Item, Field
from scrapy.selector import Selector
from scrapy.loader import ItemLoader 
from scrapy.crawler import CrawlerProcess
from bs4 import BeautifulSoup


class Notice(Item): 
    url = Field()
    headline = Field()
    description = Field()

class ElUniversoSpider(Spider):
    name = "NoticeSpider"
    custom_settings = {
        "USER_AGENT": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36"
    }

    start_urls = ['https://www.eluniverso.com/deportes/']

    def parse(self, response):
        sel = Selector(response)
        notices = sel.xpath('//*[@class="px-2"][3]/div/div/div[1]//ul/li[@class="relative "]')

        for notice in notices:
            item = ItemLoader(Notice(), notice)
            item.add_xpath('headline', './/h2/a/text()')
            item.add_xpath('description', './/p/text()')
            item.add_xpath('url', './/h2/a/@href')

            yield item.load_item()
            
            