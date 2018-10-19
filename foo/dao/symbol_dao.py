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

# encoding=utf8
import sys, os
reload(sys)
sys.setdefaultencoding('utf8')
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../"))

from comm import singleton
from global_const import *

import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../"))
import logging
import json as JSON # 启用别名，不会跟方法里的局部变量混淆


from SSDB import SSDB
# /usr/local/ssdb/ssdb-server -d /usr/local/ssdb/ssdb.conf -s start
# help http://ssdb.io/docs/zh_cn/php/
try:
	pass
	ssdb = SSDB(SSDB_SERVER, SSDB_PORT)
except Exception , e:
	pass
	print e
	sys.exit(0)


# symbol options: any object
class symbol_dao(singleton):


    def insert(self, _id, symbol):
        json = JSON.dumps(symbol)
        logging.debug("insert|%r", json)
        ssdb.request('set', [_id, json])


    def delete(self, _id):
        logging.debug("delete|%r", _id)
        ssdb.request('del', [_id])


    def find(self, _id):
        resp = ssdb.request('get', [_id])
        logging.debug("select|%r|%r", _id, resp)
        if resp.data:
            return JSON.loads(resp.data)
        else:
            return None
