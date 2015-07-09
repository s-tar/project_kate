#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'mr.S'

from sqlalchemy import create_engine, Column, Integer, Sequence, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, scoped_session
from kernel.config import config
from functools import wraps
from entities import *
import inspect
from sqlalchemy import event


Base = declarative_base()
url = config['db']['type']+"://"+config['db']['username']+":"+config['db']['password'] + "@"+config['db']['host']+"/"+config['db']['db']+"?charset=utf8"

engine = create_engine(url, echo_pool=True, encoding='utf8', echo=False,
                           pool_recycle=600, pool_size=20, max_overflow=100)


db = sessionmaker(bind=engine, autocommit=False, expire_on_commit=False)()

Base.metadata.create_all(engine)


def new_connection():
    con = sessionmaker(bind=engine, autocommit=False, expire_on_commit=False)()
    return con


class Database(object):
    def __init__(self):
        self._connection = None

    def __call__(self, entity=None):
        if not self._connection:
            self._connection = new_connection()
        if entity:
            if inspect.isclass(entity):
                if hasattr(entity, '__table__'):
                    return EntityWrapper(entity, self._connection)
            else:
                return entity
        return self._connection

    def close(self):
        if self._connection is not None:
            self._connection.close()

    def __getattr__(self, name):
        try:
            return self.__dict__[name]
        except KeyError: pass
        if self._connection:
            return getattr(self._connection, name)

        raise KeyError


class EntityWrapper():
    def __init__(self, entity, connection):
        self._entity = entity
        self._connection = connection

    def __getattr__(self, item):
        attr = getattr(self._entity, item, None)
        if attr:
            if callable(attr):
                @wraps(attr)
                def method(*args, **kwargs):
                    return attr(self._connection, *args, **kwargs)
                return method
        else:
            return attr