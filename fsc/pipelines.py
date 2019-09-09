# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import csv


class FscTransformationPipeline(object):
    def process_item(self, item, spider):
        return item


class CSVEmitterPipeline(object):
    file = None
    csv_writer = None

    def open_spider(self, spider):
        if spider.csv_file:
            self.file = open(spider.csv_file, 'w')
            self.csv_writer = csv.DictWriter(
                self.file, fieldnames=['nome', 'codice_minint_fl', 'anno', 'fsc_totale', 'prelievo_su_imu', 'fsc_netto']
            )
            self.csv_writer.writeheader()

    def close_spider(self, spider):
        if spider.csv_file:
            self.file.close()

    def process_item(self, item, spider):
        if spider.csv_file:
            self.csv_writer.writerow(dict(item))
            self.file.flush()
        return item
