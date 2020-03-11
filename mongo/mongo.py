# -*- coding: utf-8 -*-
# @filename mongo.py
# @author yw
# @email uevol@outlook.com
# @description connect mongodb repliaction set
# @created 2020-03-11T17:12:34.875Z+08:00
# @last-modified 2020-03-11T18:05:25.278Z+08:00
import urllib

from pymongo import MongoClient


class Singleton(object):
    """单例类
    """
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(Singleton, cls).__new__(cls, *args, **kwargs)
        return cls._instance


class MongoDB(Singleton):
    """docstring for MongoDB"""
    def __init__(
                self,
                db_user=None,
                db_password=None,
                db_host=None,
                auth_db=None,
                replicaset='rs0',
                db_name='test'):
        super(MongoDB, self).__init__()
        self._name = db_name
        self._user = db_user
        if self._user:
            self._user = urllib.quote_plus(self._user)
        self._password = db_password
        if self._password:
            self._password = urllib.quote_plus(self._password)
        self._auth_db = auth_db
        self._host = db_host
        self._replication = replicaset
        self.client = self._connect()
        self.db = self.client[self._name]

    def _connect(self):
        if isinstance(self._host, (list, tuple)):
            host = ','.join(self._host)

        if self._replication:
            if self._user and self._password:
                uri = 'mongodb://%s:%s@%s/?replicaset=%s&authSource=%s' % (
                    self._user, self._password, host, self._replication,
                    self._auth_db)
            else:
                uri = 'mongodb://%s/?replicaset=%s' % (host, self._replication)
        else:
            if self._user and self._password:
                uri = 'mongodb://%s:%s@%s&authSource=%s' % (
                    self._user,
                    self._password,
                    host,
                    self._auth_db)
            else:
                uri = 'mongodb://%s' % (host)

        return MongoClient(uri)

    def __del__(self):
        self.client.close()
