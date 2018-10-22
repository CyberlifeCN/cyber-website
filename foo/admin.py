#!/usr/bin/env python
# _*_ coding: utf-8_*_
#
# Copyright 2016-2017 7x24hs.com
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

from comm import *
from global_const import *
from base_handler import *
from dao import symbol_dao
from dao import article_dao

from tornado.escape import json_encode, json_decode
from tornado.httpclient import HTTPClient
from tornado.httputil import url_concat


class AdminBlogGridHandle(tornado.web.RequestHandler):
    def get(self):
        logging.info("GET %r", self.request.uri)
        self.render('admin/blog-grid.html')


class AdminBlogCreateHandle(tornado.web.RequestHandler):
    def get(self):
        logging.info("GET %r", self.request.uri)
        self.render('admin/blog-create.html')


class AdminBlogModifyHandle(tornado.web.RequestHandler):
    def get(self, article_id):
        logging.info("GET %r", self.request.uri)
        data = symbol_dao.symbol_dao().find(article_id)
        logging.info("GET article=%r", data)
        self.render('admin/blog-modify.html', article_id=article_id, article=data["symbol"])


class AdminBlogDetailsHandle(tornado.web.RequestHandler):
    def get(self, article_id):
        logging.info("GET %r", self.request.uri)
        data = symbol_dao.symbol_dao().find(article_id)
        logging.info("GET article=%r", data)
        self.render('admin/blog-details.html', article_id=article_id, article=data["symbol"])


class AdminCreateXHR(tornado.web.RequestHandler):
    @tornado.gen.coroutine
    def post(self):
        logging.info("POST %r", self.request.uri)

        title = self.get_argument("title", "")
        logging.info("got title %r", title)
        article_img = self.get_argument("article_img", "")
        logging.info("got article_img %r", article_img)
        paragraphs = self.get_argument("paragraphs", "")
        logging.info("got paragraphs %r", paragraphs)

        symbol = {"symbol":{"title":title, "img":article_img, "paragraphs":paragraphs}}
        symbol_id = generate_uuid_str()
        symbol["_id"] = symbol_id
        symbol["ctime"] = current_timestamp()
        symbol["mtime"] = symbol["ctime"]
        symbol_dao.symbol_dao().insert(symbol_id, symbol)
        yield article_dao.article_dao().insert(symbol)
        logging.info("Success[200]: create symbol=[%r]", symbol)

        self.redirect("/admin/blog-grid")


class AdminModifyXHR(tornado.web.RequestHandler):
    @tornado.gen.coroutine
    def post(self):
        logging.info("POST %r", self.request.uri)

        article_id = self.get_argument("article_id", "")
        logging.info("got article_id %r", article_id)
        title = self.get_argument("title", "")
        logging.info("got title %r", title)
        article_img = self.get_argument("article_img", "")
        logging.info("got article_img %r", article_img)
        paragraphs = self.get_argument("paragraphs", "")
        logging.info("got paragraphs %r", paragraphs)

        symbol = {"symbol":{"title":title, "img":article_img, "paragraphs":paragraphs}}
        symbol["_id"] = article_id
        symbol["mtime"] = current_timestamp()
        symbol_dao.symbol_dao().insert(article_id, symbol)
        logging.info("Success[200]: modify symbol=[%r]", symbol)

        self.redirect("/admin/blog-details/" + article_id)


class AdminBlogListHandle(tornado.web.RequestHandler):
    def get(self):
        logging.info("GET %r", self.request.uri)
        self.render('admin/blog-list.html')
