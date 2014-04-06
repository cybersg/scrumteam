#!/usr/bin/env python
#-*- coding: utf-8 -*-
__author__ = 'cybersg'

from flask import Flask
from flask_mongokit import MongoKit

def init_db():
    db = MongoKit(app)
    app.config['DB'] = db

app = Flask(__name__)
app.config.from_object('scrumteam.conf.Config')

init_db()
import models
models.documents()

import views



