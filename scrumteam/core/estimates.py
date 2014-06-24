#!/usr/bin/env python
#-*- coding: utf-8 -*-
__author__ = 'cybersg'

from scrumteam import db
from scrumteam.core.sprint import Sprint, Version


class EstimatesHistory(object):

    def __init__(self, client=None, start_sprint=None, end_sprint=None, progress_cb=None, db=None):
        self.client = client
        self.db = db
        self.start_sprint = int(start_sprint or 0)
        self.end_sprint = int(end_sprint or  0)
        self.progress_cb = progress_cb
        self.progress_id = 0
        self.firstver = None
        self.lastver = None
        self._set_versions()

    def _set_versions(self):
        versions = []
        if self.client:
            versions = self.client.get_versions(self.start_sprint, self.end_sprint)
        else:
            versions = [Version(s.version) for s in db.Sprint.find().sort([('number', 1)])]

        if self.end_sprint:
            self.lastver = [v for v in versions if v.name == "Sprint {}".format(self.end_sprint)][0]
        else:
            self.lastver = versions[-1]
            self.end_sprint = int(self.lastver.name.replace('Sprint ', ''))
        if self.start_sprint:
            self.firstver = [v for v in versions if v.name == "Sprint {}".format(self.start_sprint)][0]
        else:
            self.firstver = versions[0]
            self.start_sprint = int(self.firstver.name.replace('Sprint ', ''))

    def setup_bgtask(self):
        total = self.end_sprint - self.start_sprint
        doc = self.progress_cb(total=total, current=0)
        self.progress_id = doc['_id']
        return self.progress_id

    def make_history(self):
        n = 0
        for d in self.db.Sprint.find():
            d.delete()
        for i in range(self.start_sprint, self.end_sprint + 1):
            sprint_doc = self.db.Sprint(Sprint(i, client=self.client).to_dict())
            self.progress_cb(task_id=self.progress_id, current=n)
            n = n + 1
            sprint_doc.save()
        return


    def get_history(self):
        sprints = []
        for s in self.db.Sprint.find(
            {'number': {'$gte': self.start_sprint, '$lte': self.end_sprint} },
            {
                'name': 1, '_id': 0,
                'tasks.title': 1, 'tasks.estimated': 1, 'tasks.spent': 1,
                'tasks.subtasks.title': 1, 'tasks.subtasks.estimated' :1, 'tasks.subtasks.spent': 1
            }
        ):
            sprints.append(
                {
                    'name': s.name,
                    'tasks': s.tasks
                }
            )
        return sprints

    def search_tasks(self, phrase):

        results = []
        # aggr = self.db.Sprint.collection.aggregate([
        #     {'$project': {
        #         'name': 1, '_id': 0,
        #         'tasks.title': 1, 'tasks.estimated': 1, 'tasks.spent': 1,
        #         'tasks.subtasks.title': 1, 'tasks.subtasks.estimated' :1, 'tasks.subtasks.spent': 1
        #     }},
        #     {'$unwind': 'tasks'},
        #     {'$match': { '$or': [
        #         {'tasks.title': {'$regex': '.*' + phrase + '.*', '$options': 'i'}},
        #         {'tasks.subtasks.title': {'$regex': '.*' + phrase + '.*', '$options': 'i'}}
        #     ]}},
        #     {'$sort': {'number': 1}}
        # ])
        # for r in aggr['result']:
        #     # from scrumteam import app
        #     # app.logger.debug(r)
        #     # break
        #     r['tasks'] = [r['tasks']]
        #     results.append(r)
        results = []
        sprints = {}
        tasks = {}
        for sprint in self.db.Sprint.collection.aggregate([
            {'$unwind': "$tasks"},
            {'$unwind': "$tasks.subtasks"},
            {'$match': { '$or': [
                {'tasks.title': {'$regex': '.*' + phrase + '.*', '$options': 'i'}},
                {'tasks.subtasks.title': {'$regex': '.*' + phrase + '.*', '$options': 'i'}}
            ]}},
            {'$group': {'_id':  "$name", 'tasks': {'$addToSet': "$tasks"} }},
            #{'$group': {'_id': {'name': "$_id", 'title': "$tasks.title"}, 'tasks.subtasks': {'$addToSet': "$tasks.subtasks"} } },
            #{'$group': {'_id': {'name': '$name', 'subtasks': {'$push': '$tasks.subtasks'} }}},
            {'$project': {
                'tasks.title': 1, 'tasks.estimated': 1, 'tasks.spent': 1,
                'tasks.subtasks.title': 1, 'tasks.subtasks.estimated': 1, 'tasks.subtasks.spent': 1,
            }},
            {'$sort': {'name': 1}}
        ])['result']:
            tasks = {}
            for t in sprint['tasks']:
                if t['title'] not in tasks:
                    tasks[t['title']] = {
                        'title': t['title'],
                        'estimated': t['estimated'],
                        'spent': t['spent'],
                        'subtasks': []
                    }
                tasks[t['title']]['subtasks'].append(t['subtasks'])
            sprint['tasks'] = tasks.values()
            results.append(sprint)

        return results