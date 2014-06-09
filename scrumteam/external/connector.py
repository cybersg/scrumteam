#!/usr/bin/env python
#-*- coding: utf-8 -*-
__author__ = 'cybersg'

from flask import g
from jira.client import JIRA
import re

from scrumteam import app


class ExtClientFactory(object):

    @classmethod
    def create(cls, type, *args, **kwargs):
        if type == 'jira':
            return JiraExtClient(*args, **kwargs)
        else:
            raise NotImplementedError("Unknown external client: {0}".format(type))


class ExtClient(object):

    def __init__(self, login=None, password=None):
        self.url = None
        self.login = login
        self.password = password

    @classmethod
    def get_client(cls):
        return getattr(g, 'external_client', None)

    def connect(self):
        return None


class JiraExtClient(ExtClient):

    client = None

    def __init__(self, login, password):
        super(JiraExtClient, self).__init__(login, password)
        self.url = 'https://jira.hurra.com'
        self.project_name = 'SEM'
        self.team = 'Team B'

    def connect(self):
        jira = JIRA(
            options={'server': self.url},
            basic_auth=(self.login, self.password)
        )
        self.client = jira
        self.project = self.client.project(self.project_name)
        g.external_client = self
        return

    def get_versions(self, start_sprint, end_sprint):
        def f(x):
            m = re.search('^Sprint (\d{2})$', x.name)
            if m:
                if 37 < int(m.group(1)) < 60:
                    return True
            return False

        return sorted(
            [v for v in self.project.versions if f(v) and hasattr(v, "releaseDate")],
            key=lambda v: v.releaseDate
        )

    def get_version_name(self, sprint_name):
        name = None
        try:
            name = [v.name for v in self.project.versions if v.name == sprint_name][0]
        except IndexError:
            app.logger.error('Project {0} versions not available'.format(self.project_name))
        return name

    def get_sprint_tasks(self, sprint):
        return [
            self.get_task_info(i.key) for i in self.client.search_issues(
                'project = "{0}" AND component = "{1}" AND fixVersion = "{2}" AND type != "Sub-task"'.format(
                self.project_name, self.team, sprint.version
                )
            )
        ]

    def get_task_info(self, id):
        task = self.client.issue(id)
        info = {
            'id': task.key,
            'title': task.fields.summary,
            'estimated': task.fields.timeoriginalestimate,
            'spent': task.fields.timespent
        }
        if getattr(task, 'parent', None) is not None:
            info['parent_id'] = task.parent.key
        return info

    def get_subtasks(self, id):
        return [
            self.get_task_info(t.key) for t in
            self.client.search_issues('parent = "{}"'.format(id))
        ]



