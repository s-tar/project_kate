#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'mr.S'

from kernel.db import Base
from sqlalchemy import Column, Integer, String, Text, Boolean, ForeignKey
from sqlalchemy.orm import relationship, backref
from entities.s_user_role import UserRole
from bottle import request
from entities.entity import Entity
from entities.s_language import Language

class Translation(Base, Entity):
    __tablename__ = 's_translation'
    trl_id = Column(Integer, primary_key=True)
    trl_code = Column(String(255))
    trl_text = Column(Text())
    lng_code = Column(String(50), ForeignKey('s_language.lng_code'))
    language = relationship("Language")

    @staticmethod
    def list_by_code(conn, code):
        if type(code) is not list: code = [code]
        return conn.query(Translation).filter(Translation.trl_code.in_(code)).all()