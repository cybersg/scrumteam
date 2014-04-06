#!/usr/bin/env python
#-*- coding: utf-8 -*-
__author__ = 'cybersg'

from flask_mongokit import Document

class User(Document):
    __collection__ = 'users'
    structure = {
        'login': basestring,
        'password': basestring,
        'admin': bool
    }
    required_fields = ['login', 'password']
    default_values = {
        'admin': False
    }

def documents():
    return [User]