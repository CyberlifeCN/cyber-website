#!/usr/bin/env python
# _*_ coding: utf-8_*_
#
# Copyright 2016 7x24hs.com
# thomas@7x24hs.com
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.

import logging
import sys
import os
import time
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../"))
from comm import singleton
from global_const import *

from tornado import ioloop, gen
from tornado_mysql import pools
from tornado_mysql import cursors


class Singleton(object):
    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, '_instance'):
            cls._instance = super(Singleton, cls).__new__(cls, *args, **kwargs)
        return cls._instance


class Mysql_Connection_Pool(Singleton):
    __connection_pool = None

    def __init__(self):
        if self.__connection_pool is None:
            self.__connection_pool = pools.Pool(
                dict(host=MYSQL_HOST,
                    user=MYSQL_USR,
                    passwd=MYSQL_PWD,
                    db=MYSQL_DB,
                    charset=MYSQL_CHARSET,
                ),
                max_idle_connections=POOL_MAX_IDLE_CONNECTIONS,
                max_recycle_sec=POOL_MAX_RECYCLE_SEC,
                max_open_connections=POOL_MAX_OPEN_CONNECTIONS,
            )
            logging.info("~~~~~ CONNECTION_POOL INIT: ......");
        else:
            logging.debug("~~~~~ CONNECTION_POOL: has inited");


    def get_pool(self):
        return self.__connection_pool


@gen.coroutine
def worker(n):
    for i in range(10):
        t = 1
        print(n, "sleeping", t, "seconds")

        level2_category_id = "fa2133f6c5ec11e7b39e00163e045306"
        idx = 0
        limit = 20
        sql = "SELECT c.book_md5, c.category_id, c.level2_category_id, c._seq, i.name, i.cover_img, i.author, i.url, i.ctime "+\
            " FROM book_category c, book_info i"+\
            " WHERE c.level2_category_id='"+level2_category_id+\
            "' AND c.book_md5=i.md5"+\
            " AND i._status=100"+\
            " LIMIT "+str(idx)+","+str(limit)
        print ("sql=[%s]" % sql)

        cur = yield Mysql_Connection_Pool().get_pool().execute(sql, ())
        print(n, cur.fetchall())


@gen.coroutine
def main():
    workers = [worker(i) for i in range(10)]
    yield workers


# ioloop.IOLoop.current().run_sync(main)
# print(Mysql_Connection_Pool().get_pool()._opened_conns)
