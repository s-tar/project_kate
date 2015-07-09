#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'mr.S'


from kernel.module import Module
from entities.s_content import Content
from bottle import jinja2_template as template, request
from kernel.validator import Validator
from kernel.widget import widget


module = Module(route="/admin/content", name="content", title="Страницы", is_admin=True)
@module.route('')
def content_list():
    content_list = request.db(Content).list_all()
    return template('admin/content/list', {'content_list': content_list})


@module.route('/<alias>')
def content_list(alias):
    content = request.db(Content).get_by_alias(alias)
    return template('admin/content/form',{'content': content})


@module.post('/save')
def save_content():
    if not request.user.role('admin'):
        return False
    data = request.forms
    v = Validator(data)
    v.field("text").required()
    v.field("id").integer(nullable=True).required()

    if v.is_valid():
        data = v.valid_data
        content = request.db(Content).get_by_id(data.get("id"))

        content.text = data.get("text")

        request.db.add(content)
        request.db.commit()

        return {"status": "ok",
                "redirect": '/admin/content'}
    else:
        return {"status": "fail",
                "errors": v.errors}

@widget('content')
def content_widget(alias):
    content = request.db(Content).get_by_alias(alias)
    return content.text if content.text else ''