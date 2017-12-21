# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import urllib

from pymongo import MongoClient
from scrapy.conf import settings

MONGODB_HOST = settings.get("MONGODB_HOST")
MONGODB_PORT = settings.get("MONGODB_PORT")
MONGODB_PWD = settings.get("MONGODB_PWD")
MONGODB_USER = settings.get("MONGODB_USER")
MONGODB_DB = settings.get("MONGODB_DB")
IMAGE_PATH = settings.get("IMAGE_PATH")

mongo = MongoClient(
    host=MONGODB_HOST,
    port=MONGODB_PORT
)
mongo[MONGODB_DB].authenticate(MONGODB_USER, MONGODB_PWD)
db = mongo[MONGODB_DB]
collection = db.UserDetails


class WestartSpiderPipeline(object):
    def process_item(self, item, spider):
        collection.save(item)
        url_arrays = str(item["avatarUrl"]).split("/")
        urllib.urlretrieve(item["avatarUrl"], IMAGE_PATH + url_arrays[len(url_arrays) - 1])
        return item
