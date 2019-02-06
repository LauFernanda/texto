# -*- coding: utf-8 -*-
import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
import re
import lxml.etree
import lxml.html

class EspectadorCCspider(scrapy.Spider):
    name = 'espectador CC'
    start_urls = [
         'http://www.elespectador.com/tags/cultura-ciudadana',
         'http://www.elespectador.com/tags/cultura-ciudadana-bogota'
    ]
    def parse(self, response):
        for href in response.css('.article::attr(href)'): #Para cada link en el css
            full_url = response.urljoin(href.extract())#extraiga la url
            yield scrapy.Request(full_url, callback=self.parse_question) #ejecute en esa url la función que le voy a pasar como parámetro

    def parse_question(self, response):
        root = lxml.html.fromstring(response.css('.content_nota').extract()[0])
        comentarios=[]
        for comentario in response.css('.una_opinion'):
			autor=comentario.css('h2::text').extract()[0]
			texto=comentario.css('.txt_opinion::text').extract()[0]
			comentarios.append({'autor':autor,'texto':texto})
        yield {
            'titulo': response.css('.titulo::text').extract()[0], 
            'lead': response.css('.lead::text').extract()[0],
            'body': lxml.html.tostring(root, method="text", encoding=unicode),
            'tags': response.css('.tag-no-vacio::text').extract(),
            'fecha':  response.css('.hora::text').extract()[0],
            'compartido':response.css('.compartido_total::text').extract()[0],
            'comentarios':comentarios,
            'link': response.url,
        }
