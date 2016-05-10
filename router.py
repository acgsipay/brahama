#!/usr/bin/python
# -*- coding: utf-8 -*-
from utils import router

from source.v1.router import routes as routes_v1

routes = []

routes += router('/api/v1/', routes_v1)