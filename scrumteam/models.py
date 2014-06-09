#!/usr/bin/env python
#-*- coding: utf-8 -*-
__author__ = 'cybersg'

from flask_mongokit import Document


class User(Document):
    __collection__ = 'users'
    use_dot_notation = True
    structure = {
        'login': basestring,
        'password': basestring,
        'admin': bool
    }
    required_fields = ['login', 'password']
    default_values = {
        'admin': False
    }


class Sprint(Document):

    __collection__ = 'sprint'
    use_dot_notation = True

    structure = {
        'team': basestring,
        'number': int,
        'name': basestring,
        'project_name': basestring,
        'version': basestring,
        'tasks': [
            {
                'id': basestring,
                'parent_id': basestring,
                'subtasks': list,
                'title': basestring,
                'estimated': None,
                'spent': None,
            }
        ]
    }
    default_values = {
        'number': 0,
        'tasks': []
    }


class BgTask(Document):

    __collection__ = 'bg_task'
    use_dot_notation = True

    structure = {
        'current': int,
        'total': int,
    }
    required_fields = ['current', 'total']

def documents():
    return [User, Sprint, BgTask]