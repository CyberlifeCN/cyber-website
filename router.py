#!/usr/bin/env python
# _*_ coding: utf-8_*_
#
# Copyright 2018 cyber-life.cn
# thomas@cyber-life.cn
# @2018/05/3
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
#
# genral application route config:
# simplify the router config by dinamic load class

import sys
import os
import tornado.web

from foo import comm
from foo import base_handler
from foo import api_symbol
from foo import api_article
from foo import api_category
from foo import api_article_categories
from foo import api_category_articles
from foo import web
from foo import admin


def map():

    config = [

        (r'/admin/blog-grid', getattr(admin, 'AdminBlogGridHandle')),
        (r'/admin/blog-create', getattr(admin, 'AdminBlogCreateHandle')),
        (r'/admin/articles', getattr(admin, 'AdminArticlesXHR')),

        (r'/', getattr(web, 'WebIndexHandle')),
        (r'/website/index', getattr(web, 'WebIndexHandle')),
        (r'/website/index-2', getattr(web, 'WebIndex2Handle')),
        (r'/website/contact', getattr(web, 'WebContactHandle')),
        (r'/website/about-us', getattr(web, 'WebAboutUsHandle')),
        (r'/website/team', getattr(web, 'WebTeamHandle')),
        (r'/website/faq', getattr(web, 'WebFaqHandle')),
        (r'/website/blog-grid', getattr(web, 'WebBlogGridHandle')),
        (r'/website/blog-list', getattr(web, 'WebBlogListHandle')),
        (r'/website/blog-details', getattr(web, 'WebBlogDetailsHandle')),
        (r'/website/project', getattr(web, 'WebProjectHandle')),
        (r'/website/project-details', getattr(web, 'WebProjectDetailsHandle')),
        (r'/website/service', getattr(web, 'WebServiceHandle')),
        (r'/website/service-details', getattr(web, 'WebServiceDetailsHandle')),
        (r'/website/shop', getattr(web, 'WebShopHandle')),
        (r'/website/shop-single', getattr(web, 'WebShopSingleHandle')),

        (r'/website/api/symbols', getattr(api_symbol, 'SymbolXHR')),
        (r'/website/api/symbols/([a-z0-9]+)', getattr(api_symbol, 'SymbolSingleXHR')),
        (r'/website/api/articles', getattr(api_article, 'ArticleXHR')),
        (r'/website/api/articles/([a-z0-9]+)', getattr(api_article, 'ArticleSingleXHR')),
        (r'/website/api/categories', getattr(api_category, 'CategoryXHR')),
        (r'/website/api/categories/([a-z0-9]+)', getattr(api_category, 'CategorySingleXHR')),
        (r'/website/api/articles/([a-z0-9]+)/categories', getattr(api_article_categories, 'ArticleCategoriesXHR')),
        (r'/website/api/categories/([a-z0-9]+)/articles', getattr(api_category_articles, 'CategoryArticlesXHR')),

        # comm
        ('.*', getattr(web, 'WebPageNotFoundHandle'))

    ]

    return config
