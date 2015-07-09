#!/usr/bin/env python
# -*- coding: utf-8 -*-
import uuid
from kernel.helpers import image_resize
from kernel.validator import Validator
import os

__author__ = 'mr.S'

from kernel.server import app, files_dir
from bottle import jinja2_view as view, request


@app.route("/admin")
@view('admin/index')
def admin():
    return {}

@app.post('/upload/image')
def save_object():
    if not request.user.role('admin'): return False
    data = request.forms
    data['image'] = request.files.get('image')
    v = Validator(data)
    v.field("image").image()
    img = data.get("image")

    if v.is_valid() and img is not None:
        path = os.path.abspath(files_dir+"/upload/")
        image_name = 'image.'+str(uuid.uuid4())+".png"
        if not os.path.exists(path): os.makedirs(path)

        image_path = os.path.join(path, image_name)

        image = image_resize(img)
        image.save(image_path)

        return {"status": "ok",
                "url": '/file/upload/'+image_name,
                "width": image.size[0],
                "height": image.size[1]
                }
    else:
        return {"status": "fail",
                "errors": v.errors}