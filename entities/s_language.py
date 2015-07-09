#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'mr.S'

from kernel.db import Base
from sqlalchemy import Column, Integer, String, Boolean
from entities.entity import Entity

class Language(Base, Entity):
    __tablename__ = 's_language'
    lng_id = Column(Integer, primary_key=True)
    lng_code = Column(String(50))
    lng_name = Column(String(255))
    lng_default = Column(Boolean(create_constraint=False), default=False)
    lng_active = Column(Boolean(create_constraint=False), default=True)

    @staticmethod
    def get_by_id(conn, id):
        return conn.query(Language).filter(Language.lng_id == id).first()

    @staticmethod
    def get_by_code(conn, code):
        return conn.query(Language).filter(Language.lng_code == code).first()

    @staticmethod
    def get_default(conn):
        return conn.query(Language).filter(Language.lng_default == True).first()


    @staticmethod
    def list_active(conn):
        return conn.query(Language).filter(Language.lng_active == True).order_by(Language.lng_default.desc(), Language.lng_name).all()

    @staticmethod
    def list_all(conn):
        return conn.query(Language).order_by(Language.lng_name).all()