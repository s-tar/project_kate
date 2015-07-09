#!/usr/bin/env python
# -*- coding: utf-8 -*-
import kernel

__author__ = 'mr.S'

from kernel.module import Module
from bottle import jinja2_template as template, request
from entities.s_language import Language
from kernel.widget import widget
from kernel.validator import Validator
from kernel.translator import get_default_language, get_translation_language, set_translation_language
module = Module(name="languages", title="Языки", route="/admin/language", is_admin=True)


@module.route('')
def main():
    languages = request.db(Language).list_all()
    return template('admin/language/list', {'languages': languages})


@module.post('/save')
def save():
    if not request.user.role('admin'): return False
    data = request.forms
    v = Validator(data)
    data['lng_code'] = data['lng_code'].upper()
    v.field("lng_id").integer(nullable=True)
    v.field("lng_code").required()
    v.field("lng_name").required()
    lang = request.db(Language).get_by_code(data.get("lng_code"))
    if lang is not None and lang.lng_id != data['lng_id']:
        v.add_error('lng_name', 'Язык с таким кодом уже существует', 'language.exists')
    if v.is_valid():
        data = v.valid_data
        lang = request.db(Language).get_by_id(data.get("lng_id"))
        if lang is None: lang = Language()
        lang.lng_code = data.get("lng_code")
        lang.lng_name = data.get("lng_name")
        request.db.add(lang)
        request.db.commit()
        return {"status": "ok",
                "language": lang.as_dict(translated=True)}
    else:
        return {"status": "fail",
                "errors": v.errors}


@module.post('/change_visibility')
def change_visibility():
    if not request.user.role('admin'): return False
    id = request.forms.id
    visible = request.forms.visible == 'true'
    lang = request.db(Language).get_by_id(id)
    if lang is not None:
        lang.lng_active = visible
        request.db.add(lang)
        request.db.commit()
        return {"status": "ok", "visible": lang.lng_active}
    else:
        return {"status": "fail"}


@module.post('/change_default')
def change_default():
    if not request.user.role('admin'): return False
    id = request.forms.id
    default = request.forms.is_default == 'true'
    lang = request.db(Language).get_by_id(id)
    all = request.db(Language).list_all()
    if lang is not None:
        for lng in all:
            lng.lng_default = False
            request.db.add(lng)

        lang.lng_default = default
        request.db.add(lang)
        request.db.commit()
        kernel.translator.default_language = lang
        return {"status": "ok", "is_default": lang.lng_default}
    else:
        return {"status": "fail"}


@module.post('/delete')
def delete():
    if not request.user.role('admin'): return False
    id = request.forms.id
    lang = request.db(Language).get_by_id(id)

    if lang is not None:
        def_language = get_default_language()
        trans_language = get_translation_language()
        if trans_language.lng_id == lang.lng_id:
            set_translation_language(def_language.lng_code)
        request.db.delete(lang)
        request.db.commit()
        return {"status": "ok"}
    else:
        return {"status": "fail"}


@widget("language.form")
def form(id=None):
    language = request.db(Language).get_by_id(id) if id is not None else Language()
    return template('admin/language/form', {"language": language})