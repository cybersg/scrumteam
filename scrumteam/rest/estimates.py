#!/usr/bin/env python
#-*- coding: utf-8 -*-
__author__ = 'cybersg'

from flask_restful import Resource

from scrumteam import db
from scrumteam.core.estimates import EstimatesHistory


class EstimatesApi(Resource):

    def get(self):
        return sorted(
            [{'number': s.number, 'name': s.name} for s in db.Sprint.find()],
            key=lambda s: s['number']
        )


class HistoryApi(Resource):

    def get(self, start_sprint):
        return EstimatesHistory(db=db, start_sprint=start_sprint).get_history()


class SearchTasksApi(Resource):

    def get(self, phrase):
        rs =  EstimatesHistory(db=db).search_tasks(phrase)
        from scrumteam import app
        app.logger.debug(rs)
        return rs