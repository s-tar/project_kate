#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'mr.S'

from kernel.db import Base
from entities.entity import Entity
from sqlalchemy import Column, Integer, Text, ForeignKey


class SEOTag(Base, Entity):
    __tablename__ = 's_seo_tag'
    seot_id = Column(Integer, primary_key=True)
    seot_text = Column(Text())
    seou_id = Column(Integer, ForeignKey('s_seo_url.seou_id'))


    @staticmethod
    def get_by_id(conn, id):
        return conn.query(SEOTag).filter(SEOTag.seot_id == id).first()