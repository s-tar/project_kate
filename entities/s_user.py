#!/usr/bin/env python
# -*- coding: utf-8 -*-
from bottle import request

__author__ = 'mr.S'

from kernel.db import Base
from sqlalchemy import Column, Integer, String, func, ForeignKey
from sqlalchemy.orm import relationship, backref
from entities.s_user_role import UserRole
from entities.entity import Entity

class User(Base, Entity):
    __tablename__ = 's_user'
    id = Column(Integer, primary_key=True)
    email = Column(String(50))
    password = Column(String(50))
    first_name = Column(String(255))
    last_name = Column(String(255))
    photo = Column(String(255))
    photo_s = Column(String(255))

    communities = relationship("Community", secondary='s_user_community', backref=backref('user'), uselist=True)
    roles = relationship(UserRole, backref=backref('user'), uselist=True)

    @property
    def name(self):
        return ((self.first_name or '') + ' ' + (self.last_name or '')).strip()

    def public_data(self):
        return {
            'id': self.id,
            'name': self.name,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'photo': self.photo,
            'photo_s': self.photo_s
        }

    @staticmethod
    def get_by_id(conn, id):
        return conn.query(User).filter(User.id == id).first()

    @staticmethod
    def get_by_email(conn, email):
        return conn.query(User).filter(User.email == email).first()