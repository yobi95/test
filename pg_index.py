#!/usr/bin/env python3
# -*- coding:utf-8 -*-
"""
首页蓝图
定义蓝图pg_index，实现首页蓝图，处理已登录用户的首页
"""
from urllib import parse

from flask import Blueprint, redirect, render_template, request, send_from_directory

import funcs
import global_var as gv
from global_var import enum_error as ee
from api_loginout import loggeduser
from api_children import get_child_status_by_pid

import traceback 

# 定义蓝图-------------------------------------------------
pg_index = Blueprint(
    'pg_index',
    __name__,
    template_folder='templates'
)


# functions--------------------------------------------


# views------------------------------------------------

@pg_index.route('/admin', methods=['GET'])
def pg_admin_get():
    # get username, role, check role
    _sk = request.cookies.get("secret_key", type=str)
    _un, _role = loggeduser(request)
    if _un is None:
        resp = redirect('/login')
        return resp
    if _role!='admin' and _role!='staff':
        resp = redirect('/login')
        return resp 
    _s = None
    if 'send' in gv.logged[_sk] and gv.logged[_sk]['send']:
        del gv.logged[_sk]['send']
        _s = gv.logged[_sk]['secret']
    return render_template('index_admin.html', loggeduser=_un, role=_role, secret=_s)


@pg_index.route('/parent', methods=['GET'])
def pg_parent_get():
    # # get secret_key
    # get username, role, check role
    _un, _role = loggeduser(request)
    if _un is None:
        resp = redirect('/login')
        return resp

    # if role is incorrect, redirect
    if _role == 'admin' or _role == 'staff':
        resp = redirect('/admin')
        return resp

    # get child info
    _sk = request.cookies.get("secret_key", type=str)
    if _sk is None or _sk not in gv.logged:
        resp = redirect('/login')
        return resp
    pid = gv.logged[_sk]['id']
    _status = get_child_status_by_pid(pid, _sk)

    _s = None
    if 'send' in gv.logged[_sk] and gv.logged[_sk]['send']:
        del gv.logged[_sk]['send']
        _s = gv.logged[_sk]['secret']
    # return page
    return render_template('index_parent.html', status=_status, loggeduser=_un, secret=_s)

@pg_index.route('/uploads/<path:filename>')
def download_file(filename):
    photo_path = gv.config.get("photo", "path")
    return send_from_directory(photo_path, filename, as_attachment=True)


@pg_index.route('/childlist_parent', methods=['GET'])
def filelist_get():
    _un, _role = loggeduser(request)
    return render_template('childlist_parent.html', loggeduser=_un)

#one day status data grouped by type  
@pg_index.route('/group_parent', methods=['GET'])
def pg_parent_group_get():
    # # get secret_key
    # get username, role, check role
    _un, _role = loggeduser(request)
    if _un is None:
        resp = redirect('/login')
        return resp

    # if role is incorrect, redirect
    if _role == 'admin' or _role == 'staff':
        resp = redirect('/admin')
        return resp

    # get child info
    _sk = request.cookies.get("secret_key", type=str)
    if _sk is None or _sk not in gv.logged:
        resp = redirect('/login')
        return resp
    pid = gv.logged[_sk]['id']
    _status = get_child_status_by_pid(pid, _sk)

    _s = None
    if 'send' in gv.logged[_sk] and gv.logged[_sk]['send']:
        del gv.logged[_sk]['send']
        _s = gv.logged[_sk]['secret']
    # return page
    return render_template('index_parent_gp.html', status=_status, loggeduser=_un, secret=_s)