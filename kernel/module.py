#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'mr.S'
from kernel.server import app
from functools import wraps

modules = []


class Module(object):
    def __init__(self, name, title=None, route="", index=None, is_admin=False, group=""):
        self.name = self.__class__.__name__
        self.name = name
        self.title = title
        self._route = route
        self.index = index if index else route
        self.is_admin = is_admin
        self.group = group
        modules.append(self)
        modules.sort(key=lambda x: x.name)

    def route(self, route, is_index=False, *args, **kargs):
        route = self._route + route
        if is_index:
            self.index = route

        def wrapper(fn):
            return app.route(route, *args, **kargs)(fn)
        return wrapper

    def post(self, route, *args, **kargs):
        def wrapper(fn):
            return app.post(self._route + route, *args, **kargs)(fn)
        return wrapper

    def get(self, route, *args, **kargs):
        def wrapper(fn):
            return app.get(self._route + route, *args, **kargs)(fn)
        return wrapper