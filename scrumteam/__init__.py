#!/usr/bin/env python
#-*- coding: utf-8 -*-
__author__ = 'cybersg'

from flask import Flask
from flask_mongokit import MongoKit

def init_db():
    db = MongoKit(app)
    app.config['DB'] = db
    db.register(models.documents())

app = Flask(__name__, static_url_path='')
app.config.from_object('scrumteam.conf.Config')

import models
init_db()
db = app.config['DB']
import views



