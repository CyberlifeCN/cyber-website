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


import tornado.web
import logging
import time
import sys
import os
import json as JSON # 启用别名，不会跟方法里的局部变量混淆

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../"))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../dao"))

from comm import *
from global_const import *
from base_handler import *
from dao import symbol_dao

from tornado.escape import json_encode, json_decode
from tornado.httpclient import *
from tornado.httputil import url_concat

from tornado_swagger import swagger


@swagger.model()
class SymbolReq:
    def __init__(self, symbol):
        self.symbol = symbol


# /website/api/symbols
class SymbolXHR(BaseHandler):
    # @tornado.web.asynchronous
    # @tornado.gen.coroutine
    @swagger.operation(nickname='post')
    def post(self):
        """
            @description: 创建一个对象

            @param body:
            @type body: C{SymbolReq}
            @in body: body
            @required body: True

            @rtype: L{Resp}
            @raise 400: Invalid Input
            @raise 500: Internal Server Error
        """
        logging.debug(self.request.body)

        symbol = None
        try:
            symbol = json_decode(self.request.body)
        except:
            logging.warn("Bad Request[400]: create symbol=[%r]", self.request.body)

            self.set_status(200) # Bad Request
            self.write(JSON.dumps({"errCode":400,"errMsg":"Bad Request"}))
            self.finish()
            return

        symbol_id= None
        if symbol.has_key("_id"):
            symbol_id = symbol["_id"]
            symbol["mtime"] = current_timestamp()
            symbol_dao.symbol_dao().insert(symbol_id, symbol)
            logging.debug("Success[200]: update symbol=[%r]", symbol)
        else:
            symbol_id = generate_uuid_str()
            symbol["_id"] = symbol_id
            symbol["ctime"] = current_timestamp()
            symbol_dao.symbol_dao().insert(symbol_id, symbol)
            logging.debug("Success[200]: create symbol=[%r]", symbol)
        self.set_status(200) # Created
        self.write(JSON.dumps({"errCode":200,"errMsg":"Success","rs":symbol_id}))
        self.finish()
        return


# /website/api/symbols/([a-z0-9]*)
class SymbolSingleXHR(BaseHandler):
    # @tornado.web.asynchronous
    # @tornado.gen.coroutine
    @swagger.operation(nickname='get')
    def get(self, _id):
        """
            @description: 读取一个对象

            @rtype: L{Resp}
            @raise 400: Invalid Input
            @raise 500: Internal Server Error
        """
        symbol = symbol_dao.symbol_dao().find(_id)
        if symbol:
            logging.debug("OK(200): got symbol=[%r] from ssdb", symbol)
            self.set_status(200) # OK
            self.write(JSON.dumps({"errCode":200,"errMsg":"Success","rs":symbol}))
            self.finish()
            return
        else:
            logging.warn("Not Found[404]: got symbol=[%r] from ssdb", _id)
            self.set_status(200) # Not Found
            self.write(JSON.dumps({"errCode":404,"errMsg":"Not Found"}))
            self.finish()
            return


    @swagger.operation(nickname='put')
    def put(self, _id):
        """
            @description: 修改一个对象

            @param body:
            @type body: C{SymbolReq}
            @in body: body
            @required body: True

            @rtype: L{Resp}
            @raise 400: Invalid Input
            @raise 500: Internal Server Error
        """
        logging.debug(self.request.body)

        symbol = None
        try:
            symbol = json_decode(self.request.body)
        except:
            logging.warn("Bad Request[400]: create symbol=[%r]", self.request.body)

            self.set_status(200) # Bad Request
            self.write(JSON.dumps({"errCode":400,"errMsg":"Bad Request"}))
            self.finish()
            return

        symbol["mtime"] = current_timestamp()
        symbol_dao.symbol_dao().insert(_id, symbol)

        logging.debug("Success[200]: update symbol=[%r]", symbol)
        self.set_status(200) # Created
        self.write(JSON.dumps({"errCode":200,"errMsg":"Success"}))
        self.finish()
        return


    @swagger.operation(nickname='delete')
    def delete(self, _id):
        """
            @description: 删除一个对象

            @rtype: L{Resp}
            @raise 400: Invalid Input
            @raise 500: Internal Server Error
        """
        symbol_dao.symbol_dao().delete(_id)

        logging.debug("Success[200]: delete symbol=[%r]", _id)
        self.set_status(200) # OK
        self.write(JSON.dumps({"errCode":200,"errMsg":"Success"}))
        self.finish()
        return
