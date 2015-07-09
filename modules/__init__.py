#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'mr.S'

import os
import glob

__all__ = []
modules = glob.glob(os.path.dirname(__file__)+"/*.py")
modules = modules + glob.glob(os.path.dirname(__file__)+"/*/__init__.py")


for f in modules:
    f = f.replace("__init__.py", "")
    f = f.replace(os.path.dirname(__file__), "")
    f = f.replace(".py", "", -1)
    f = f.strip('/').strip('\\')
    if f:
        __all__.append(os.path.basename(f))