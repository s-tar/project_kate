#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'mr.S'


from kernel.module import Module
from entities.s_contacts import Contacts
from bottle import jinja2_view as view, request

module = Module(name="contacts", route="/admin/contacts", title="Контакты", is_admin=True)
@module.route('')
@view('admin/contacts/main')
def main():
    contacts = request.db(Contacts).list_all_by_type()
    return {'contacts': contacts}


@module.post('/save')
def save():
    if not request.user.role('admin'):
        return False
    data = request.forms

    addresses_ids = data.getall('address_id')
    addresses = data.getall('address')

    emails_ids = data.getall('email_id')
    emails = data.getall('email')

    phones_ids = data.getall('phone_id')
    phones_nums = data.getall('phone_num')
    phones_description = data.getall('phone_description')

    feedback_ids = data.getall('feedback_id')
    feedback_email = data.getall('feedback_email')

    map_ids = data.getall('map_id')
    map = data.getall('map')

    sn_names = data.getall('sn.name')
    sn_ids = data.getall('sn.id')
    sn_links = data.getall('sn.link')

    save_contacts(addresses_ids, addresses, 'address')
    save_contacts(emails_ids, emails, 'email')

    phones = []
    for a, b in zip(phones_nums, phones_description):
        phones.append(a + '|' + b if a != '<delete>' else '<delete>')

    save_contacts(phones_ids, phones, 'phone')

    save_contacts(feedback_ids, feedback_email, 'feedback')
    save_contacts(map_ids, map, 'map')
    for i, name in enumerate(sn_names):
        save_contacts([sn_ids[i]], [sn_links[i]], name)

    request.db.commit()
    return


def save_contacts(ids, values, type):
    if not request.user.role('admin'):
        return False
    for i, id in enumerate(ids):
        if id != '':
            contact = request.db(Contacts).get_by_id(id)
        else:
            contact = Contacts()
            contact.cnt_type = type
        contact.cnt_value = values[i]

        if contact.cnt_value == '<delete>':
            if contact.cnt_id is not None: request.db.delete(contact)
        else:
            request.db.add(contact)