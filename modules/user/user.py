#!/usr/bin/env python
# -*- coding: utf-8 -*-
from kernel.module import Module
from sqlalchemy import func

__author__ = 'mr.S'

from kernel.server import app
from kernel.validator import Validator
from entities.s_user import User
from entities.s_community import Community
from entities.s_user_community import UserCommunity
from bottle import jinja2_template as template, request, HTTPError
import urllib2
import json
import hashlib
from kernel.config import config
from kernel.server import files_dir
from kernel.helpers import remove_similar, image_resize, image_thumbnail
import os
import uuid
from passlib.hash import sha256_crypt

user_path = os.path.abspath(files_dir+"/users/user_{id}")
profile_path = os.path.join(user_path, "profile")
online = {}

module = Module(name="user", route="/user")


@module.post('/login/fb')
def login_fb():
    user = None
    data = json.loads(request.forms.data)
    try:
        response = urllib2.urlopen("https://graph.facebook.com/me?fields=first_name,last_name,picture,email&access_token="+data['authResponse']['accessToken'])
        response = json.loads(response.read())
        if response is not None and 'id' in response:
            fb_id = response['id']
            uc = request.db().query(UserCommunity).join(Community)\
                .filter(Community.alias == 'fb', UserCommunity.external_id == fb_id).first()

            user = uc.user if uc is not None else None
            if user is None:
                email = response['email']

                user = request.db.query(User).filter_by(email=email).first()
                if user is None:
                    user = User(first_name=response['first_name'],
                                last_name=response['last_name'],
                                email=response['email'],
                                photo='https://graph.facebook.com/'+fb_id+'/picture?type=large',
                                photo_s='https://graph.facebook.com/'+fb_id+'/picture?type=square')

                community = request.db.query(Community).filter_by(alias='fb').first()
                if community is None:
                    community = Community(alias='fb', name='Facebook')

                uc = UserCommunity(user=user, community=community, external_id=fb_id)
                request.db.add(uc)
                request.db.commit()
    except HTTPError:
        pass
    return auth(user)


@module.post('/login/vk')
def login_vk():
    user = None
    data = json.loads(request.forms.data)
    params = "expire="+str(data['expire']) \
             + "mid="+str(data['mid'])\
             + "secret="+str(data['secret'])\
             + "sid="+str(data['sid'])\
             + str(config['sn']['vk']['app_secret'])
    md5 = hashlib.md5()
    md5.update(params)
    sig = md5.hexdigest()
    if sig == data['sig']:
        try:
            response = urllib2.urlopen("https://api.vk.com/method/getProfiles?uid="+data['mid']+"&fields=uid,photo,photo_big,photo_medium")
            response = json.loads(response.read())
            if response is not None:
                response = response['response'][0]
                vk_id = response['uid']
                uc = request.db().query(UserCommunity).join(Community)\
                    .filter(Community.alias == 'vk', UserCommunity.external_id == vk_id).first()
                user = uc.user if uc is not None else None
                if user is None:
                    user = User(first_name=response['first_name'],
                                last_name=response['last_name'],
                                photo=response['photo_big'],
                                photo_s=response['photo'])

                    community = request.db.query(Community).filter_by(alias='vk').first()
                    if community is None:
                        community = Community(alias='vk', name='VKontakte')

                    uc = UserCommunity(user=user, community=community, external_id=vk_id)
                    request.db.add(uc)
                    request.db.commit()
        except KeyError, HTTPError:
            pass

    return auth(user)

@module.post('/login/admin')
def login_native():
    data = request.forms
    v = Validator(data)
    v.field("email").required()
    v.field("password").required()
    if v.is_valid():
        data = v.valid_data
        user = request.db().query(User).filter(User.email == data.get('email')).first()
        if not user or sha256_crypt.verify(data.get('password'), user.password):
            v.add_error('email', 'Неправильный логин или пароль', 'wrong_login')
        else:
            auth(user)
            return {"status": "ok", "reload": True}
    return {"status": "fail",
            "errors": v.errors}

