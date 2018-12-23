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
from dao import category_dao

from tornado.escape import json_encode, json_decode
from tornado.httpclient import *
from tornado.httputil import url_concat

from tornado_swagger import swagger


@swagger.model()
class CategoryReq:
    def __init__(self, name):
        self.name = name


# /website/api/categories
class CategoryXHR(BaseHandler):
    # @tornado.web.asynchronous
    @tornado.gen.coroutine
    @swagger.operation(nickname='post')
    def post(self):
        """
            @description: 创建一个分类

            @param body:
            @type body: C{CategoryReq}
            @in body: body
            @required body: True

            @rtype: L{Resp}
            @raise 400: Invalid Input
            @raise 500: Internal Server Error
        """
        logging.debug(self.request.body)

        category = None
        try:
            category = json_decode(self.request.body)
        except:
            logging.warn("Bad Request[400]: create category=[%r]", self.request.body)

            self.set_status(200) # Bad Request
            self.write(JSON.dumps({"errCode":400,"errMsg":"Bad Request"}))
            self.finish()
            return

        category_id = generate_uuid_str()
        category["_id"] = category_id
        category["ctime"] = current_timestamp()
        category["mtime"] = category["ctime"]
        yield category_dao.category_dao().insert(category)
        logging.debug("Success[200]: create category=[%r]", category)

        self.set_status(200) # Created
        self.write(JSON.dumps({"errCode":200,"errMsg":"Success","rs":category_id}))
        self.finish()
        return


    # @tornado.web.asynchronous
    @tornado.gen.coroutine
    @swagger.operation(nickname='get')
    def get(self):
        """
            @description: 查询所有分类

            @rtype: L{ClientsResp}
            @raise 400: Invalid Input
            @raise 500: Internal Server Error
        """
        categories = yield category_dao.category_dao().find_all()

        logging.debug("OK[200]: query categories=[%r]", len(categories))
        self.set_status(200) # OK
        self.write(JSON.dumps({"errCode":200,"errMsg":"Success","rs":categories}))
        self.finish()
        return


# /website/api/categories/([a-z0-9]*)
class CategorySingleXHR(BaseHandler):
    # @tornado.web.asynchronous
    @tornado.gen.coroutine
    @swagger.operation(nickname='get')
    def get(self, _id):
        """
            @description: 读取一个分类

            @rtype: L{Resp}
            @raise 400: Invalid Input
            @raise 500: Internal Server Error
        """
        category = yield category_dao.category_dao().find(_id)
        if category:
            logging.debug("OK(200): got category=[%r] from mysql", category)
            self.set_status(200) # OK
            self.write(JSON.dumps({"errCode":200,"errMsg":"Success","rs":category}))
            self.finish()
            return
        else:
            logging.warn("Not Found[404]: got category=[%r] from mysql", _id)
            self.set_status(200) # Not Found
            self.write(JSON.dumps({"errCode":404,"errMsg":"Not Found"}))
            self.finish()
            return


    @tornado.gen.coroutine
    @swagger.operation(nickname='put')
    def put(self, _id):
        """
            @description: 修改一个分类

            @param body:
            @type body: C{CategoryReq}
            @in body: body
            @required body: True

            @rtype: L{Resp}
            @raise 400: Invalid Input
            @raise 500: Internal Server Error
        """
        logging.debug(self.request.body)

        category = None
        try:
            category = json_decode(self.request.body)
        except:
            logging.warn("Bad Request[400]: update category=[%r]", self.request.body)

            self.set_status(200) # Bad Request
            self.write(JSON.dumps({"errCode":400,"errMsg":"Bad Request"}))
            self.finish()
            return

        category["_id"] = _id
        category["mtime"] = current_timestamp()
        yield category_dao.category_dao().update(category)

        logging.debug("Success[200]: update category=[%r]", category)
        self.set_status(200) # Created
        self.write(JSON.dumps({"errCode":200,"errMsg":"Success"}))
        self.finish()
        return


    @tornado.gen.coroutine
    @swagger.operation(nickname='delete')
    def delete(self, _id):
        """
            @description: 删除一个分类

            @rtype: L{Resp}
            @raise 400: Invalid Input
            @raise 500: Internal Server Error
        """
        yield category_dao.category_dao().delete(_id)

        logging.debug("Success[200]: delete category=[%r]", _id)
        self.set_status(200) # OK
        self.write(JSON.dumps({"errCode":200,"errMsg":"Success"}))
        self.finish()
        return
