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
from dao import article_categories_dao

from tornado.escape import json_encode, json_decode
from tornado.httpclient import *
from tornado.httputil import url_concat

from tornado_swagger import swagger


@swagger.model()
class CategoriesReq:
    def __init__(self, ids):
        self.ids = ids


# /website/api/articles/([a-z0-9]*)/categories
class ArticleCategoriesXHR(BaseHandler):
    # @tornado.web.asynchronous
    @tornado.gen.coroutine
    @swagger.operation(nickname='put')
    def put(self, article_id):
        """
            @description: 修改一个文章的所有分类

            @param body:
            @type body: C{CategoriesReq}
            @in body: body
            @required body: True

            @rtype: L{Resp}
            @raise 400: Invalid Input
            @raise 500: Internal Server Error
        """
        logging.debug(self.request.body)

        categories = None
        try:
            categories = json_decode(self.request.body)
        except:
            logging.warn("Bad Request[400]: update article=[%r]", self.request.body)

            self.set_status(200) # Bad Request
            self.write(JSON.dumps({"errCode":400,"errMsg":"Bad Request"}))
            self.finish()
            return

        yield article_categories_dao.article_categories_dao().delete_all(article_id)
        for category_id in categories:
            yield article_categories_dao.article_categories_dao().insert(article_id, category_id)
        logging.debug("Success[200]: update article=[%r] categories=[%r]", article_id, categories)

        self.set_status(200) # Created
        self.write(JSON.dumps({"errCode":200,"errMsg":"Success"}))
        self.finish()
        return


    # @tornado.web.asynchronous
    @tornado.gen.coroutine
    @swagger.operation(nickname='get')
    def get(self, article_id):
        """
            @description: 查询一个文章的所有分类

            @rtype: L{ClientsResp}
            @raise 400: Invalid Input
            @raise 500: Internal Server Error
        """
        categories = yield article_categories_dao.article_categories_dao().find_all(article_id)
        for category in categories:
            category_info = yield category_dao.category_dao().find(category["category_id"])
            category["name"] = category_info["name"]

        logging.debug("OK[200]: query article=[%r] categories=[%r]", article_id, len(categories))
        self.set_status(200) # OK
        self.write(JSON.dumps({"errCode":200,"errMsg":"Success","rs":categories}))
        self.finish()
        return
