#!/usr/bin/python
# -*- coding: utf-8 -*-
import tornado.web

from tools.cache import Cache
from tools.soap.SipayPlus import SipayEcommerce
from tools.logging import Logger

class Application(tornado.web.Application):
    def __init__(self, *args, **kwargs):
        super(Application, self).__init__(*args, **kwargs)

        self.__dict__['logger'] = Logger(mainlog=kwargs['log.file.main'], errorlog=kwargs['log.file.error'], debug=kwargs['debug'])
        self.__dict__['memcache'] = Cache(kwargs['memcached.host'], kwargs['memcached.port'], Cache.ENGINE_MEMCACHE, expiration=kwargs['memcached.expiration'])
        self.__dict__['soap.sipay_ecommerce'] =  SipayEcommerce()
