#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'mr.S'

from kernel.db import Base
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship, backref

class Community(Base):
    __tablename__ = 's_community'
    id = Column(Integer, primary_key=True)
    alias = Column(String(50))
    name = Column(String(50))