#!/usr/bin/env python
#-*- coding: utf-8 -*-
from threading import Thread
from bson import ObjectId
from flask import request, copy_current_request_context
from flask_restful import Resource
from scrumteam import db
from scrumteam.core.estimates import EstimatesHistory
from scrumteam.external.connector import ExtClient, ExtClientFactory

__author__ = 'cybersg'


class GenerateHistoryApi(Resource):

    client = None

    def _connect(self):
        self.client = ExtClient.get_client() or ExtClientFactory.create(
            'jira',
            login=request.json.get('ext_login', None),
            password=request.json.get('ext_password', None)
        )
        self.client.connect()
        return

    def progress(self, task_id=None, current=None, total=None):
        doc = None
        if not task_id:
            if not total:
                raise ValueError("Param 'total' required")
            db.BgTask({'current': current, 'total': total}).save()
            doc = db.BgTask.find().sort('_id', -1)[0]
        else:
            if current:
                doc = db.BgTask.find_and_modify({'_id': ObjectId(task_id)}, {'$set': {'current': current}})
            else:
                doc = db.BgTask.find_one({'_id': ObjectId(task_id)})
        if doc:
            doc['_id'] = str(doc['_id'])
        return doc

    def post(self):
        self._connect()
        estimates = EstimatesHistory(
            self.client, progress_cb=self.progress, db=db
        )
        task_id = estimates.setup_bgtask()
        @copy_current_request_context
        def _start():
            estimates.make_history()
        t = Thread(target=_start)
        t.start()
        return {'task_id': task_id}

    def get(self, task_id):
        return self.progress(task_id=task_id)