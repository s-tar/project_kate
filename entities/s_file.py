#!/usr/bin/env python
# -*- coding: utf-8 -*-
import hashlib
import uuid
from entities.entity import Entity
from kernel.db import Base
from sqlalchemy import Column, Integer, String, Boolean
from kernel.config import config
from sqlalchemy import event
import os
from sqlalchemy.orm import class_mapper

__author__ = 'mr.S'
root = os.path.dirname(os.path.abspath(os.path.join(__file__, '../')))
files_path = os.path.normpath(os.path.join(root, config['files']['path']))


class File(Base, Entity):
    __tablename__ = 's_file'
    id = Column(Integer, primary_key=True)
    module = Column(String(255))
    entity = Column(String(255))
    name = Column(String(255))
    extension = Column(String(255))
    uniq_id = Column(String(255))
    visible = Column(Boolean(create_constraint=False), default=True)
    order = Column(Integer, default=1)

    @staticmethod
    def get(conn, name=None, module=None, entity=None):

        if name or module or entity:
            query = conn.query(File)
            if entity: query = query.filter(File.entity == File.stringify_entity(entity))
            if module: query = query.filter(File.module == module)
            if name:
                parts = name.rsplit('.', 1)
                query = query.filter(File.name == parts[0])
                if len(parts) > 1:
                    query = query.filter(File.extension == parts[1])
            query = query.order_by(File.order, File.id.desc())
            return query.all()
        return []

    @staticmethod
    def create(conn, name, module=None, entity=None):
        name = name.strip("/")
        name_parts = name.split('.')

        new_file = File()
        new_file.name = name_parts[0]
        new_file.module = module
        new_file.entity = File.stringify_entity(entity)
        new_file.extension = name_parts[-1] if len(name_parts) > 1 else None

        new_file.update_uniq_id()
        conn.add(new_file)
        conn.commit()

        return new_file

    def get_path(self, sufix=None, with_cache=False):
        path = [config['files']['path']]
        name = []
        if self.module: path.append(self.module)
        if self.entity: path.append(self.entity)
        if self.name: name.append(self.name)
        name.append('id'+str(self.id))
        if sufix: name.append(sufix)
        if with_cache: name.append('_'+self.uniq_id+'_')
        if self.extension: name.append(self.extension)

        path = os.path.normpath(os.path.join('/'.join(path), '.'.join(name)))
        return path

    def update_uniq_id(self):
        m = hashlib.md5()
        m.update(str(uuid.uuid4()))
        self.uniq_id = m.hexdigest()

    def get_fullpath(self, sufix=None):
        path = self.get_path(sufix)
        return os.path.join(root, path)

    def get_url(self, sufix=None):
        path = self.get_path(sufix, with_cache=True)
        return '/'+path.replace('\\', '/')

    def create_dir(self):
        path = os.path.dirname(self.get_fullpath())
        if not os.path.exists(path):
            os.makedirs(path)

    def remove_files(self):
        path, name = self.get_fullpath().rsplit(os.sep, 1)
        name = self.name.split('/')[-1]+'.id'+str(self.id)
        if os.path.exists(path):
            for f in os.listdir(path):
                if not os.path.isdir(f) and f.startswith(name):
                    os.remove(os.path.join(path, f))

    @staticmethod
    def stringify_entity(entity):
        if isinstance(entity, Base):
            _key = [entity.__table__.name]
            for f in class_mapper(entity.__class__).primary_key:
                _key.append(str(getattr(entity, f.name)))
            return '.'.join(_key)
        return str(entity)
