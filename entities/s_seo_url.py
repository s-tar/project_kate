#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'mr.S'

from kernel.db import Base
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship, backref
from entities.s_seo_tag import SEOTag


class SEOUrl(Base):
    __tablename__ = 's_seo_url'
    seou_id = Column(Integer, primary_key=True)
    seou_url = Column(String(255))

    tags = relationship(SEOTag, cascade="delete", backref=backref('url'), uselist=True)

    @staticmethod
    def list_all(conn):
        return conn.query(SEOUrl).all()

    @staticmethod
    def list_all_ordered(conn):
        return conn.query(SEOUrl).order_by(SEOUrl.seou_url.desc()).all()

    @staticmethod
    def get_by_id(conn, id):
        return conn.query(SEOUrl).filter(SEOUrl.seou_id == id).first()

    @staticmethod
    def get_by_url(conn, url):
        return conn.query(SEOUrl).filter(SEOUrl.seou_url == url).first()
