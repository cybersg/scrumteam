#!/usr/bin/env python
#-*- coding: utf-8 -*-
__author__ = 'cybersg'

from flask import Flask, g
from flask_mongokit import MongoKit

app = Flask(__name__, template_folder='static')
app.config.from_object('scrumteam.conf.Config')

import models
db = MongoKit(app)
app.config['DB'] = db
db.register(models.documents())

def get_db():
    global db
    cn = getattr(g, 'db', None)
    if cn is None:
        cn = db
    return cn


import views



