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

from tornado.escape import json_encode, json_decode
from tornado.httpclient import *
from tornado.httputil import url_concat


class WebIndexHandle(tornado.web.RequestHandler):
    def get(self):
        logging.info("GET %r", self.request.uri)
        self.render('index.html')


class WebIndex2Handle(tornado.web.RequestHandler):
    def get(self):
        logging.info("GET %r", self.request.uri)
        self.render('index-2.html')


class WebContactHandle(tornado.web.RequestHandler):
    def get(self):
        logging.info("GET %r", self.request.uri)
        self.render('contact.html')


class WebAboutUsHandle(tornado.web.RequestHandler):
    def get(self):
        logging.info("GET %r", self.request.uri)
        self.render('about-us.html')


class WebTeamHandle(tornado.web.RequestHandler):
    def get(self):
        logging.info("GET %r", self.request.uri)
        self.render('team.html')


class WebFaqHandle(tornado.web.RequestHandler):
    def get(self):
        logging.info("GET %r", self.request.uri)
        self.render('faq.html')


class WebBlogGridHandle(tornado.web.RequestHandler):
    def get(self):
        logging.info("GET %r", self.request.uri)
        self.render('blog-grid.html')


class WebBlogListHandle(tornado.web.RequestHandler):
    def get(self):
        logging.info("GET %r", self.request.uri)
        self.render('blog-list.html')


class WebBlogDetailsHandle(tornado.web.RequestHandler):
    def get(self):
        logging.info("GET %r", self.request.uri)
        self.render('blog-details.html')


class WebProjectHandle(tornado.web.RequestHandler):
    def get(self):
        logging.info("GET %r", self.request.uri)
        self.render('project.html')


class WebProjectDetailsHandle(tornado.web.RequestHandler):
    def get(self):
        logging.info("GET %r", self.request.uri)
        self.render('project-details.html')


class WebServiceHandle(tornado.web.RequestHandler):
    def get(self):
        logging.info("GET %r", self.request.uri)
        self.render('service.html')


class WebServiceDetailsHandle(tornado.web.RequestHandler):
    def get(self):
        logging.info("GET %r", self.request.uri)
        self.render('service-details.html')


class WebShopHandle(tornado.web.RequestHandler):
    def get(self):
        logging.info("GET %r", self.request.uri)
        self.render('shop.html')


class WebShopSingleHandle(tornado.web.RequestHandler):
    def get(self):
        logging.info("GET %r", self.request.uri)
        self.render('shop-single.html')


class WebPageNotFoundHandle(tornado.web.RequestHandler):
    def get(self):
        logging.info("GET %r", self.request.uri)
        self.render('404.html')
