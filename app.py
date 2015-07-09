#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'mr.S'
import os, sys, site
#sys.stdout = sys.stderr

path = os.path.dirname(os.path.realpath(__file__))
#site.addsitedir(path + '/venv/lib/python2.6/site-packages')
#sys.path.insert(0, path + '/venv/lib/python2.6/site-packages')

# Activate your virtual env
#activate_env=os.path.expanduser(path+"/venv/bin/activate_this.py")
#execfile(activate_env, dict(__file__=activate_env))

if 'APPDIR' not in os.environ:
    os.environ['APPDIR'] = path

sys.path.append(path)
os.chdir(path)


import platform, bottle,  sqlalchemy, beaker, jinja2
from bottle import Bottle, default_app


import kernel.server
kernel.server.run(__name__ == '__main__')
application = app = kernel.server.app