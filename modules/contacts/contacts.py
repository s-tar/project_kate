#!/usr/bin/env python
# -*- coding: utf-8 -*-
from kernel.widget import widget
from kernel.translator import translate, get_default_language

__author__ = 'mr.S'


from kernel.server import app
from bottle import jinja2_template as template, request
from kernel.validator import Validator
import smtplib
from email.mime.text import MIMEText
from entities.s_contacts import Contacts

@app.route('/contacts')
def contacts():
    contacts = request.db(Contacts).list_all_by_type()
    return template('page', {
        'content': template('contacts/contacts', {'contacts': contacts}),
        'menu_item': 'contacts'
    })

@app.post('/contacts/send')
def send():
    data = request.forms
    v = Validator(data)
    v.field("name").required()
    v.field("email_phone").required()
    v.field("reason").integer()

    receivers = [c.cnt_value for c in request.db(Contacts).list_by_type('feedback')]
    if v.is_valid():
        data = v.valid_data
        reason = translate('site.contacts.reason'+str(data.get("reason")), language=get_default_language().lng_code)
        text = """\
        Контактное лицо: %s <br/>
        Email или телефон: %s <br/>
        Причина: %s <br/>
        <br/>
        %s
        """ % (data.get('name'),
               data.get('email_phone'),
               reason,
               data.get('text'))
        msg = MIMEText(text.encode('utf-8'), 'html')
        sender = data.get('email')
        receiver = ', '.join(receivers)
        msg['Subject'] = 'Письмо от пользователя %s' % data.get('name')
        msg['From'] = 'Обратная связь'
        msg['To'] = receiver
        s = smtplib.SMTP('localhost')
        s.sendmail(sender, receiver, msg.as_string())
        s.quit()
        return {"status": "ok",
                "message": translate('site.feedback.message_sent', default="Повiдомлення вiдправленно.")}
    else:
        return {"status": "fail",
                "errors": translate('site.feedback.fill_all_fields', default="Заповнiть, будь ласка, усi поля.")}


@widget('contacts.social_networks')
def sn_widget():
    contacts = request.db(Contacts).list_all_by_type()
    return template('contacts/sn',{'contacts': contacts})