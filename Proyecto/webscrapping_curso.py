"""
OBJETIVO: 
    - Extraer informacion sobre los productos en la pagina de Mercado Libre Mascotas
    - Aprender a realizar extracciones verticales y horizontales utilizando reglas
CREADO POR: LEONARDO KUFFO
ULTIMA VEZ EDITADO: 28 FEBRERO 2023
"""
from scrapy.item import Field
from scrapy.item import Item
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from scrapy.loader import ItemLoader
from bs4 import BeautifulSoup

from itemloaders.processors import MapCompose

class Vehiculo(Item):
    name = Field()
    precio = Field()
    kilometraje = Field()
    transmision = Field()
    motor = Field()
    combustible = Field()
    vendedor = Field()
    region = Field()
    comuna = Field()
    

class ChileAutosCrawler(CrawlSpider):
    name = 'chileautos'

    custom_settings = {
      'USER_AGENT': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 13_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.6613.120 Safari/537.36',
      'CLOSESPIDER_PAGECOUNT': 10000 # Numero maximo de paginas en las cuales voy a descargar items. Scrapy se cierra cuando alcanza este numero
    }

    # Utilizamos 2 dominios permitidos, ya que los articulos utilizan un dominio diferente
    allowed_domains = ['www.chileautos.cl', 'chileautos.cl']

    start_urls = ['https://www.chileautos.cl/vehiculos/autos-veh%C3%ADculo/']

    download_delay = 3

    # Tupla de reglas
    rules = (
        Rule( # REGLA #1 => HORIZONTALIDAD POR PAGINACION
            LinkExtractor(
                allow=r'/?offset=\d+' # Patron en donde se utiliza "\d+", expresion que puede tomar el valor de cualquier combinacion de numeros /?offset=36
            ), follow=True),
        Rule( # REGLA #2 => VERTICALIDAD AL DETALLE DE LOS PRODUCTOS
            LinkExtractor(
                allow=r'/vehiculos/detalles/' 
            ), follow=True, callback='parse_items'), # Al entrar al detalle de los productos, se llama al callback con la respuesta al requerimiento
    )

    def parse_items(self, response):

        item = ItemLoader(Vehiculo(), response)
        
        # Utilizo Map Compose con funciones anonimas
        # PARA INVESTIGAR: Que son las funciones anonimas en Python?
        item.add_xpath('name', '//div[@class="col features-item-value features-item-value-vehculo"]/text()', MapCompose(lambda i: i.replace('\n', ' ').replace('\r', ' ').strip()))
        item.add_xpath('precio', '//div[@class= "col features-item-value features-item-value-precio"]/text()', MapCompose(lambda i: i.replace('\n', ' ').replace('\r', ' ').strip()))
        item.add_xpath('kilometraje', '//div[@class= "col features-item-value features-item-value-kilmetros"]/text()', MapCompose(lambda i: i.replace('\n', ' ').replace('\r', ' ').strip()))
        item.add_xpath('transmision', '//div[@class="col features-item-value features-item-value-transmisin-tipo-de-transmisin"]/text()', MapCompose(lambda i: i.replace('\n', ' ').replace('\r', ' ').strip()))
        item.add_xpath('motor', '//div[@class="col features-item-value features-item-value-litros-motor"]/text()', MapCompose(lambda i: i.replace('\n', ' ').replace('\r', ' ').strip()))
        item.add_xpath('vendedor', '//span[@class="adtype-value"]/text()', MapCompose(lambda i: i.replace('\n', ' ').replace('\r', ' ').strip()))
        item.add_xpath('region', '//div[@class="col features-item-value features-item-value-regin"]/text()', MapCompose(lambda i: i.replace('\n', ' ').replace('\r', ' ').strip()))
        item.add_xpath('comuna', '//div[@class="col features-item-value features-item-value-comuna"]/text()', MapCompose(lambda i: i.replace('\n', ' ').replace('\r', ' ').strip()))
        item.add_xpath('comuna', '//div[@class="col features-item-value features-item-value-combustible-tipo-de-combustible-primario"]/text()', MapCompose(lambda i: i.replace('\n', ' ').replace('\r', ' ').strip()))


        yield item.load_item()

# EJECUCION
# scrapy runspider 2_mercadolibre.py -o mercado_libre.json