#!/usr/bin/env python
#-*- coding: utf-8 -*-
__author__ = 'cybersg'

from flask_restful import Api

from cybersg.sgflask import user_api
from scrumteam import app

app.register_blueprint(user_api.user_api)
api = Api(app)
api.add_resource(user_api.UserApi, '/users', endpoint='users')
api.add_resource(user_api.UserApi, '/user/<login>', endpoint='user')