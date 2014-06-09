#!/usr/bin/env python
#-*- coding: utf-8 -*-

__author__ = 'cybersg'


class Version(object):

    def __init__(self, name):
        self.name = name


class Sprint(object):

    def __init__(self, num, client):
        self.client = client
        self.number = num
        self.name = 'Sprint {0}'.format(str(num))
        self.version = self.client.get_version_name(self.name)
        self.tasks = [Task(client, **t) for t in client.get_sprint_tasks(self)]

    def to_dict(self):
        obj = {
            'number': self.number,
            'name': self.name,
            'version': self.version,
            'project_name': self.client.project_name,
            'team': self.client.team,
            'tasks': []
        }
        for t in self.tasks:
            obj['tasks'].append(t.to_dict())
        return obj


class Task(object):

    def __init__(self, client, id=None, title=None, parent_id=None, estimated=None, spent=None):
        self.id = id
        self.title = title
        self.parent_id = parent_id
        self.estimated = estimated
        self.spent = spent
        self.subtasks = [
            Task(client, **t) for t in client.get_subtasks(self.id)
        ]

    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'parent_id': self.parent_id,
            'estimated': self.estimated,
            'spent': self.spent,
            'subtasks': [t.to_dict() for t in self.subtasks],
        }
