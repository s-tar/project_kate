#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'mr.S'

import uuid
from beaker.ext.sqla import make_cache_table, SqlaNamespaceManager
import re
from sqlalchemy import MetaData
import bottle
import datetime
import kernel
from kernel.widget import get as loadWidget
from kernel.helpers import is_ajax
from kernel.translator import set_environment, translate
import kernel.translator
from bottle import Bottle, static_file, Jinja2Template, request, jinja2_template as template
from beaker.middleware import SessionMiddleware
from kernel.user import User
from entities.s_user import User as UserEntity
import kernel.db
import sys
import os


app = application = Bottle()
reload(sys)
sys.setdefaultencoding('UTF8')
template_path = './templates/default/'
bottle.TEMPLATE_PATH.insert(0, template_path)


def run(run=True):
    global app
    SqlaNamespaceManager._init_dependencies()
    setattr(SqlaNamespaceManager, 'lock_dir', None)
    session_opts = {
        'session.type': 'ext:sqla',
        'session.bind': kernel.db.engine,
        'session.table': make_cache_table(MetaData()),
        'session.cookie_expires': False,
        'session.auto': True}

    class BeforeRequestMiddleware(object):
        def __init__(self, app):
            self.app = app

        def __call__(self, e, h):
            e['PATH_INFO'] = e['PATH_INFO'].rstrip('/')
            return self.app(e, h)

    Jinja2Template.defaults = {
        'widget': loadWidget,
        'is_ajax': is_ajax,
        'modules': kernel.module.modules,
        'request': request,
        't': translate,
        'translate': translate,
        'datetime': datetime,
        'translator': kernel.translator
    }
    Jinja2Template.settings = {
        'filters': {
            'floatint': lambda num: num if isinstance(num, int) else '%.1f' % num,
            'e_quotes':  lambda text: text.replace('"', '&quot;').replace("'", "&#39;") if text else text,
            'announcement': lambda text: str(text).split('<!-- page break -->')[0] if text else '',
        }
    }

    @app.route('/static/<path:path>')
    def static(path):
        return static_file(path, './templates/default/static/')

    @app.route('/file/<path:path>')
    @app.route('/files/<path:path>')
    def file(path):
        path = re.sub(r'(.*)\._(.*)_\.(.*)', r'\1.\3', path)
        return static_file(path, './files/')

    @app.post('/widget/<name:path>')
    def widget(name):
        try:
            data = request.json['data'] if request.json is not None and 'data' in request.json else {}
            return loadWidget(name, data, wrap=False)
        except ValueError:
            bottle.response.status = 404


    @app.error(404)
    def error404(error):
        return template("404")

    @app.hook('before_request')
    def before_request():
        request.session = request.environ.get('beaker.session')
        request.db = kernel.db.Database()
        request.user = User(request.session, request.db)


    @app.hook('after_request')
    def after_request():
        if hasattr(request, 'db'):
            request.db.close()

    app = BeforeRequestMiddleware(app)
    app = SessionMiddleware(app, session_opts)

    if run:
        bottle.run(app, host='192.168.1.2', port=3000)


def get_environment():
    if request.environ['PATH_INFO'].startswith('/admin/') or request.environ['PATH_INFO'] == '/admin':
        return 'admin'
    else:
        return 'site'

files_dir = os.path.abspath("./files/")
from modules import *

__all__ = ["app", "session", "files_dir"]