#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'mr.S'

from sqlalchemy import event
import kernel
from entities.s_translation import Translation
from entities.s_language import Language
from bottle import request
from sqlalchemy.orm import class_mapper
from sqlalchemy import inspect
from kernel.db import Database
from sqlalchemy.orm.attributes import get_history
from sqlalchemy.orm.session import Session
import kernel


dictionary = {}
default_language = None

def update_translation(_dictionary):
    global dictionary
    code = _dictionary.code
    dictionary[code] = _dictionary

def translate(code, default='', language=None):
    from entities.s_dictionary import Dictionary
    global dictionary
    mode = request.query.get('mode')
    if mode == 'no_translation': return code
    if code not in dictionary:
        db = Database()
        d = db(Dictionary).get_by_code(code)
        if d is None:
            d = Dictionary()
            d.code = code
            d.text = default
            db.add(d)
            db.commit()
        db.expunge(d)
        db.close()
        dictionary[code] = d
    return dictionary[code].t('text', language=language)


def get_entity_code(obj, field=None):
    key = [obj.__table__.name]
    for f in class_mapper(obj.__class__).primary_key:
        key.append(str(getattr(obj, f.name)))
    if field is not None: key.append(field)
    return '.'.join(key)


def get_translations(obj, db=None, language=None):
    database = db or Database()
    ids = []
    for c in obj.__table__.columns:
        if c.name in obj.translatable_fields:
            ids.append(get_entity_code(obj, c.name))
    query = database().query(Translation).filter(Translation.trl_code.in_(ids))
    if language is not None:
        query = query.filter(Translation.lng_code == language)
    translations = query.all()
    if not db:
        database.close()
    return translations


def after_insert_listener(mapper, connection, target):
    lang = request.forms.get('translation_language')
    if not lang: lang = get_translation_language().lng_code
    db = request.db()
    for c in target.__table__.columns:
        if c.name in target.translatable_fields:
            translation = Translation()
            translation.trl_code = get_entity_code(target, c.name)
            translation.lng_code = lang
            translation.trl_text = getattr(target, c.name)
            db.add(translation)
    db.commit()


def after_delete_listener(mapper, connection, target):
    db = Database()
    for t in get_translations(target, db): db.delete(t)
    db.commit()
    db.close()


def update_listener(mapper, connection, target):
    modified = Session.object_session(target).is_modified(target, include_collections=False)
    if modified:
        translations = {}
        insp = inspect(target)
        db = kernel.db.Database()
        for t in get_translations(target, db):
            if not t.lng_code in translations: translations[t.lng_code] = {}
            translations[t.lng_code][t.trl_code] = t
        default_lang = get_default_language().lng_code
        trans_lang = request.forms.get('translation_language')
        if not trans_lang: trans_lang = get_translation_language().lng_code
        if not trans_lang in translations: translations[trans_lang] = {}

        for f in target.translatable_fields:
            if getattr(target, f) is not None and getattr(target, f) != 'None' and modified:
                attr_state = insp.attrs[f]
                code = get_entity_code(target, f)
                if code in translations[trans_lang]:
                    translation = translations[trans_lang][code]
                else:
                    translation = Translation()
                    translation.trl_code = code
                    translation.lng_code = trans_lang
                translation.trl_text = str(getattr(target, f))
                db.add(translation)

                if not hasattr(target, '__translation__'): setattr(target, '__translation__', {})
                if not trans_lang in target.__translation__: target.__translation__[trans_lang] = {}
                target.__translation__[trans_lang][f] = getattr(target, f)
                if trans_lang != default_lang and len(attr_state.history.deleted) > 0:
                    setattr(target, f, attr_state.history.deleted[0])
        db.commit()
        db.close()


def on_load(target, context):
    translations = {}
    for t in get_translations(target):
        lang = t.lng_code
        attr = t.trl_code.split('.')[-1]
        text = t.trl_text
        if not lang in translations: translations[lang] = {}
        translations[lang][attr] = text

    setattr(target, '__translation__', translations)


def entity_translate(self, attr, editable=False, default=None, language=None):
    lang = language or get_translation_language().lng_code if editable else get_language().lng_code
    val = None
    if hasattr(self, '__translation__') and lang in self.__translation__ and attr in self.__translation__[lang]:
        val = self.__translation__[lang][attr]
    if val is None: val = default
    if val is None: val = getattr(self, attr)
    return val


def translatable(_class, fields):
    _class.translatable_fields = fields
    event.listen(_class, 'after_insert', update_listener)
    event.listen(_class, 'before_update', update_listener)
    event.listen(_class, 'after_delete', after_delete_listener)
    event.listen(_class, 'load', on_load)
    setattr(_class, 't', entity_translate)
    setattr(_class, 'translate', entity_translate)


def get_default_language():
    global default_language
    db = Database()
    if not default_language:
        lang = db(Language).get_default()
        default_language = lang
    db.close()
    return default_language


def set_language(lang_code):
    s = request.session
    env = kernel.server.get_environment()
    if not 'language' in s: s['language'] = {}
    lang = request.db(Language).get_by_code(lang_code)
    s['language'][env] = lang


def get_language():
    s = request.session
    env = kernel.server.get_environment()

    if not 'language' in s: s['language'] = {}
    if env not in s['language']:
        s['language'][env] = get_default_language()

    return s['language'][env]


def set_translation_language(lang_code):
    s = request.session
    if not 'language' in s: s['language'] = {}
    lang = request.db(Language).get_by_code(lang_code)
    s['language']['translation'] = lang


def get_translation_language():
    s = request.session
    lang = None
    lang_code = request.forms['__translation__'] if '__translation__' in request.forms else ''
    if lang_code != '':
        lang = request.db(Language).get_by_code(lang_code)
    if not lang and 'language' in s and 'translation' in s['language']:
        lang = s['language']['translation']
    if not lang:
        lang = get_default_language()
    return lang


def set_environment(env):
    s = request.session
    if not 'language' in s: s['language'] = {}
    s['language']['environment'] = 'environment_'+env
    return ''


def get_environment():
    s = request.session
    if not 'language' in s: s['language'] = {}
    return s['language']['environment'] if 'environment' in s['language'] else 'site'