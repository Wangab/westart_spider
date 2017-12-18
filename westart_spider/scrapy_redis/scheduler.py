#!/usr/bin/python
#-*-coding:utf-8-*-

import redis
from scrapy.utils.misc import load_object
from .dupefilter import RFPDupeFilter


# default values
REDIS_HOST = '127.0.0.1'
REDIS_PORT = 6379
REDIS_POOL_MAX = 10
REDIS_DB = 0
SCHEDULER_PERSIST = False
QUEUE_KEY = '%(spider)s:requests'
QUEUE_CLASS = '.queue.SpiderQueue'



class Scheduler(object):
    """Redis-based scheduler"""

    def __init__(self, server, persist, queue_key, queue_cls, dupefilter):
        """Initialize scheduler.

        Parameters
        ----------
        server : Redis instance
        persist : bool
        queue_key : str
        queue_cls : queue class
        dupefilter_key : str
        """
        self.server = server
        self.persist = persist
        self.queue_key = queue_key
        self.queue_cls = queue_cls
        self.df = dupefilter

    def __len__(self):
        return len(self.queue)

    @classmethod
    def from_settings(cls, settings):
        host = settings.get('REDIS_HOST', REDIS_HOST)
        port = settings.get('REDIS_PORT', REDIS_PORT)
        db = settings.get('REDIS_DB', REDIS_DB)
        max_connet = settings.get('REDIS_POOL_MAX', REDIS_POOL_MAX)
        dupefilter_cls = load_object(settings['DUPEFILTER_CLASS'])
        persist = settings.get('SCHEDULER_PERSIST', SCHEDULER_PERSIST)
        queue_key = settings.get('SCHEDULER_QUEUE_KEY', QUEUE_KEY)
        queue_cls = load_object(settings.get('SCHEDULER_QUEUE_CLASS', QUEUE_CLASS))
        redis_poll = redis.ConnectionPool(host=host, port=port, db=db, max_connections=max_connet)
        server = redis.Redis(connection_pool=redis_poll,socket_keepalive=5,socket_connect_timeout=30,socket_timeout=30)
        dupefilter = dupefilter_cls.from_settings(settings)
        return cls(server, persist, queue_key, queue_cls, dupefilter)

    @classmethod
    def from_crawler(cls, crawler):
        settings = crawler.settings
        cls.stats = crawler.stats
        return cls.from_settings(settings)

    def open(self, spider):
        """
            execute this function when open one spider
        """
        self.spider = spider
        self.queue = self.queue_cls(self.server, spider, self.queue_key)
        # notice if there are requests already in the queue to resume the crawl
        if len(self.queue):
            spider.log("Resuming crawl (%d requests scheduled)" % len(self.queue))

    def close(self, reason):
        pass

    def enqueue_request(self, request):
        if not request.dont_filter and self.df.request_seen(request):
            return
        self.queue.push(request)

    def next_request(self):
        request = self.queue.pop()
        return request

    def has_pending_requests(self):
        return len(self) > 0
