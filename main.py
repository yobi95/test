#!/usr/bin/env python3
# -*- coding:utf-8 -*-
"""
Flask框架的web服务
作为主文件运行，初始化数据库，并启动web服务器。
建立flask app，设置logger和错误页面路由
注册蓝图
"""
import base64
import logging
import multiprocessing
import queue
import re
import threading
import time
import traceback
from multiprocessing import Process
from urllib import parse
import os

import MySQLdb
from DBUtils.PooledDB import PooledDB
from flask import (Flask, abort, make_response, redirect, render_template,
                   request, url_for)
from flask_mail import Mail

import funcs
import global_var as gv
import preenv

from api_loginout import loggeduser
from api_loginout import api_loginout
from api_user import api_user
from api_children import api_children
from api_status import api_status
from api_selector import api_selector
from api_files import api_files
from pg_loginout import pg_loginout
from pg_index import pg_index
from pg_child import pg_child
from pg_user import pg_user
from pg_status import pg_status
import configparser

# init-------------------------------------------------

# debug模式
MODE_DEBUG = False

# 构建app，设置log，设置config，设置mail
config = configparser.ConfigParser()
config.read("config.conf", encoding='utf-8')
funcs.mkdir("logs")
logger = funcs.buildLogger(None, "logs/main.log", True)
app = Flask(__name__)
app.logger = logger
app.config['JSON_AS_ASCII']=False
#app.config['JSONIFY_PRETTYPRINT_REGULAR']=False


app.config['MAIL_SERVER'] = config.get('mail', 'smtp_server')
app.config['MAIL_PORT'] = config.getint('mail', 'port')
app.config['MAIL_USE_TLS'] = config.getboolean('mail', 'use_tls')
app.config['MAIL_USERNAME'] = config.get('mail', 'username')
app.config['MAIL_PASSWORD'] = config.get('mail', 'passwd')
mail = Mail(app)

# test and initialize database
preenv.initDB(app.logger)
# 初始化全局变量
gv.init_global(app.logger, mail, config)


# views------------------------------------------------


@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
def index():
    resp = redirect('/login')
    return resp


@app.route('/contact', methods=['GET', 'POST'])
def contact():
    _un, _role = loggeduser(request)
    _infopg =  _role.lower() + 'info'
    return render_template('about.html', loggeduser=_un,infopg=_infopg)

@app.route('/about', methods=['GET', 'POST'])
def about():
    _un, _role = loggeduser(request)
    _infopg =  _role.lower() + 'info'
    return render_template('about.html', loggeduser=_un,infopg=_infopg)

# 国际化文件
@app.route('/static/i18n_serv/<path:subpath>', methods=['GET'])
def i18n_serv(subpath):
    if subpath is None:
        abort(404)
    sps = subpath.split('/')
    lang = sps[0]
    bfn = sps[-1]
    if MODE_DEBUG:
        gv.load_i18n(app.logger)
    if lang in gv.i18n:
        if bfn in gv.i18n[lang]:
            return gv.i18n[lang][bfn]
    return ''


# 错误处理
@app.route('/error')
@app.errorhandler(400)
@app.errorhandler(401)
@app.errorhandler(404)
@app.errorhandler(500)
def error(e):
    app.logger.debug("error occurred: %s" % e)
    _un, _role = loggeduser(request)
    try:
        return render_template('error.html', code=int(e.code), loggeduser=_un)
    except Exception as e:
        app.debug('exception is %s' % e)
    finally:
        return render_template('error.html', code=int(e.code), loggeduser=_un)


# 注册蓝图-------------------------------------------------
app.register_blueprint(api_loginout)
app.register_blueprint(api_user)
app.register_blueprint(api_children)
app.register_blueprint(api_status)
app.register_blueprint(api_selector)
app.register_blueprint(api_files)
app.register_blueprint(pg_loginout)
app.register_blueprint(pg_index)
app.register_blueprint(pg_child)
app.register_blueprint(pg_user)
app.register_blueprint(pg_status)

if __name__ == '__main__':
  #  serverhost = gv.config.get("web", "host")
 #   listenport = gv.config.getint("web", "port")
#    app.logger.info("Start server in "+serverhost+":"+str(listenport))
    # app.config["EXPLAIN_TEMPLATE_LOADING"] = True   # 打印模板路径
    app.run(
        host='0.0.0.0',
 #       port=listenport,
        debug=MODE_DEBUG
    )
    ssl_context=('/etc/ssl/certs/cert.pem', '/etc/ssl/private/key.pem')
    #ssl_context='adhoc' #adhoc ssl Testing
