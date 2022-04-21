#!/usr/bin/env python3
# -*- coding:utf-8 -*-
"""
登入登出API蓝图
定义蓝图api_loginout，实现登录登出蓝图
"""
from urllib import parse
import time
import traceback
import os
import base64

from flask import Blueprint, redirect, render_template, request, Response

import funcs
import global_var as gv
from global_var import enum_error as ee


# 定义蓝图-------------------------------------------------
api_loginout = Blueprint(
    'api_loginout',
    __name__,
    template_folder='templates'
)


# functions--------------------------------------------


def loggeduser(req):
    """
    从cookies里获得已登录用户
    仅使用token验证，用于登录状态保持，不得用于权限校验
    验证是否已登录时可以使用
    若当前会话用户已登录，返回:用户名,角色
    若当前会话无用户登录，返回:None
    """
    _sk = req.cookies.get("secret_key", type=str)
    _un = req.cookies.get("username")
    if _sk in gv.logged:
        if gv.logged[_sk]['timeout']<int(time.time()):
            del gv.logged[_sk]
            return None,None
        if gv.logged[_sk]['token'] == req.cookies.get("token") \
                and gv.logged[_sk]['un'] == _un:
            return gv.logged[_sk]['un'], gv.logged[_sk]['role']
    return None, None


def verify_auto(req, allows=None):
    """
    verify id and sign
    call verify_form or verify_args according to req.method
    :param allows:      允许的role列表，用户在列表内才会通过，否则
                        返回错误码，默认None时不检查
    :return :   a dict like {'code':0,'msg':'secretkey'}
                code=0 if pass, error code others.
                msg is error message, but if verification
                pass, msg is the secretkey of user
    """
    if req.method == 'GET':
        return verify_args(req, allows=allows)
    return verify_form(req, allows=allows)


def verify(secret_key, prefixstr, signstr, allows=None):
    """
    验证身份和签名
    :param secret_key:  secret key
    :param prefixstr:   prefix string of sign
    :param signstr:     sign string
    :param allows:      允许的role列表，用户在列表内才会通过，否则
                        返回错误码，默认None时不检查
    :return :           a dict like {'code':0,'msg':'secretkey'}
                        code=0 if pass, error code others.
                        msg is error message, but if verification
                        pass, msg is the secretkey of user
    """
    if secret_key in gv.logged:
        _secret = gv.logged[secret_key]['secret']
        if gv.logged[secret_key]['timeout']<int(time.time()):
            del gv.logged[secret_key]
            return ee.TIMEOUT()
    else:
        return {'code': 21, 'msg': 'Not logged in'}
    tpwmd5 = funcs.get_md5(prefixstr + _secret)
    if tpwmd5 == signstr:
        if allows is not None:
            if gv.logged[secret_key]['role'] not in allows:
                return {'code': 30, 'msg': 'no authority'}
        return {'code': 0, 'msg': secret_key}
    else:
        return {'code': 24, 'msg': 'sign verification failed'}


def verify_form(req, allows=None):
    """
    verify id and sign
    for form data
    :param allows:      允许的role列表，用户在列表内才会通过，否则
                        返回错误码，默认None时不检查
    :return :   a dict like {'code':0,'msg':'secretkey'}
                code=0 if pass, error code others.
                msg is error message, but if verification
                pass, msg is the secretkey of user
    """
    # get parameters
    _sk = req.form.get('secret_key')
    _keys = req.form.get('keys')
    _sign = req.form.get('sign')
    if str(_sk) not in gv.logged:
        return {'code': 21, 'msg': 'not logged in'}
    paramerror = {'code': 40, 'msg': 'verification failed: param error'}
    if _sk is None or _keys is None or _sign is None:
        return paramerror
    _keys = _keys.split(',')
    _pres = []
    _allkeys = req.form.to_dict().keys()
    for _k in _allkeys:
        if _k not in _keys:
            if _k not in ['keys', 'sign']:
                return paramerror
    for _key in _keys:
        _val = req.form.get(_key)
        if _val is None:
            return paramerror
        _pres.append(_key + "=" + str(_val))
    _prefixstr = '&'.join(_pres)
    return verify(_sk, _prefixstr, _sign, allows=allows)


def verify_args(req, allows=None):
    """
    verify id and sign
    for args data
    :param allows:      允许的role列表，用户在列表内才会通过，否则
                        返回错误码，默认None时不检查
    :return :   a dict like {'code':0,'msg':'secretkey'}
                code=0 if pass, error code others.
                msg is error message, but if verification
                pass, msg is the secretkey of user
    """
    # get parameters
    _sk = req.args.get('secret_key')
    _keys = req.args.get('keys')
    _sign = req.args.get('sign')
    if str(_sk) not in gv.logged:
        return {'code': 21, 'msg': 'not logged in'}
    paramerror = {'code': 40, 'msg': 'param error'}
    if _sk is None or _keys is None or _sign is None:
        return paramerror
    _keys = _keys.split(',')
    _pres = []
    _allkeys = req.args.to_dict().keys()
    for _k in _allkeys:
        if _k not in _keys:
            if _k not in ['keys', 'sign']:
                return paramerror
    for _key in _keys:
        _val = req.args.get(_key)
        if _val is None:
            return paramerror
        _pres.append(_key + "=" + str(_val))
    _prefixstr = '&'.join(_pres)
    return verify(_sk, _prefixstr, _sign, allows=allows)


