#!/usr/bin/env python
# -*- coding: utf-8 -*-
from sqlalchemy.orm import class_mapper

__author__ = 'mr.S'


class Entity():
    def t(self, attr, editable=False, default=None):
        val = getattr(self, attr)
        if val is None: val = default
        return val

    def as_dict(self, translated=False):
        d = {}
        for c in self.__table__.columns:
            val = self.t(c.name, translated, getattr(self, c.name))
            d[c.name] = str(val) if val is not None else ''
        return d

    @classmethod
    def get_by_id(cls, conn, id):
        if isinstance(id, list):
            return conn.query(cls).filter(cls.id.in_(id)).all() if id else []
        else:
            return conn.query(cls).filter(cls.id == id).first()

    @classmethod
    def get_all(cls, conn):
        return conn.query(cls).all()