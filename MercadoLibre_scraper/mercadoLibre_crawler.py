from scrapy.spiders import CrawlSpider, Rule
from scrapy.item import Item, Field
from scrapy.selector import Selector
from scrapy.loader import ItemLoader 
from scrapy.loader.processors import MapCompose as mc
from scrapy.linkextractors import LinkExtractor
from scrapy.crawler import CrawlerProcess


class Product(Item): 
    title = Field()
    price = Field()
    description = Field()
    

class MercadoLibreCrawler(CrawlSpider):
    name = "mercadoLibre"
    custom_settings = {
        "USER_AGENT": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36",
    }


    # Reduce el espectro de busqueda de URLs. No nos podemos salir de los dominios de esta lista
    allowed_domains = ['listado.mercadolibre.com.ec', 'articulo.mercadolibre.com.ec']
    
    start_urls = ['https://listado.mercadolibre.com.ec/waflera#D[A:waflera]']

    download_delay = 1 ## evitar un bloqueo del sitio web

    rules = (
        # pagination
        Rule(
            LinkExtractor(
                allow=r'_Desde_\d+'
            ), follow=True
        ),
        # get product
        Rule(
            LinkExtractor(
                allow=r'(/p/MEC\d+|/MEC-\d+)'
            ), follow=True, callback="parse_mercadoLibre"
        ),
    )

    
    def parse_mercadoLibre(self, response):
        item = ItemLoader(Product(), response)

        ## ========//=========
        item.add_xpath('title', '//h1[@class="ui-pdp-title"]/text()')
        item.add_xpath('price', '//meta[@itemprop="price"]/@content')
        item.add_xpath('description', '//*[@class="ui-pdp-description"]/p/text()')

        yield item.load_item()