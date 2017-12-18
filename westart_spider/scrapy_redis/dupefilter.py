#!/usr/bin/python
#-*-coding:utf-8-*-

import time
import redis
from scrapy.dupefilters import BaseDupeFilter

# default values
REDIS_HOST = '127.0.0.1'
REDIS_PORT = 6379
REDIS_POOL_MAX = 10
REDIS_DB = 0
SCHEDULER_PERSIST = False
QUEUE_KEY = '%(spider)s:requests'
QUEUE_CLASS = '.queue.SpiderQueue'
COUNT_UPDATE_KEY = "spider_update_count"


class RFPDupeFilter(BaseDupeFilter):

    def __init__(self, server, key):
        """Initialize duplication filter
        Parameters
        ----------
        server : Redis instance
        key : str
            Where to store fingerprints
        """
        self.server = server
        self.key = key

    @classmethod
    def from_settings(cls, settings):
        host = settings.get('REDIS_HOST', REDIS_HOST)
        port = settings.get('REDIS_PORT', REDIS_PORT)
        db = settings.get('REDIS_DB', REDIS_DB)
        max_connet = settings.get('REDIS_POOL_MAX', REDIS_POOL_MAX)
        key = "dupefilter:%s" % int(time.time())
        dupefilter_key = settings.get('DUPEFILTER_KEY', key)
        redis_poll = redis.ConnectionPool(host=host, port=port, db=db, max_connections=max_connet)
        server = redis.Redis(connection_pool=redis_poll, socket_keepalive=5, socket_connect_timeout=30, socket_timeout=30)

        return cls(server, dupefilter_key)

    def request_seen(self, request):
        """
            use sismember judge whether fp is duplicate.
        """
        fp = request.url
        try:
            if self.server.exists("dupefilter:{0}".format(fp)):
                return True
            self.server.set("dupefilter:{0}".format(fp), 1)
            self.server.expire("dupefilter:{0}".format(fp),3600 * 24 * 30)
            return False
        except Exception as e:
            return False

    def close(self, reason):
        pass
        """Delete data on close. Called by scrapy's scheduler"""
        # self.clear()


