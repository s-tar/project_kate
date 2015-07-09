#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'mr.S'

from kernel.db import Base
from entities.entity import Entity
from sqlalchemy import Column, Integer, String, Text, desc
from bottle import request
from kernel.translator import translatable

class Contacts(Base, Entity):
    __tablename__ = 's_contacts'
    cnt_id = Column(Integer, primary_key=True)
    cnt_type = Column(String(255))
    cnt_value = Column(Text())

    @staticmethod
    def list_all(conn):
        return conn.query(Contacts).all()

    @staticmethod
    def get_by_id(conn, id):
        return conn.query(Contacts).filter(Contacts.cnt_id == id).first()

    @staticmethod
    def list_by_type(conn, type):
        return conn.query(Contacts).filter(Contacts.cnt_type == type).all()

    @staticmethod
    def list_all_by_type(conn):
        _contacts = Contacts.list_all(conn)
        contacts = {}
        for contact in _contacts:
            if contact.cnt_type not in contacts.keys(): contacts[contact.cnt_type] = []
            contacts[contact.cnt_type].append(contact)
        return contacts

translatable(Contacts, ['cnt_value'])