from scrapy.spiders import CrawlSpider, Rule
from scrapy.item import Item, Field
from scrapy.selector import Selector
from scrapy.loader import ItemLoader 
from scrapy.loader.processors import MapCompose as mc
from scrapy.linkextractors import LinkExtractor
from scrapy.crawler import CrawlerProcess


class Hotel(Item): 
    name = Field()
    description = Field()
    amenities = Field()
    score = Field()

class TripadivisorSpider(CrawlSpider):
    name = "HotelCrawler"
    custom_settings = {
        "USER_AGENT": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36",
        'CLOSESPIDER_ITEMCOUNT': 20,
    }


    # Reduce el espectro de busqueda de URLs. No nos podemos salir de los dominios de esta lista
    allowed_domains = ['tripadvisor.com', 'tripadvisor.co']
    
    start_urls = ['https://www.tripadvisor.co/Hotels-g297476-Cartagena_Cartagena_District_Bolivar_Department-Hotels.html']

    download_delay = 2 ## evitar un bloqueo del sitio web

    rules = (
        Rule(
            LinkExtractor(
                allow=r'/Hotel_Review-'
            ), follow=True, callback="parse_hotel"),
    )

    def parse_hotel(self, response):
        sel = Selector(response)
        item = ItemLoader(Hotel(), sel)

        ## ========//=========
        item.add_xpath('name', '//h1[@id="HEADING"]/text()')
        item.add_xpath('description', '//div[@id="ABOUT_TAB"]//div[@class="fIrGe _T"]//text()')
        item.add_xpath('amenities', '//div[contains(@data-test-target, "amenity_text")]/text()')
        item.add_xpath('score', '//div[@id="ABOUT_TAB"]//*[@class="kJyXc P"]/text()')

        yield item.load_item()