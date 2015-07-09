#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'mr.S'
from kernel.module import Module
from bottle import jinja2_view as view, jinja2_template as template, request
from entities.s_seo_url import SEOUrl
from entities.s_seo_tag import SEOTag
from kernel.validator import Validator
from kernel.widget import widget
import re


module = Module(name="seo", title="SEO", route="/admin/seo", is_admin=True)
@module.route("")
@view("admin/seo/main")
def index():
    urls = request.db(SEOUrl).list_all()
    return {"urls": urls}


@module.route("/<id:int>")
@module.route("/new")
@view("admin/seo/form")
def seo_form(id=None):
    seo = request.db(SEOUrl).get_by_id(id)
    return {"seo": seo}


@module.post('/save')
def seo_save():
    if not request.user.role('admin'): return False
    data = request.forms
    v = Validator(data)
    v.field("seou_url").required()
    v.field("seou_id").integer(nullable=True)
    v.fields("seot_id").integer(nullable=True)
    seo = request.db(SEOUrl).get_by_url(v.valid_data.get("seou_url").strip())
    if seo is not None and seo.seou_id != v.valid_data.seou_id:
        v.add_error("seou_url", "Такая ссылка уже существует")

    if v.is_valid():
        seo = request.db(SEOUrl).get_by_id(data.seou_id)
        if seo is None:
            seo = SEOUrl()
        seo.seou_url = data.get('seou_url').strip()
        tag_ids = data.getall('seot_id')
        tag_text = data.getall('seot_text')
        request.db.add(seo)
        request.db.commit()
        for i, text in enumerate(tag_text):
            text = text.strip()
            id = tag_ids[i]
            tag = request.db(SEOUrl).get_by_id(id)
            if tag is None:
                tag = SEOTag()
                tag.seou_id = seo.seou_id
            if text == '':
                if id is not None:
                    request.db.delete(tag)
            else:
                tag.seot_text = text
                request.db.add(tag)
        request.db.commit()
        return {"status": "ok"}
    else:
        return {"status": "fail",
                "errors": v.errors}


@module.post('/delete/<id:int>')
def delete_seo(id=None):
    if not request.user.role('admin'): return False
    seo = request.db(SEOUrl).get_by_id(id)
    if seo is not None:
        request.db.delete(seo)
        request.db.commit()
        return {"status": "ok"}
    else:
        return {"status": "fail"}


@widget('seo')
def seo_widget():
    seos = request.db(SEOUrl).list_all_ordered()
    result = ''
    found = False
    for seo in seos:
        req = request.urlparts
        url = request.url
        re_url = seo.seou_url.replace('.', '\\.').replace('*', '.*')
        if re_url[0] == '/':
            re_url = req.scheme + '://' + req.netloc + seo.seou_url.replace('.', '\\.').replace('*', '.*')

        if re.match('^'+re_url+'$', url):
            found = True
            for tag in seo.tags:
                result = result + tag.seot_text + '\n'
        if found: break
    return result
