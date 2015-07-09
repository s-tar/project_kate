#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'mr.S'


from kernel.module import Module
from entities.s_dictionary import Dictionary
from bottle import jinja2_template as template
from kernel.widget import widget
from kernel.validator import Validator
from bottle import request
from kernel.translator import update_translation

module = Module(name="directory", title="Словарь", route="/admin/dictionary", is_admin=True)

@module.route('')
def main():
    dictionary = request.db(Dictionary).list_all()
    return template('admin/dictionary/list',{'dictionary': dictionary})

@module.post('/save')
def save():
    if not request.user.role('admin'): return False
    data = request.forms
    v = Validator(data)
    v.field("id").required().integer()
    if v.is_valid():
        data = v.valid_data
        dictionary = request.db(Dictionary).get_by_id(data.get("id"))
        dictionary.text = data.get("text")
        request.db.add(dictionary)
        request.db.flush()
        request.db.commit()
        update_translation(dictionary)
        return {"status": "ok",
                "dictionary": dictionary.as_dict(translated=True)}
    else:
        return {"status": "fail",
                "errors": v.errors}

@widget("dictionary.form")
def form(id):
    dictionary = request.db(Dictionary).get_by_id(id)
    return template('admin/dictionary/form', {"dictionary": dictionary})


