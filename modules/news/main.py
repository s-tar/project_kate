#!/usr/bin/env python
# -*- coding: utf-8 -*-
from entities.s_news import News
from kernel.module import Module
from bottle import jinja2_view as view, jinja2_template as template, request, redirect
from kernel.translator import translate
from kernel.validator import Validator

__author__ = 'mr.S'


module = Module(name="news", route="/news", title="Новости")


@module.route('')
@view('news/list')
def all():
    user = request.user.get()
    if user:
        load_month()
        news = request.db(News).get_visible()
        return {'news': news, 'page': 'news'}
    redirect("/")


@module.route('/<id:int>')
@view('news/news')
def news(id=None):
    user = request.user.get()
    if user:
        load_month()
        news = request.db(News).get_by_id(id)
        return {'news': news, 'page': 'news'}
    redirect("/")

def load_month():
    translate('date.month_1', default="Января")
    translate('date.month_2', default="Февраля")
    translate('date.month_3', default="Марта")
    translate('date.month_4', default="Апреля")
    translate('date.month_5', default="Мая")
    translate('date.month_6', default="Июня")
    translate('date.month_7', default="Июля")
    translate('date.month_8', default="Августа")
    translate('date.month_9', default="Сентября")
    translate('date.month_10', default="Октября")
    translate('date.month_11', default="Ноября")
    translate('date.month_12', default="Декабря")



