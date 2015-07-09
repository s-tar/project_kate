#!/usr/bin/env python
# -*- coding: utf-8 -*-
import hashlib
from bottle import FileUpload
from entities.s_file import File
from kernel.config import config
from kernel.db import Database
import os
import uuid
import shutil

__author__ = 'mr.S'

root = os.path.dirname(os.path.abspath(os.path.join(__file__, '../')))
files_path = os.path.normpath(os.path.join(root, config['files']['path']))

def save_to_db(name, module=None, entity=None, database=None):
    db = database
    if not db: db = Database()
    name = name.strip("/")
    name_parts = name.split('.')

    new_file = File()
    new_file.name = name_parts[0]
    new_file.module = module
    new_file.entity = entity
    new_file.extension = name_parts[-1] if len(name_parts) > 1 else None
    new_file.type = '.'.join(name_parts[1:-1]) if len(name_parts) > 2 else None

    prev_file = db(File).get_by_fullpath(new_file.fullpath)

    if prev_file:
        new_file = prev_file

    old_path = os.path.join(root, new_file.fullpath)
    m = hashlib.md5()
    m.update(str(uuid.uuid4()))
    new_file.uniq_id = m.hexdigest()
    new_path = os.path.join(root, new_file.fullpath)

    if old_path != new_path and os.path.exists(old_path): os.remove(old_path)

    db.add(new_file)
    print new_file.id
    if not database:
        db.commit()
        db.close()

    return new_path

def save(file_or_path, name=None, module=None, entity=None, save_method=None, database=None):
    file_path = file_or_path
    if isinstance(file_or_path, file):
        file_path = file_or_path.name

    new_path = save_to_db(name, module, entity, database)

    if not os.path.exists(os.path.dirname(new_path)):
        os.makedirs(os.path.dirname(new_path))


    if save_method:
        save_method(new_path)
    elif isinstance(file_or_path, file):
        file_or_path.seek(0)
        with open(new_path, "wb") as f:
            shutil.copyfileobj(file_or_path, f)
    else:
        shutil.copyfile(file_path, new_path)

    return new_path
