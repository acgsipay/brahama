#!/usr/bin/python
# -*- coding: utf-8 -*-
import os
import sys
import ssl

from tornado.ioloop import IOLoop
from tornado.httpserver import HTTPServer
from tornado.options import options

from app import Application
from settings import params
from router import routes

if __name__ == '__main__':
    application = Application(routes, **settings)

    ssl_options = {
        "certfile": os.path.join(settings['vault_path'], 'sipay.cert.crt'),
        "keyfile": os.path.join(settings['vault_path'], 'sipay.key.pem'),
        "ca_certs": os.path.join(settings['vault_path'], 'sipay.ca.crt'),
        "cert_reqs": ssl.CERT_NONE
    }

    http_server = HTTPServer(application, ssl_options=ssl_options, xheaders=True)

    http_server.listen(options.port)

    IOLoop.instance().start()