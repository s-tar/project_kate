#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'mr.S'
from entities.s_user import User as UserEntity


class User(object):
    def __init__(self, session, db):
        self._session = session
        self._user = None
        self._db = db

    def get(self):
        if not self._session:
            return None
        user_id = self._session.get('user', {}).get('id', None)

        if not self._user and user_id:
            self._user = self._db(UserEntity).get_by_id(user_id)
        return self._user

    def set(self, user):
        s = self._session
        if user:
            s.setdefault('user', {})['id'] = user.id
            s.save()
            s.persist()
            self._user = user
        else:
            if 'user' in s:
                del s['user']
            s.save()
            s.persist()
            self._user = None
        return self._user

    def role(self, name):
        name = name.strip().lower()
        user = self.get()
        return False if not user else bool([role.code.lower() for role in user.roles if role.code.lower() in(name, 'superadmin')])
