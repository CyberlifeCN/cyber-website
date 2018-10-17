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
# --- refactored entry point for the application ---

import os
import logging
import ssl
import signal
import time
import tornado.httpserver
import tornado.ioloop
from tornado.options import define, options
import tornado.web

# all the route config
import router
from foo.config import Config

MODULE = "website"
MAX_WAIT_SECONDS_BEFORE_SHUTDOWN = 3
CONF_FILE = "/etc/cyberlife/website.conf"

define("port", default=None, help="run on the given port", type=int)
define("debug", default=True, help="run in debug mode")


# The config file parser
def parse_config(conf_file):
    # parse conf file
    conf = Config(conf_file)
    conf.load_conf()
    return conf.get_tornado_port()


# Init logging
def init_logging(port):
    log_file = "/opt/cyberlife/logs/" + MODULE + "." + str(port) + ".log"
    logger = logging.getLogger()
    logger.setLevel(Config.log_level)

    # fh = logging.FileHandler(os.path.join(Config.log_path, log_file))
    fh = logging.handlers.TimedRotatingFileHandler(
        os.path.join(Config.log_path, log_file), when='D', backupCount=10)
    sh = logging.StreamHandler()

    ###########This set the logging level that show on the screen#############
    # sh.setLevel(logging.DEBUG)
    # sh.setLevel(logging.ERROR)

    formatter = logging.Formatter('%(asctime)s -%(module)s:%(filename)s-L%(lineno)d-%(levelname)s: %(message)s')
    fh.setFormatter(formatter)
    sh.setFormatter(formatter)

    logger.addHandler(fh)
    logger.addHandler(sh)
    logging.info("Current log level is : %s",
                 logging.getLevelName(logger.getEffectiveLevel()))


def sig_handler(sig, frame):
    logging.warning('Caught signal: %s', sig)
    tornado.ioloop.IOLoop.instance().add_callback(shutdown)


def shutdown():
    logging.info('Stopping http server')
    http_server.stop()

    logging.info('%r will shutdown in %s seconds ...',
                MODULE,
                MAX_WAIT_SECONDS_BEFORE_SHUTDOWN)
    io_loop = tornado.ioloop.IOLoop.instance()

    deadline = time.time() + MAX_WAIT_SECONDS_BEFORE_SHUTDOWN

    def stop_loop():
        now = time.time()
        if now < deadline and (io_loop._callbacks or io_loop._timeouts):
            io_loop.add_timeout(now + 1, stop_loop)
        else:
            io_loop.stop()
            logging.info('Shutdown')

    stop_loop()


class Application(tornado.web.Application):
    def __init__(self):
        settings = dict(
            # __TODO:_GENERATE_YOUR_OWN_RANDOM_VALUE_HERE__
            # cookie_secret="bZJc2sWbQLKos6GkHn/VB9oXwQt8S0R0kRvJ5/xJ89E=",
            template_path=os.path.join(os.path.dirname(__file__), "templates"),
            static_path=os.path.join(os.path.dirname(__file__), "static"),
            xsrf_cookies=False,
            debug=options.debug,
            # login_url="/auth/api/unauthorized",
            # ssl_options={
            #    "certfile": os.path.join(os.path.abspath("."), "bike-forever.com.crt"),
            #    "keyfile": os.path.join(os.path.abspath("."), "bike-forever.com.key"),
            # }
        )

        handlers = router.map()

        super(Application, self).__init__(handlers, **settings)


def main():

    # tornado.locale.load_gettext_translations(os.path.join(os.path.dirname(__file__), "locale"), "aplan")
    tornado.locale.set_default_locale("en_US")

    #################parse command#######################
    options.parse_command_line()

    ############parse and load config file###############
    options.port = parse_config(CONF_FILE)

    ############init logging##############################
    init_logging(options.port)
    logging.info("%r start! %r", MODULE, options.port)
    # logging.error("Test error:%r start!", MODULE)
    # logging.debug("Test debug:%r start!", MODULE)

    ############setting tornado server#####################
    global http_server

    http_server = tornado.httpserver.HTTPServer(Application())
    http_server.listen(options.port)

    ##############set signal handler#######################
    signal.signal(signal.SIGTERM, sig_handler)
    signal.signal(signal.SIGINT, sig_handler)

    ############start tornado server#######################
    tornado.ioloop.IOLoop.instance().start()
    logging.info('Exit %r', MODULE)


if __name__ == '__main__':
    main()
