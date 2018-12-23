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
from dao import article_categories_dao

from tornado.escape import json_encode, json_decode
from tornado.httpclient import *
from tornado.httputil import url_concat

from tornado_swagger import swagger


# /website/api/categories/([a-z0-9]*/articles
class CategoryArticlesXHR(BaseHandler):

    # @tornado.web.asynchronous
    @tornado.gen.coroutine
    @swagger.operation(nickname='get')
    def get(self, category_id):
        """
            @description: 分页查询一个分类的所有文章

            @param page: default=1
            @type page: L{int}
            @in page: query
            @required page: False

            @param limit: default=20
            @type limit: L{int}
            @in limit: query
            @required limit: False

            @rtype: L{ClientsResp}
            @raise 400: Invalid Input
            @raise 500: Internal Server Error
        """
        page = self.get_argument("page", 1)
        limit = self.get_argument("limit", 20)

        idx = (int(page) - 1) * int(limit)
        total_num = 0
        total_page = 0

        articles = yield article_categories_dao.article_categories_dao().find_pagination(category_id, idx, limit)
        total_num = yield article_categories_dao.article_categories_dao().count_pagination(category_id, idx, limit)

        datas = []
        for article in articles:
            data = symbol_dao.symbol_dao().find(article["article_id"])
            datas.append(data)

        if total_num % int(limit) == 0:
            total_page = int(total_num / int(limit))
        else:
            total_page = int(total_num / int(limit)) + 1
        rs = {"page":page, "total_page":total_page, "data":datas}

        logging.debug("OK[200]: query articles: page=[%r] total_page=[%r] num=[%r]", page, total_page, len(datas))
        self.set_status(200) # OK
        self.write(JSON.dumps({"errCode":200,"errMsg":"Success","rs":rs}))
        self.finish()
        return
