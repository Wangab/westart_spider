# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
from pymongo import MongoClient
from scrapy.conf import settings

MONGODB_HOST = settings.get("MONGODB_HOST")
MONGODB_PORT = settings.get("MONGODB_PORT")
MONGODB_PWD = settings.get("MONGODB_PWD")
MONGODB_USER = settings.get("MONGODB_USER")
MONGODB_DB = settings.get("MONGODB_DB")

mongo = MongoClient(
    host=MONGODB_HOST,
    port=MONGODB_PORT
)
mongo[MONGODB_DB].authenticate(MONGODB_USER, MONGODB_PWD)
db = mongo[MONGODB_DB]
collection = db.MM_User


class WestartSpiderPipeline(object):
    def process_item(self, item, spider):
        collection.save(item)

        return item
