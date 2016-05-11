#!/usr/bin/python
# -*- coding: utf-8 -*-
from tornado.web import URLSpec


def router(prefix, routes):
    data = []

    for route in routes:
        pattern = route.regex.pattern

        if pattern.startswith('/'):
            pattern = pattern[1:]

        if pattern.endswith('$'):
            pattern = pattern[:-1]

        pattern = r'%s%s' % (prefix, pattern)

        if pattern[-1] == '/':
            pattern += '?'

        data.append(URLSpec(pattern, route.handler_class, kwargs=route.kwargs, name=route.name))

    return data