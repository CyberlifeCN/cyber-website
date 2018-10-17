#!/usr/bin/env python2.7
# _*_ coding: utf-8_*_
#
#   Author  :   Thomas
#   E-mail  :   thomas@cloudancing.cn
#   Date    :   2018/07/13
#   Desc    :   Test db

import ConfigParser
import os
import logging


class Config:

    ###########################tornado config######################
    port = 7020

    #####################log config########################
    log_level = None
    log_path = None

    #####################default value config########################

    ###init func###
    def __init__(self, conf_file):
        self.conf_file = conf_file
        self.cf = None

    ###load config###
    def load_conf(self):
        if os.path.isfile(self.conf_file):

            self.cf = ConfigParser.ConfigParser()
            self.cf.read(self.conf_file)

            ## get tornado config
            Config.tornado_port = self.get_tornado_port()

            ## get log config
            Config.log_level = self.get_log_level()
            Config.log_path = self.get_log_path()

            return 0
        else:
            return -1

    def get_tornado_port(self):
        '''  get tornado port '''
        port = self.cf.get("tornado", "tornado_port")
        return int(port)

    def get_log_path(self):
        '''  get log path '''
        path = self.cf.get("log", "log_path")
        if path == "" or path == None or not os.path.exists(path):
            return os.path.join(os.getcwd(), "log")
        else:
            return path

    def get_log_level(self):
        '''  get log path '''
        level = self.cf.get("log", "log_level")
        if level == "DEBUG":
            return logging.DEBUG
        elif level == "INFO":
            return logging.INFO
        elif level == "WARNING":
            return logging.WARNING
        elif level == "ERROR":
            return logging.ERROR
        else:
            return logging.INFO
