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
from dao import category_dao
from dao import article_categories_dao

from tornado.escape import json_encode, json_decode
from tornado.httpclient import *
from tornado.httputil import url_concat


class SiteIndexHandle(tornado.web.RequestHandler):
    @tornado.gen.coroutine
    def get(self):
        category_id = "db957c6ed38611e8be700017fa03296f"
        articles = yield article_categories_dao.article_categories_dao().find_pagination(category_id, 0, 3)
        news = []
        for article in articles:
            data = symbol_dao.symbol_dao().find(article["article_id"])
            data["mtime"] = timestamp_to_date(data["mtime"])
            news.append(data)

        category_id = "9771de04d38811e8ab5c0017fa03296f"
        articles = yield article_categories_dao.article_categories_dao().find_pagination(category_id, 0, 3)
        projects = []
        for article in articles:
            data = symbol_dao.symbol_dao().find(article["article_id"])
            projects.append(data)

        category_id = "475d7b40d37d11e887b20017fa03296f"
        articles = yield article_categories_dao.article_categories_dao().find_pagination(category_id, 0, 3)
        services = []
        for article in articles:
            data = symbol_dao.symbol_dao().find(article["article_id"])
            services.append(data)

        self.render('index.html',
            services=services,
            projects=projects,
            news=news)


class SiteIndex2Handle(tornado.web.RequestHandler):
    def get(self):
        self.render('index-2.html')


class SiteContactHandle(tornado.web.RequestHandler):
    def get(self):
        self.render('contact.html')


class SiteAboutUsHandle(tornado.web.RequestHandler):
    def get(self):
        self.render('about-us.html')


class SiteTeamHandle(tornado.web.RequestHandler):
    def get(self):
        self.render('team.html')


class SiteFaqHandle(tornado.web.RequestHandler):
    def get(self):
        self.render('faq.html')


class SiteBlogGridHandle(tornado.web.RequestHandler):
    def get(self):
        self.render('blog-grid.html')


class SiteBlogListHandle(tornado.web.RequestHandler):
    def get(self):
        self.render('blog-list.html')


class SiteBlogDetailsHandle(tornado.web.RequestHandler):
    @tornado.gen.coroutine
    def get(self, article_id):
        data = symbol_dao.symbol_dao().find(article_id)
        data["symbol"]["mtime"] = timestamp_to_datehourmin(data["mtime"])
        categories = yield category_dao.category_dao().find_all()
        self.render('blog-details.html',
            article=data["symbol"],
            categories=categories)


class SiteProjectHandle(tornado.web.RequestHandler):
    def get(self):
        self.render('project.html')


class SiteProjectDetailsHandle(tornado.web.RequestHandler):
    def get(self, article_id):
        data = symbol_dao.symbol_dao().find(article_id)
        self.render('project-details.html',
            article=data["symbol"])


class SiteServiceHandle(tornado.web.RequestHandler):
    def get(self):
        self.render('service.html')


class SiteServiceDetailsHandle(tornado.web.RequestHandler):
    def get(self, article_id):
        data = symbol_dao.symbol_dao().find(article_id)
        self.render('service-details.html',
            article=data["symbol"])


class SiteShopHandle(tornado.web.RequestHandler):
    def get(self):
        self.render('shop.html')


class SiteShopSingleHandle(tornado.web.RequestHandler):
    def get(self):
        self.render('shop-single.html')


class SitePublishAgreementHandle(tornado.web.RequestHandler):
    def get(self):
        self.render('publish-agreement.html')


class SitePrivacyStatementHandle(tornado.web.RequestHandler):
    def get(self):
        self.render('privacy-statement.html')


class SiteEndUserLicenseAgreementHandle(tornado.web.RequestHandler):
    def get(self):
        self.render('end-user-license-agreement.html')


class SitePageNotFoundHandle(tornado.web.RequestHandler):
    def get(self):
        self.render('404.html')
