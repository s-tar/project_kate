#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'mr.S'

from kernel.db import Base
from sqlalchemy import Column, Integer, String, Text
from entities.entity import Entity
from kernel.translator import translatable

class Dictionary(Base, Entity):
    __tablename__ = 's_dictionary'
    id = Column(Integer, primary_key=True)
    code = Column(String(255))
    text = Column(Text())


    @staticmethod
    def get_by_code(conn, code):
        return conn.query(Dictionary).filter(Dictionary.code == code).first()


    @staticmethod
    def list_by_code(conn, code):
        if type(code) is not list: code = [code]
        return conn.query(Dictionary).filter(Dictionary.code.in_(code)).all()

    @staticmethod
    def list_all(conn):
        return conn.query(Dictionary).order_by(Dictionary.code).all()


translatable(Dictionary, ['text'])