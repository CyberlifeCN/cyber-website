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

# import MySQLdb as mysql
from tornado import ioloop, gen
from mysql_connection_pool import *
import json as JSON # 启用别名，不会跟方法里的局部变量混淆

 # DROP TABLE IF EXISTS  `article`;
 # CREATE TABLE `article` (
 #   `_id` char(32) NOT NULL COMMENT 'uuid',
 #   `ctime` bigint(19) NOT NULL DEFAULT '0',
 #   `mtime` bigint(19) NOT NULL DEFAULT '0',
 #   PRIMARY KEY (`_id`)
 # ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
class article_dao(singleton):

    @gen.coroutine
    def insert(self, data):
        # 执行一个查询
        sql = "INSERT INTO article(_id, ctime, mtime) VALUES ('" +\
            data['_id'] + "','" +\
            str(data['ctime']) + "','" +\
            str(data['mtime']) +\
            "')"
        logging.debug("sql=[%r]", sql)
        cur = yield Mysql_Connection_Pool().get_pool().execute(sql, ())
        # cur.commit()


    @gen.coroutine
    def find(self, _id):
        # 执行一个查询
        sql = "SELECT _id, ctime, mtime"+\
            " FROM article " +\
            " WHERE _id='" + _id +\
            "'"
        logging.debug("sql=[%r]", sql)
        cur = yield Mysql_Connection_Pool().get_pool().execute(sql, ())
        # 取得上个查询的结果，是数组
        data = cur.fetchone()
        logging.debug("client: %r", data)
        if data:
            info = {
                "_id":data[0],
                "ctime":data[1],
                "mtime":data[2],
            }
            raise gen.Return(info)
        else:
            raise gen.Return(None)


    @gen.coroutine
    def find_pagination(self, idx, limit):
        # 执行一个查询
        sql = "SELECT _id, ctime, mtime" +\
            " FROM article ORDER BY ctime desc" +\
            " LIMIT " + str(idx) + "," + str(limit)
        logging.debug("sql: %r", sql)

        cur = yield Mysql_Connection_Pool().get_pool().execute(sql, ())
        array = []
        # 取得上个查询的结果，是数组
        datas = cur.fetchall()
        for data in datas:
            info = {
                "_id":data[0],
                "ctime":data[1],
                "mtime":data[2],
            }
            array.append(info)
        raise gen.Return(array)


    @gen.coroutine
    def count_pagination(self, idx, limit):
        sql = "SELECT count(*) FROM article"
        logging.debug("sql: %r", sql)
        cur = yield Mysql_Connection_Pool().get_pool().execute(sql, ())

        # 取得上个查询的结果，是数组
        data = cur.fetchone()
        logging.debug("count: %r", data)
        if data:
            raise gen.Return(data[0])
        else:
            raise gen.Return(0)


    @gen.coroutine
    def delete(self, _id):
        # 执行一个查询
        sql = "DELETE FROM article " +\
            " WHERE _id='" + _id + "'"
        logging.debug("sql=[%r]", sql)
        cur = yield Mysql_Connection_Pool().get_pool().execute(sql, ())
        # cur.commit()
