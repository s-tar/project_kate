#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'mr.S'

from entities.entity import Entity
from kernel.db import Base
from kernel.translator import translatable
from sqlalchemy import Column, Integer, String, Text, Boolean, DateTime
import datetime

class News(Base, Entity):
    __tablename__ = 's_news'
    id = Column(Integer, primary_key=True)
    title = Column(String(255))
    text = Column(Text())
    datetime = Column(DateTime(), default=datetime.datetime.now())
    visible = Column(Boolean(create_constraint=False), default=True)



    @staticmethod
    def get_all(conn):
        return conn.query(News).order_by(News.datetime.desc()).all()

    @staticmethod
    def get_visible(conn):
        return conn.query(News).filter(News.visible == True).order_by(News.datetime.desc()).all()

translatable(News, ['title', 'text'])