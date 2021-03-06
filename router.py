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
from foo import site


def map():

    config = [

        (r'/admin', getattr(admin, 'AdminIndexHandle')),
        (r'/admin/index', getattr(admin, 'AdminIndexHandle')),
        (r'/admin/blog-grid', getattr(admin, 'AdminBlogGridHandle')),
        (r'/admin/blog-create', getattr(admin, 'AdminBlogCreateHandle')),
        (r'/admin/blog-modify/([a-z0-9]+)', getattr(admin, 'AdminBlogModifyHandle')),
        (r'/admin/blog-details/([a-z0-9]+)', getattr(admin, 'AdminBlogDetailsHandle')),
        (r'/admin/article-create', getattr(admin, 'AdminCreateXHR')),
        (r'/admin/article-modify', getattr(admin, 'AdminModifyXHR')),
        (r'/admin/index-2', getattr(admin, 'AdminIndex2Handle')),
        (r'/admin/contact', getattr(admin, 'AdminContactHandle')),
        (r'/admin/about-us', getattr(admin, 'AdminAboutUsHandle')),
        (r'/admin/team', getattr(admin, 'AdminTeamHandle')),
        (r'/admin/faq', getattr(admin, 'AdminFaqHandle')),
        (r'/admin/blog-grid', getattr(admin, 'AdminBlogGridHandle')),
        (r'/admin/blog-list', getattr(admin, 'AdminBlogListHandle')),
        (r'/admin/blog-details', getattr(admin, 'AdminBlogDetailsHandle')),
        (r'/admin/project', getattr(admin, 'AdminProjectHandle')),
        (r'/admin/project-details', getattr(admin, 'AdminProjectDetailsHandle')),
        (r'/admin/service', getattr(admin, 'AdminServiceHandle')),
        (r'/admin/service-details', getattr(admin, 'AdminServiceDetailsHandle')),
        (r'/admin/shop', getattr(admin, 'AdminShopHandle')),
        (r'/admin/shop-single', getattr(admin, 'AdminShopSingleHandle')),
        (r'/admin/404', getattr(admin, 'Admin404Handle')),

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

        (r'/', getattr(site, 'SiteIndexHandle')),
        (r'/index', getattr(site, 'SiteIndexHandle')),
        (r'/index-2', getattr(site, 'SiteIndex2Handle')),
        (r'/contact', getattr(site, 'SiteContactHandle')),
        (r'/about-us', getattr(site, 'SiteAboutUsHandle')),
        (r'/team', getattr(site, 'SiteTeamHandle')),
        (r'/faq', getattr(site, 'SiteFaqHandle')),
        (r'/blog-grid', getattr(site, 'SiteBlogGridHandle')),
        (r'/blog-list', getattr(site, 'SiteBlogListHandle')),
        (r'/blog-details/([a-z0-9]+)', getattr(site, 'SiteBlogDetailsHandle')),
        (r'/project', getattr(site, 'SiteProjectHandle')),
        (r'/project-details/([a-z0-9]+)', getattr(site, 'SiteProjectDetailsHandle')),
        (r'/service', getattr(site, 'SiteServiceHandle')),
        (r'/service-details/([a-z0-9]+)', getattr(site, 'SiteServiceDetailsHandle')),
        (r'/shop', getattr(site, 'SiteShopHandle')),
        (r'/shop-single', getattr(site, 'SiteShopSingleHandle')),
        (r'/publish-agreement', getattr(site, 'SitePublishAgreementHandle')),
        (r'/privacy-statement', getattr(site, 'SitePrivacyStatementHandle')),
        (r'/end-user-license-agreement', getattr(site, 'SiteEndUserLicenseAgreementHandle')),


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
