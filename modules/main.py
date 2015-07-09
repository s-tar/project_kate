#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'mr.S'

from entities.s_content import Content
from entities.s_news import News
from entities.s_user import User
from sqlalchemy import func
from kernel.server import app
from kernel.widget import *
from bottle import jinja2_template as template, jinja2_view as view, request, redirect
from kernel.config import config


@app.route("/")
@app.route("/index")
def index(id=None):
    user = request.user.get()
    return template('index', {})

@app.route("/registration")
def registration():
    user = request.user.get()
    if not user:
        return template('registration')
    redirect("/")

@app.route("/password/recovery")
def password_recovery():
    user = request.user.get()
    if not user:
        return template('recovery')
    redirect("/")

@app.route("/rules")
def rules():
    user = request.user.get()
    if user:
        rules = request.db(Content).get_by_alias('rules')
        return template('rules', {'page': 'rules', 'rules': rules})
    redirect("/")

@app.route("/rating")
def rating():
    user = request.user.get()
    if user:
        users = request.db().query(User).all()
        users.sort(key=lambda u: u.get_total_rating(), reverse=True)
        cities = request.db(Region).get_all()
        return template('rating', {'page': 'rating',
                                   'user': user,
                                   'members': users,
                                   'cities': cities})
    redirect("/")

@app.route("/config/sn")
def config_sn():
    return {
        'vk': {
            'app_id': config['sn']['vk']['app_id']
        },
        'fb': {
            'app_id': config['sn']['fb']['app_id']
        }
    }


@widget('main.popup')
def widget_main_popup():
    return template('widgets/popup')