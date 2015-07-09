#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'mr.S'

from kernel.widget import widget
from bottle import jinja2_template as template, request
from entities.s_language import Language
from kernel.translator import get_translation_language, set_translation_language, set_language, get_language
from kernel.module import Module
from kernel.server import app

module = Module(name="translator", route="/admin/translator/")

@widget('translator.right_tabs')
def right_tabs(for_element=""):
    languages = request.db(Language).list_active()
    current = get_translation_language()
    return template('admin/translator/right_tabs', {'languages': languages, 'current': current.lng_code, 'for_element': for_element})

@widget('translator.language_selector')
def language_selector():
    languages = request.db(Language).list_active()
    current = get_language()
    return template('admin/translator/language_selector', {'languages': languages, 'current': current})

@module.post('change_translation_language')
def change_translation():
    code = request.forms['code']
    set_translation_language(code)
    return {'status': 'ok'}

@module.post('change_language')
def change_translation():
    code = request.forms['code']
    set_language(code)
    return {'status': 'ok'}

@app.post('/translator/change_language')
def change_translation():
    code = request.forms['code']
    set_language(code)
    return {'status': 'ok'}