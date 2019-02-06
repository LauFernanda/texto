# -*- coding: utf-8 -*-
import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.spiders import BaseSpider
from scrapy.linkextractors import LinkExtractor
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
import re
import lxml.etree
import lxml.html

class EspectadorCCspider(BaseSpider):
    name = 'espectador CC'
    start_urls = ['http://www.eltiempo.com/archivo/buscar?q=cultura+ciudadana&producto=eltiempo&pagina=%d&orden=reciente' % page for page in xrange(1,57561)]
    def parse(self, response):
        for href in response.css('.bread_crumb a::attr(href)'): #Para cada link en el css
            full_url = response.urljoin(href.extract())#extraiga la url
            yield scrapy.Request(full_url, callback=self.parse_question) #ejecute en esa url la función que le voy a pasar como parámetro

    def parse_question(self, response):
        root = lxml.html.fromstring(response.css('.columna_articulo').extract()[0])
        yield {
            'titulo': response.css('.articleHeadline::text').extract()[0], 
            'lead': response.css('.description::text').extract()[0],
            'body': lxml.html.tostring(root, method="text", encoding=unicode),
            'fecha':  response.css('.ico-time::text').extract()[0],
            'compartido':response.css('.text_redes::text').extract()[0],
            'link': response.url,
        }
