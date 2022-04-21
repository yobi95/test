#!/usr/bin/env python3
# -*- coding:utf-8 -*-
"""
用户蓝图
定义蓝图pg_user，实现用户page相关蓝图
"""
from urllib import parse

from flask import Blueprint, redirect, render_template, request, abort

import funcs
import global_var as gv
from api_loginout import loggeduser
from api_user import users_parent_post

# 定义蓝图-------------------------------------------------
pg_user = Blueprint(
    'pg_user',
    __name__,
    template_folder='templates'
)

# views------------------------------------------------

@pg_user.route('/userinfo', methods=['GET'])
def userinfo_get():
    _un, _role = loggeduser(request)
    if _un is None:
        return redirect('/login')
    _sk = request.cookies.get("secret_key", type=str)
    _uid = gv.logged[_sk]['id']
    _role = gv.logged[_sk]['role'].lower() + 'info'
    return render_template('infopage.html', loggeduser=_un,
                           uid=_uid, role=_role)


@pg_user.route('/addparent', methods=['GET'])
def addparent_get():
    _un, _role = loggeduser(request)
    if _un is None:
        return redirect('/login')
    if _role == 'parent':
        return '<h1>No authority!</h1><p>Parent can not add parent account, login as admin or staff please.</p>'
    return render_template('addparent.html', loggeduser=_un)

@pg_user.route('/parentlist', methods=['GET'])
def parentlist_get():
    _un, _role = loggeduser(request)
    if _un is None:
        return redirect('/login')
    if _role == 'parent':
        return '<h1>No authority!</h1><p>Login as admin or staff please.</p>'
    return render_template('parentlist.html', loggeduser=_un)

@pg_user.route('/alterparent', methods=['GET'])
def alterparent_get():
    _un, _role = loggeduser(request)
    if _un is None:
        return redirect('/login')
    if _role == 'parent':
        return '<h1>No authority!</h1><p>Login as admin or staff please.</p>'
    _id = request.args.get('id')
    return render_template('alterparent.html', loggeduser=_un, id=_id)

@pg_user.route('/addstaff', methods=['GET'])
def addstaff_get():
    _un, _role = loggeduser(request)
    if _un is None:
        return redirect('/login')
    if _role == 'parent' or _role=='staff':
        return '<h1>No authority!</h1><p>Parent can not add parent account, login as admin please.</p>'
    return render_template('addstaff.html', loggeduser=_un)

@pg_user.route('/stafflist', methods=['GET'])
def stafflist_get():
    _un, _role = loggeduser(request)
    if _un is None:
        return redirect('/login')
    if _role == 'parent':
        return '<h1>No authority!</h1><p>Login as admin please.</p>'
    return render_template('stafflist.html', loggeduser=_un)

@pg_user.route('/alterstaff', methods=['GET'])
def alterstaff_get():
    _un, _role = loggeduser(request)
    if _un is None:
        return redirect('/login')
    if _role == 'parent' or _role=='staff':
        return '<h1>No authority!</h1><p>Login as admin please.</p>'
    _id = request.args.get('id')
    return render_template('alterstaff.html', loggeduser=_un, id=_id)

    
@pg_user.route('/resetpw', methods=['GET'])
def resetpw_get():
    _un, _role = loggeduser(request)
    return render_template('resetpw.html', loggeduser=_un)