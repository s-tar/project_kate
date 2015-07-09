#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'mr.S'

from kernel.db import Base
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship, backref


class UserRole(Base):
    __tablename__ = 's_user_role'
    id = Column(Integer, primary_key=True)
    code = Column(String(255))

    user_id = Column(Integer, ForeignKey('s_user.id'))