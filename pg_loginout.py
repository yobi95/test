#!/usr/bin/env python3
# -*- coding:utf-8 -*-
"""
登入登出蓝图
定义蓝图loginout，实现登录登出蓝图
"""
from urllib import parse

from flask import Blueprint, redirect, render_template, request

import funcs
import global_var as gv
from api_loginout import loggeduser, login, logout, get_secret

# 定义蓝图-------------------------------------------------
pg_loginout = Blueprint(
    'pg_loginout',
    __name__,
    template_folder='templates'
)

# views------------------------------------------------


@pg_loginout.route('/login', methods=['GET', 'POST'])
def login_page():
    # get next_url
    next_url = request.form.get('next_url')
    if next_url is None:
        next_url = request.args.get('next_url')
    nu2 = "/"
    if next_url is not None:
        nu2 = parse.unquote(next_url)
    # login
    if request.method == 'POST':
        _sk = request.form.get('secret_key', type=str)
        _loginres = login()
        if _loginres['code'] == 0:
            # login successfully
            # check role and redirect
            _role = gv.logged[_sk]['role']
            if _role == 'admin' or _role=='staff':
                nu2 = 'admin'
            else:
                nu2 = 'parent'
            resp = redirect(nu2 or "/")
            # set cookies
            resp.set_cookie('username', gv.logged[_sk]['un'].encode(
                "utf-8", "ignore"), max_age=259200)
            resp.set_cookie('secret_key', _sk.encode(
                "utf-8", "ignore"), max_age=259200)
            resp.set_cookie('token', gv.logged[_sk]['token'].encode(
                "utf-8", "ignore"), max_age=259200)
            gv.logged[_sk]['send'] = True
            return resp
        elif _loginres['code'] == 30:
            if _sk in gv.secrets:
                del gv.secrets[_sk]
            # already logged
            return redirect(nu2 or "/")
        else:
            # login failed
            if _sk in gv.secrets:
                del gv.secrets[_sk]
            _sec = get_secret()
            return render_template(
                "login.html",
                next_url=next_url,
                secret=_sec['data'][0],
                errormsg=_loginres["msg"])
    # GET
    _un, _role = loggeduser(request)
    if _un is not None:
        if _role in ['admin', 'staff']:
            resp = redirect('admin')
            return resp
        if _role=='parent':
            resp = redirect('parent')
            return resp
        return redirect('about')
    _sec = get_secret()
    return render_template('login.html', next_url=next_url, secret=_sec['data'][0])


@pg_loginout.route('/logout', methods=['GET'])
def logoutpage():
    _un, _role = loggeduser(request)
    if _un is not None:
        _sk = request.cookies.get("secret_key", type=str)
        del gv.logged[_sk]
    return redirect("/")
