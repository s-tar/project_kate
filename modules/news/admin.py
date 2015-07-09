#!/usr/bin/env python
# -*- coding: utf-8 -*-
from entities.s_news import News
from kernel.module import Module
from bottle import jinja2_view as view, jinja2_template as template, request
from kernel.validator import Validator

__author__ = 'mr.S'


module = Module(name="news_admin", route="/admin/news", title="Новости", is_admin=True)


@module.route('')
@view('admin/news/list')
def all():
    news = request.db(News).get_all()
    return {'news': news}


@module.route("/new")
@module.route("/<id:int>")
def edit_route(id=None):
    news = request.db(News).get_by_id(id) or News()
    return template("admin/news/form", {'news': news})


@module.post('/save')
def save():
    if not request.user.role('admin'): return False
    data = request.forms
    v = Validator(data)
    v.field("id").integer(nullable=True)
    v.field("title").required()
    v.field("text").required()
    v.field("datetime").datetime(format='%d.%m.%Y %H:%M')

    if v.is_valid():
        data = v.valid_data
        news = request.db(News).get_by_id(data.get("id")) or News()

        news.title = data.get("title")
        news.text = data.get("text")
        news.datetime = data.get("datetime")

        request.db.add(news)
        request.db.commit()

        return {"status": "ok",
                "redirect": '/admin/news'}
    else:
        return {"status": "fail",
                "errors": v.errors}


@module.post('/change_visibility')
def change_visibility():
    if not request.user.role('admin'): return False
    id = request.forms.id
    visible = request.forms.visible == 'true'
    entity = request.db(News).get_by_id(id)
    if entity is not None:
        entity.visible = visible
        request.db.add(entity)
        request.db.commit()
        return {"status": "ok", "visible": entity.visible}
    else:
        return {"status": "fail"}


@module.post('/delete')
def delete():
    if not request.user.role('admin'): return False
    id = request.forms.id
    entity = request.db(News).get_by_id(id)
    if entity is not None:
        request.db.delete(entity)
        request.db.commit()

        return {"status": "ok"}
    else:
        return {"status": "fail"}