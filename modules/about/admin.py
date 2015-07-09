#!/usr/bin/env python
# -*- coding: utf-8 -*-
from entities.s_content import Content
from entities.s_file import File
from kernel.helpers import image_resize
from kernel.validator import Validator

__author__ = 'mr.S'

from kernel.module import Module
from bottle import jinja2_view as view, request


module = Module(name="about", route="/admin/about", title="О себе", is_admin=True)


@module.route('')
@view('admin/about/form')
def main():
    about = request.db(Content).get_by_alias('about') or Content()
    photos = request.db(File).get(name="photo", module=module.name, entity=about)
    return {'about': about, 'photos': photos}


@module.post('/save')
def save_object():
    if not request.user.role('admin'): return False
    data = request.forms
    photos = request.files.getall('file')

    v = Validator(data)

    v.fields("file.id").integer(nullable=True)
    v.fields("file.visible").boolean()
    v.fields("file.order").integer()

    if v.is_valid():
        data = v.valid_data
        about = request.db(Content).get_by_alias('about')
        if not about:
            about = Content()
            about.con_alias = 'about'
            about.con_name = 'about'

        about.con_text = data.get("text")

        request.db.add(about)
        request.db.commit()

        action = data.getall('file.action')
        visible = data.getall('file.visible')
        order = data.getall('file.order')

        for i, id in enumerate(data.getall('file.id')):
            if action[i]:
                if action[i] == 'new':
                    file = request.db(File).create('photo.jpg', module=module.name, entity=about)
                    file.create_dir()
                    file.update_uniq_id()
                    photo = photos.pop(0)
                    image_resize(photo).convert('RGB').save(file.get_fullpath())
                else:
                    file = request.db(File).get_by_id(id)
                file.visible = visible[i]
                file.order = order[i]
                if action[i] == 'delete':
                    file.remove_files()
                    request.db.delete(file)
                else:
                    request.db.add(file)

        request.db.commit()
        return {"status": "ok",
                "reload": 'true'}
    else:
        return {"status": "fail",
                "errors": v.errors}