# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class FscItem(scrapy.Item):
    prelievo_su_imu = scrapy.Field()
    fsc_totale = scrapy.Field()
    fsc_netto = scrapy.Field()

    # codice ente
    codice_minint_fl = scrapy.Field()
    nome = scrapy.Field()

    # anno
    anno = scrapy.Field()
