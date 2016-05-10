#!/usr/bin/python
# -*- coding: utf-8 -*-
from uuid import uuid1

from tornado.web import RequestHandler

class BaseHandler(RequestHandler):
    def initialize(self):
        self.uuid = str(uuid1())
        self.container = {}

    @property
    def headers(self):
        return self.request.headers 

    @property
    def remote_ip(self):
        return self.request.remote_ip   

    def prepare(self):
        self.parse()
        self.auth()

    def parse(self):
        self.request.json_arguments = {}

        if "Content-Type" in self.headers and self.headers["Content-Type"].startswith('application/json'):
            try: 
                self.request.json_arguments = json_decode(self.request.body)
            except Exception, e:
                pass

    def get_json_argument(self, name, default=RequestHandler._ARG_DEFAULT, strip=True):
        return self._get_argument(name, default, self.request.json_arguments, strip)

    def get_json_arguments(self, name, strip=True):
        return self._get_arguments(name, self.request.json_arguments, strip)

    def auth(self):
        pass