@module.post('/login/native')
def login_native():
    data = request.forms
    v = Validator(data)
    v.field("email").required()
    v.field("password").required()
    if v.is_valid():
        data = v.valid_data
        user = request.db().query(User).filter(User.email == data.get('email')).first()
        if not user or not verify_password(data.get('password'), user.password):
            v.add_error('email', 'Неправильный email или пароль', 'wrong_login')
        else:
            auth(user)
            return {"status": "ok", "reload": True}
    return {"status": "fail",
            "errors": v.errors}

@module.post('/registrate')
def registrate():
    data = request.forms
    data['photo'] = request.files.get('photo')
    v = Validator(data)
    v.field("first_name").required()
    v.field("last_name").required()
    v.field("email").required().email()
    v.field("password").required().length(min=5, message="Длина пароля не менее %(min)d символов")
    v.field("photo").image()
    if data.get("password") != data.get("repassword"):
        v.add_error('password', 'Пароли не совпадают', 'wrong_repassword')
    if(v.is_valid()):
        data = v.valid_data
        password_hash = hash_password(data.get('password'))
        user = request.db(User).get_by_email(data['email'])
        if user:
            v.add_error('email', 'Электронный адрес уже используется.', 'email_is_used_already')
        else:
            user = User()
            user.email = data['email']
            user.first_name = data['first_name']
            user.last_name = data['last_name']
            user.password = password_hash
            request.db.add(user)
            request.db.commit()
            img = data.get("photo")
            if img is not None:
                path = profile_path.format(id=user.id)
                photo_name = 'photo_'+str(user.id)+"_"+str(uuid.uuid4())+".png"
                thumbnail_name = photo_name.rstrip(".png")+".thumbnail.png"
                if not os.path.exists(path): os.makedirs(path)
                remove_similar(path, photo_name)

                image_path = os.path.join(path, photo_name)
                thumbnail_path = os.path.join(path, thumbnail_name)

                photo = image_thumbnail(img, width=200, height=200, fill='cover')
                photo.save(image_path)

                img.file.seek(0)
                thumbnail = image_thumbnail(img, width=50, height=50, fill='cover')
                thumbnail.save(thumbnail_path)

                user.photo = "/file"+image_path.replace(files_dir, '').replace("\\", '/')
                user.photo_s = "/file"+thumbnail_path.replace(files_dir, '').replace("\\", '/')
                request.db.commit()
            auth(user)
            return {"status": "ok", "reload": True}
    return {"status": "fail",
            "errors": v.errors}


@module.post('/change_photo')
def chnage_photo():
    user = request.user.get()
    data = request.forms
    data['photo'] = request.files.get('photo')
    v = Validator(data)
    if user:
        img = data.get("photo")
        if img is not None:
            path = profile_path.format(id=user.id)
            photo_name = 'photo_'+str(user.id)+"_"+str(uuid.uuid4())+".png"
            thumbnail_name = photo_name.rstrip(".png")+".thumbnail.png"
            if not os.path.exists(path): os.makedirs(path)
            remove_similar(path, photo_name)

            image_path = os.path.join(path, photo_name)
            thumbnail_path = os.path.join(path, thumbnail_name)

            photo = image_thumbnail(img, width=200, height=200, fill='cover')
            photo.save(image_path)

            img.file.seek(0)
            thumbnail = image_thumbnail(img, width=50, height=50, fill='cover')
            thumbnail.save(thumbnail_path)

            user.photo = "/file"+image_path.replace(files_dir, '').replace("\\", '/')
            user.photo_s = "/file"+thumbnail_path.replace(files_dir, '').replace("\\", '/')
            request.db.add(user)
            request.db.commit()
            return {"status": "ok", "photo": user.photo}
    return {"status": "fail",
            "errors": v.errors}

@module.post('/logout')
def user_logout():
    user = request.user.get()
    s = request.session
    if user is not None:
        s.pop('user', None)
        s.persist()
        s.save()
    return {'status': 'ok'}


def auth(user):
    user = request.user.set(user)
    if user:
        return {'status': 'ok'}
    else:
        return {'status': 'fail'}


def hash_password(password):
    return sha256_crypt.encrypt(password)


def verify_password(password, hash):
    return sha256_crypt.verify(password, hash)

@app.route('/profile/id<uid:int>')
def user_profile(uid):
    user = request.db(User).get_by_id(uid)

    return template('user/profile', {'user': user})