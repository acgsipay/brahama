#!/usr/bin/python
# -*- coding: utf-8 -*-
import tornado.web


class Application(tornado.web.Application):
    def __init__(self, *args, **kwargs):
        super(Application, self).__init__(*args, **kwargs)
