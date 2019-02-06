# -*- coding: utf-8 -*-
import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.spiders import BaseSpider
from scrapy.linkextractors import LinkExtractor
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
import re
import lxml.etree
import lxml.html

class EspectadorCCspider(scrapy.Spider):
    name = 'espectador CC'
    starts_urls=['http://www.eltiempo.com/archivo/buscar?q=%22cultura+ciudadana%22&producto=eltiempo&pagina={pagina}'.format(pagina= pagina) for pagina in xrange(1,2000)]
    def parse(self, response):
        for href in response.css('article a::attr(href)'): #Para cada link en el css
            full_url = response.urljoin(href.extract())#extraiga la url
            yield scrapy.Request(full_url, callback=self.parse_question) #ejecute en esa url la función que le voy a pasar como parámetro
               
    def parse_question(self, response):
       # root = lxml.html.fromstring(response.css('.columna_articulo').extract()[0])
        yield {
          #  'titulo': response.css('.articleHeadline::text').extract()[0], 
            #'lead': response.css('.description::text').extract()[0],
            #'body': lxml.html.tostring(root, method="text", encoding=unicode),
            #'fecha':  response.css('.ico-time::text').extract()[0],
            #'compartido':response.css('.text_redes::text').extract()[0],
            'link': response.url,
        }
