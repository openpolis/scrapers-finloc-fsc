# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class FscItem(scrapy.Item):
    nome = scrapy.Field()
    codice_minint_fl = scrapy.Field()
    anno = scrapy.Field()


class FscItem2019(FscItem):
    prelievo_su_imu = scrapy.Field()
    fsc_totale = scrapy.Field()
    fsc_netto = scrapy.Field()


class FscItem2018(FscItem):
    riparto_pereq_art_1 = scrapy.Field()
    riparto_pereq_fabb = scrapy.Field()
    fsc_riparto_pereq_45 = scrapy.Field()
    fsc_riparto_pereq_100 = scrapy.Field()
