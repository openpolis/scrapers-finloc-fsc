# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import csv
from fsc.items import FscItem2019, FscItem2018

class FscTransformationPipeline(object):
    def process_item(self, item, spider):
        return item


class CSVEmitterPipeline(object):
    file = None
    csv_writer = None

    def open_spider(self, spider):
        if spider.csv_file:
            self.file = open(spider.csv_file, 'w')
            if spider.year == '2019':
                fields = list(FscItem2019.fields.keys())
            elif spider.year == '2018':
                fields = list(FscItem2018.fields.keys())
            else:
                raise Exception(f"Year not supported: {spider.year}")

            self.csv_writer = csv.DictWriter(
                self.file, fieldnames=fields
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
