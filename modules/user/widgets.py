#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'mr.S'
from kernel.widget import *
from bottle import jinja2_template as template, request
from modules.user.user import online



@widget('user.header')
def widget_header():
    user = request.user.get()
    return template('user/widgets/header', {'user': user})

@widget('user.admin.login.form')
def widget_login_form():
    user = request.user.get()
    return template('user/widgets/admin_login_form') if not user else None

@widget('user.login.form')
def widget_login_form():
    user = request.user.get()
    return template('user/widgets/login_form') if not user else None


@widget('user.registration.form')
def widget_registration_form():
    user = request.user.get()
    return template('user/widgets/registration_form') if not user else None

@widget('user.icon')
def widget_icon(user):
    return template('user/widgets/icon', {'user': user,
                                          'online': online})
