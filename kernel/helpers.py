#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'mr.S'
from bottle import request, FileUpload
from PIL import Image
import os


def is_ajax():
    return True if request.headers.get('X-Requested-With') == 'XMLHttpRequest' else False

def image_thumbnail(image, width, height, position=('center', 'center'), fill='contain'):
    try:
        if type(image) is FileUpload:
            image.file.seek(0)
            image = image.file
        image = Image.open(image)
        owidth = image.size[0]
        oheight = image.size[1]

        wr, hr = 1.0*width/owidth, 1.0*height/oheight
        size = owidth, oheight
        x, y = position
        # back = Image.new('RGBA', (width, height), (125, 125, 125, 0))
        if fill == 'cover':
            if wr < hr:
                size = owidth*height/oheight, height
            else:
                size = width, oheight*width/owidth
        else:
            if wr > hr:
                size = owidth*height/oheight, height
            else:
                size = width, oheight*width/owidth

        if x == 'center':
            x = (size[0] - width) / 2
        elif x == 'right':
            x = size[0] - width
        else:
            x = 0

        if y == 'center':
            y = (size[1] - height) / 2
        elif y == 'bottom':
            y = size[1] - height
        else:
            y = 0
        image = image.resize(size, Image.ANTIALIAS)
        image = image.crop((x, y, x+width, y+height))
        return image

    except IOError, e:
        print e.errno
        print e
        print "Can not resize image "


def image_resize(image, width=None, height=None, max_width=None, max_height=None):
    try:
        if type(image) is FileUpload:
            image.file.seek(0)
            image = image.file
        image = Image.open(image)
        owidth = image.size[0]
        oheight = image.size[1]

        size = owidth, oheight
        if not width and owidth > max_width: width = max_width
        if not height and oheight > max_height: height = max_height
        if width is not None and height is not None:
            size = width, height
        elif width is not None:
            p = width/float(owidth)
            size = width, int(oheight*p)
        elif height is not None:
            p = height/float(oheight)
            size = int(owidth*p), height
        image = image.resize(size, Image.ANTIALIAS)
        print size
        if image.mode == 'RGBA':
            bg = Image.new(mode='RGBA', size=image.size, color=(255, 255, 255, 0))
            bg.paste(image, image)
            image = bg
        return image
    except IOError, e:
        print e.errno
        print e
        print "Can not resize image "

def remove_similar(path, name):
    if name is not None:
        name = name.split('.')[0]+'.'
        if os.path.exists(path):
            for f in os.listdir(path):
                if not os.path.isdir(f) and f.startswith(name):
                    os.remove(os.path.join(path, f))