#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'mr.S'

from kernel.db import Base
from entities.entity import Entity
from sqlalchemy import Column, Integer, String, Text, desc
from bottle import request
from kernel.translator import translatable

class Content(Base, Entity):
    __tablename__ = 's_content'
    id = Column(Integer, primary_key=True)
    alias = Column(String(255))
    name = Column(String(255))
    text = Column(Text())

    @staticmethod
    def list_all(conn):
        return conn.query(Content).all()

    @classmethod
    def get_by_id(cls, conn, id):
        return conn.query(Content).filter(Content.id == id).first()

    @staticmethod
    def get_by_alias(conn, alias):
        return conn.query(Content).filter(Content.alias == alias).first()

translatable(Content, ['name', 'text'])