def _checkLogin(username, password, secret_key, parent_allow):
    """
    验证登录信息
    :param username: 用户提交的用户名
    :param password: 用户提交的加密後密码
    :param secret_key: 登录页面的secret_key
    :return : unity formated dict
    """
    if secret_key not in gv.secrets:
        return {"code": 51, "msg": "secret key not exists", 'count': 0, 'data': []}
    if gv.secrets[secret_key]['timeout'] < time.time():
        del gv.secrets[secret_key]
        return {"code": 22, "msg": "secret timeout", 'count': 0, 'data': []}
    
    _secret = gv.secrets[secret_key]['secret']
    sqlstr = "select id,passwdmd5,`role`,`parent_allow` from user where `username`='{un}';".format(
        un=base64.b64encode(username.encode('utf8')).decode())
    conn = gv.dbpool.connection()
    cur = conn.cursor()
    cur.execute("SET NAMES UTF8;")
    cur.execute(sqlstr.encode("utf-8", "ignore"))
    pwres = cur.fetchall()
    cur.close()
    conn.close()
    if len(pwres) == 0:
        return {"code": 51, "msg": "username not exists", 'count': 0, 'data': []}
    tpwmd5 = pwres[0][1]
    tpwmd5 = funcs.get_md5(tpwmd5 + _secret)
    parent_allow == pwres[0][3]
    print(pwres[0][3])
    '''
     sqlstr = "select id,passwdmd5,`role` from user where `username`='{un}';".format(
        un=base64.b64encode(username.encode('utf8')).decode()
    '''
    if pwres[0][3] == 'No':#for chacking parent account is not disable
        return {"code": 23, "msg": 'account is disable'}
    if password == tpwmd5:
        return {"code": 0, "msg": '', 'count': 1,
                'data': [{'id': pwres[0][0], 'role':pwres[0][2]}]}
    return {"code": 23, "msg": "password incorrect"}
    
# views------------------------------------------------
@api_loginout.route('/api/getSecret', methods=['GET'])
def get_secret():
    """
    Interface getSecret
    :return : secret key and secret
    """
    _un, _role = loggeduser(request)
    if _un is not None:
        return {'code': 30, 'msg': 'Already logged in', 'count': 0, 'data': []}
    secret = base64.b64encode(os.urandom(24)).decode()
    # save into server, timeout is 30min
    sk = base64.b64encode(os.urandom(12)).decode()
    gv.secrets[sk] = {
        'secret': secret,
        'timeout': int(time.time())+1800
    }
    resdict = {
        "code": 0,
        "msg": "",
        "count": 1,
        "data": [{'secret_key': sk, 'secret': secret}]
    }
    return resdict


@api_loginout.route('/api/login', methods=['POST'])
def login():
    try:
        _un, _role = loggeduser(request)
        if _un is not None:
            return {'code': 30, 'msg': 'Already logged in', 'count': 0, 'data': []}
        username = request.form.get('username')
        passwd_md5 = request.form.get('passwd_md5')
        secret_key = request.form.get('secret_key', type=str)
        parent_allow = request.form.get('parent_allow')
        chk = _checkLogin(username, passwd_md5, secret_key, parent_allow)
        if chk["code"] == 0:
            # 验证通过
            _role = chk['data'][0]['role']
            _id = chk['data'][0]['id']
            _token = base64.b64encode(os.urandom(24)).decode()
            _secret = base64.b64encode(os.urandom(24)).decode()
            # set logged
            gv.logged[secret_key] = {
                'id': _id,
                'un': username,
                'token': _token,
                'secret': _secret,
                'role': _role,
                'timeout': int(time.time())+86400*gv.logintimeout
            }
            # delete secret
            if secret_key in gv.secrets:
                del gv.secrets[secret_key]
            # build response
            respdict = {
                "code": 0,
                "msg": "",
                "count": 1,
                "data": [{'secret_key': secret_key, 'token': _token, 'secret': _secret}]
            }
            return respdict
        else:
            return chk
    except:
        emsg = traceback.format_exc()
        gv.logger.error("Error in login \n" + emsg)
        respdict = {
            "code": 20,
            "msg": 'Unknown error occured',
            "count": 0,
            "data": []
        }
        return respdict


@api_loginout.route('/api/logout', methods=['POST'])
def logout():
    vres = verify_form(request)
    if not vres['code'] == 0:
        # verification faild
        respdict = {
            "code": vres['code'],
            "msg": vres['msg'],
            "count": 0,
            "data": []
        }
        return respdict
    del gv.logged[vres['msg']]
    respdict = {
        "code": 0,
        "msg": '',
        "count": 0,
        "data": []
    }
    return respdict
