#!/usr/bin/env python3
# -*- coding:utf-8 -*-
"""
用户API蓝图
定义蓝图api_user，实现用户蓝图
视图含义见对应api文档
"""
import traceback

from flask import Blueprint, request, render_template, current_app
from threading import Thread

import funcs
import global_var as gv
from api_loginout import verify_auto
from global_var import enum_error as ee
from flask_mail import Message
import random
import time

# 定义蓝图-------------------------------------------------
api_user = Blueprint(
    'api_user',
    __name__,
    template_folder='templates'
)


# functions--------------------------------------------


def check_username(un):
    """
    检查用户名是否存在
    :param un:  username
    :return :   Ture=exists or False=not
    """
    try:
        sqlstr = "select id from user where `username`='{un}';".format(
            un=funcs.b64encode(un))
        conn = gv.dbpool.connection()
        cur = conn.cursor()
        cur.execute("SET NAMES UTF8;")
        cur.execute(sqlstr.encode("utf-8", "ignore"))
        pwres = cur.fetchall()
        cur.close()
        conn.close()
        if pwres is None or len(pwres) == 0:
            return False
        return True
    except:
        gv.logger.error(traceback.format_exc())
        res = ee.DBERR()
        return res


def get_id_by_username(un):
    """
    通过用户名得到id和role
    :param un:  username
    :return :   unity formated dict,data:{'id':id,'role':role,'email':email}
    """
    try:
        sqlstr = "select id,email,`role`,parent_allow from user where `username`='{un}';".format(
            un=funcs.b64encode(un))
        conn = gv.dbpool.connection()
        cur = conn.cursor()
        cur.execute("SET NAMES UTF8;")
        cur.execute(sqlstr.encode("utf-8", "ignore"))
        pwres = cur.fetchall()
        cur.close()
        conn.close()
        if pwres is None or len(pwres) == 0:
            return ee.NORMAL()
        resu = ee.NORMAL()
        resu['count'] = len(pwres)
        resu['data'].append({
            'id': pwres[0][0],
            'email': funcs.b64decode(pwres[0][1]),
            'role': pwres[0][2],
            'parent_allow': funcs.b64decode(pwres[0][3])})
        return resu
    except:
        gv.logger.error(traceback.format_exc())
        res = ee.DBERR()
        return res


def get_parents(page, limit, simple=False):
    '''
    get parents from database
    :param page: page, 0 based
    :param limit: count per page, 0 = no limit
    :param simple:  simple mode
    :return : Unified format json
    '''
    flist_t = [
        {'fn': "t1`.`id", 'type': 'str'},
        {'fn': "username", 'type': 'b64str'},
        {'fn': "name", 'type': 'b64str'},
        {'fn': "name_chi", 'type': 'b64str'},
        {'fn': "child_ids", 'type': 'str'},
        {'fn': "edu", 'type': 'b64str'},
        {'fn': "occupation", 'type': 'b64str'},
        {'fn': "tel", 'type': 'str'},
        {'fn': "occupation", 'type': 'b64str'},
    ]
    flist_p = [
        {'fn': "id", 'type': 'int'},
        {'fn': "name", 'type': 'b64str'},
        {'fn': "name_chi", 'type': 'b64str'},
        {'fn': "child_ids", 'type': 'str'},
        {'fn': "edu", 'type': 'b64str'},
        {'fn': "occupation", 'type': 'b64str'},
        {'fn': "tel", 'type': 'str'}
    ]
    limitstr = ''
    if page < 0:
        page = 0
    if limit > 0:
        limitstr = ' limit {0},{1}'.format(str(page*limit), str(limit))
    if simple:
        flist_t = flist_t[:4]
        flist_p = flist_p[:3]
    kstr_p = funcs.build_field_str(flist_p)
    wstr = 'inner join (select {kstr} from parent {limit}) as t1'\
        ' on `user`.id=t1.id'.format(kstr=kstr_p, limit=limitstr)
    try:
        conn = gv.dbpool.connection()
        cur = conn.cursor()
        res = funcs.get_datas(cur, 'user', flist_t,
                              wstr=wstr, logger=gv.logger)
        cur.close()
        conn.close()
        if res['code'] == 0 and len(res['data']) > 0:
            # 更改id字段名
            for line in res['data']:
                line['id'] = line['t1`.`id']
                del line['t1`.`id']
        return res
    except:
        gv.logger.error(traceback.format_exc())
        res = ee.DBERR()
        return res


def delete_user(un):
    '''
    delete user in db
    :param un: username
    '''
    try:
        sqlstr = "delete from `user` where `username`='{0}';".format(
            funcs.b64encode(un))
        conn = gv.dbpool.connection()
        cur = conn.cursor()
        cur.execute("SET NAMES UTF8;")
        cur.execute(sqlstr.encode("utf-8", "ignore"))
        conn.commit()
        cur.close()
        conn.close()
        return None
    except:
        gv.logger.error(traceback.format_exc())
        return None


def get_parent(id):
    '''
    get parents from database
    :param id: id
    :return : Unified format json
    '''
    tmpstr1 = '`name`,name_chi,child_ids,relations,edu,occupation,tel,reason'
    sqlstr1 = 'select t1.id,`username`,email,' + tmpstr1 + ' from `user`'\
        ' inner join (select id,' + tmpstr1 + ' from parent {wstr}) as t1'\
        ' on `user`.id=t1.id;'
    if type(id) != type(1):
        if type(id) != type(''):
            return ee.PARAMERR(app=': id')
        if not str.isdigit(id):
            return ee.PARAMERR(app=': id')
    wstr = ' where id={0}'.format(str(id))

    try:
        conn = gv.dbpool.connection()
        cur = conn.cursor()
        cur.execute("SET NAMES UTF8;")
        cur.execute(sqlstr1.format(wstr=wstr).encode("utf-8", "ignore"))
        res = cur.fetchall()
        resdata = []
        if res is None:
            cur.close()
            conn.close()
            return ee.DBERR()
        for line in res:
            if len(line) != 11:
                continue
            ld = {
                'id': str(line[0]),
                'username': funcs.b64decode(line[1]),
                'email': funcs.b64decode(line[2]),
                'name': funcs.b64decode(line[3]),
                'name_chi': funcs.b64decode(line[4]),
                'child_ids': line[5] if line[5] is not None else "",
                'relations': funcs.b64decode(line[6]),
                'edu': funcs.b64decode(line[7]),
                'occupation': funcs.b64decode(line[8]),
                'tel': line[9] if line[9] is not None else "",
                'reason': funcs.b64decode(line[10])
                
            }
            resdata.append(ld)
        count = len(resdata)
        cur.close()
        conn.close()
        res = {'code': 0, 'msg': '', 'count': count, 'data': resdata}
        return res
    except:
        gv.logger.error(traceback.format_exc())
        res = ee.DBERR()
        return res


def get_staffs(page, limit):
    '''
    get staffs from database
    :param page: page, 0 based
    :param limit: count per page, 0 = no limit
    :return : Unified format json
    '''
    tmpstr1 = '`name`,name_chi,gender,group_id'
    sqlstr1 = 'select t1.id,`username`,' + tmpstr1 + ' from `user`'\
        ' inner join (select id,' + tmpstr1 + ' from staff {limit}) as t1'\
        ' on `user`.id=t1.id;'
    sqlstr2 = "select count(1) from parent;"
    limitstr = ''
    if page < 0:
        page = 0
    if limit > 0:
        limitstr = ' limit {0},{1}'.format(str(page*limit), str(limit))

    try:
        conn = gv.dbpool.connection()
        cur = conn.cursor()
        cur.execute("SET NAMES UTF8;")
        cur.execute(sqlstr1.format(limit=limitstr).encode("utf-8", "ignore"))
        res = cur.fetchall()
        resdata = []
        if res is None:
            cur.close()
            conn.close()
            return ee.DBERR()
        for line in res:
            if len(line) != 6:
                continue
            ld = {
                'id': str(line[0]),
                'username': funcs.b64decode(line[1]),
                'name': funcs.b64decode(line[2]),
                'name_chi': funcs.b64decode(line[3]),
                'gender': line[4] if line[4] is not None else "",
                'group_id': line[5] if line[5] is not None else ""
            }
            resdata.append(ld)
        cur.execute(sqlstr2.encode("utf-8", "ignore"))
        res = cur.fetchall()
        if res is None:
            cur.close()
            conn.close()
            return ee.DBERR()
        count = int(res[0][0])
        cur.close()
        conn.close()
        res = {'code': 0, 'msg': '', 'count': count, 'data': resdata}
        return res
    except:
        gv.logger.error(traceback.format_exc())
        res = ee.DBERR()
        return res

def get_userinfo(id, getpw=False):
    '''
    get user info from db
    :param getpw: True=return passwdmd5
    '''
    flist = [
        {'fn':'id',"type":'str'},
        {'fn':'username','type':'b64str'},
        {'fn':'email','type':'b64str'},
        {'fn':'role','type':'str'},
        {'fn':'parent_allow','type':'b64str'}
    ]
    if getpw:
        flist.append({'fn':'passwdmd5','type':'str'})
    wstr = 'where id={0}'.format(str(id))
    try:
        conn = gv.dbpool.connection()
        cur = conn.cursor()
        cur.execute("SET NAMES UTF8;")
        data = funcs.get_datas(cur, 'user', flist, wstr=wstr, logger=gv.logger)
        return data
    except:
        gv.logger.error(traceback.format_exc())
        res = ee.DBERR()
        return res


def get_staff(id):
    '''
    get staff from database
    :param id: id
    :return : Unified format json
    '''
    tmpstr1 = '`name`,name_chi,gender,group_id'
    sqlstr1 = 'select t1.id,`username`,email,' + tmpstr1 + ' from `user`'\
        ' inner join (select id,' + tmpstr1 + ' from staff {wstr}) as t1'\
        ' on `user`.id=t1.id;'
    if type(id) != type(1):
        if type(id) != type(''):
            return {'code': 40, 'msg': 'invalid id', 'count': 0, 'data': []}
        if not str.isdigit(id):
            return {'code': 40, 'msg': 'invalid id', 'count': 0, 'data': []}
    wstr = ' where id={0}'.format(str(id))

    try:
        conn = gv.dbpool.connection()
        cur = conn.cursor()
        cur.execute("SET NAMES UTF8;")
        cur.execute(sqlstr1.format(wstr=wstr).encode("utf-8", "ignore"))
        res = cur.fetchall()
        resdata = []
        if res is None:
            cur.close()
            conn.close()
            return {'code': 10, 'msg': 'database error', 'count': 0, 'data': []}
        for line in res:
            if len(line) != 7:
                continue
            ld = {
                'id': str(line[0]),
                'username': funcs.b64decode(line[1]),
                'email': funcs.b64decode(line[2]),
                'name': funcs.b64decode(line[3]),
                'name_chi': funcs.b64decode(line[4]),
                'gender': line[5] if line[5] is not None else "",
                'group_id': line[6] if line[6] is not None else ""
            }
            resdata.append(ld)
        count = len(resdata)
        cur.close()
        conn.close()
        res = {'code': 0, 'msg': '', 'count': count, 'data': resdata}
        return res
    except:
        gv.logger.error(traceback.format_exc())
        res = {'code': 10, 'msg': 'database error', 'count': 0, 'data': []}
        return res


def delete_user_by_id(role):
    chksql = "select 1 from `user` where id={0} and `role`='{1}';"
    sqlstr = 'delete from `{0}` where id={1};'
    id = request.form.get('id')
    if id is None or (type(id) == type('') and not str.isdigit(id)):
        return {'code': 40, 'msg': 'id is needed', 'count': 0, 'data': []}
    try:
        conn = gv.dbpool.connection()
        cur = conn.cursor()
        cur.execute("SET NAMES UTF8;")
        cur.execute(chksql.format(str(id), role).encode("utf-8", "ignore"))
        res = cur.fetchall()
        if res is None or len(res) == 0:
            cur.close()
            conn.close()
            return {'code': 40, 'msg': 'parameters error', 'count': 0, 'data': []}
        cur.execute(sqlstr.format('user', str(id)).encode("utf-8", "ignore"))
        cur.execute(sqlstr.format(role, str(id)).encode("utf-8", "ignore"))
        conn.commit()
        cur.close()
        conn.close()
        return {'code': 0, 'msg': '', 'count': 0, 'data': []}
    except:
        gv.logger.error(traceback.format_exc())
        return {'code': 10, 'msg': 'database error', 'count': 0, 'data': []}


def insert_parent():
    # field define list
    uid = funcs.get_random_int64()
    fs_p = [
        {'fn': 'id', 'type': 'int', 'val': uid},
        {'fn': 'name', 'type': 'b64str', 'val': request.form.get('name')},
        {'fn': 'name_chi', 'type': 'b64str',
            'val': request.form.get('name_chi')},
        {'fn': 'relations', 'type': 'b64str',
            'val': request.form.get('relations')},
        {'fn': 'edu', 'type': 'b64str', 'val': request.form.get('edu')},
        {'fn': 'occupation', 'type': 'b64str',
            'val': request.form.get('occupation')},
        {'fn': 'tel', 'type': 'str', 'val': request.form.get('tel')},
        {'fn': 'reason', 'type': 'b64str', 'val': request.form.get('reason')}
    ]
    fs_u = [
        {'fn': 'id', 'type': 'int', 'val': uid},
        {'fn': 'username', 'type': 'b64str',
            'val': request.form.get('username')},
        {'fn': 'passwdmd5', 'type': 'str',
            'val': request.form.get('passwd_md5')},
        {'fn': 'email', 'type': 'b64str', 'val': request.form.get('email')},
        {'fn': 'role', 'type': 'str', 'val': 'parent'},
        {'fn': 'parent_allow', 'type': 'b64str', 'val': request.form.get('parent_allow')}
    ]

    # check params
    if fs_u[1]['val'] is None or len(fs_u[1]['val']) < 1:
        return {'code': 40, 'msg': 'username is needed', 'count': 0, 'data': []}
    if fs_u[2]['val'] is None or len(fs_u[2]['val']) < 1:
        return {'code': 40, 'msg': 'passwd_md5 is needed', 'count': 0, 'data': []}
    if check_username(fs_u[1]['val']):
        return {'code': 50, 'msg': 'username already exists', 'count': 0, 'data': []}

    # build sql string
    kstr_u = funcs.build_field_str(fs_u)
    vstr_u = funcs.build_values_str(fs_u)
    if vstr_u is None:
        return {'code': 40, 'msg': 'parameters error', 'count': 0, 'data': []}
    kstr_p = funcs.build_field_str(fs_p)
    vstr_p = funcs.build_values_str(fs_p)
    if vstr_p is None:
        return {'code': 40, 'msg': 'parameters error', 'count': 0, 'data': []}

    tbn_p = 'parent'
    tbn_u = 'user'
    sqlstr = "insert into `{tbn}`({0}) select {1} from dual where not exists (select 1 from `{tbn}` where `username`='{2}');"
    sqlstr_p = "insert into `{tbn}`({0}) select {1} from dual where not exists (select 1 from `{tbn}` where `id`={2});"
    try:
        conn = gv.dbpool.connection()
        cur = conn.cursor()
        cur.execute("SET NAMES UTF8;")
        sqlstr1 = sqlstr.format(
            kstr_u, vstr_u, funcs.b64encode(fs_u[1]['val']),
            tbn=tbn_u
        )
        cur.execute(sqlstr1.encode("utf-8", "ignore"))
        sqlstr1 = sqlstr_p.format(
            kstr_p, vstr_p, str(uid),
            tbn=tbn_p
        )
        cur.execute(sqlstr1.encode("utf-8", "ignore"))
        conn.commit()
        cur.close()
        conn.close()
    except:
        gv.logger.error(traceback.format_exc())
        res = {'code': 10, 'msg': 'database error', 'count': 0, 'data': []}
        return res
    return {'code': 0, 'msg': '', 'count': 0, 'data': []}

def get_child_ids(pid):
    '''
    get child ids of parent 
    '''
    fl = [{'fn':'child_ids','type':'str'}]
    try:
        conn = gv.dbpool.connection()
        cur = conn.cursor()
        cur.execute("SET NAMES UTF8;")
        wstr = 'where id={}'.format(str(pid))
        res = funcs.get_datas(cur, 'parent', fl, wstr=wstr, logger=gv.logger)
        cur.close()
        conn.close()
        ids = set()
        if len(res['data'])>0:
            for _line in res['data']:
                if _line['child_ids'] is not None and \
                    _line['child_ids']!='':
                    _lids = _line['child_ids'].split(',')
                    ids.update(_lids)
        resdata = []
        for id in ids:
            if id!='':
                resdata.append({'id':int(id)})
        res['count']=len(resdata)
        res['data']=resdata
        return res
    except:
        estr = traceback.format_exc()
        gv.logger.error('database error!\n'+estr)
        return ee.DBERR()
    return ee.UNKNOWN()

def update_parent():
    # field define list
    id = request.form.get('id')
    fs_p = [
        {'fn': 'name', 'type': 'b64str', 'val': request.form.get('name')},
        {'fn': 'name_chi', 'type': 'b64str',
            'val': request.form.get('name_chi')},
        {'fn': 'relations', 'type': 'b64str',
            'val': request.form.get('relations')},
        {'fn': 'edu', 'type': 'b64str', 'val': request.form.get('edu')},
        {'fn': 'occupation', 'type': 'b64str',
            'val': request.form.get('occupation')},
        {'fn': 'tel', 'type': 'str', 'val': request.form.get('tel')},
        {'fn': 'reason', 'type': 'b64str', 'val': request.form.get('reason')}
    ]
    fs_u = [
        {'fn': 'username', 'type': 'b64str',
            'val': request.form.get('username')},
        {'fn': 'email', 'type': 'b64str', 'val': request.form.get('email')},
        {'fn': 'parent_allow', 'type': 'b64str', 'val': request.form.get('parent_allow')}
    ]

    # check params
    if id is None or (type(id) == type('') and not str.isdigit(id)):
        return {'code': 40, 'msg': 'id is needed', 'count': 0, 'data': []}
    if fs_u[0]['val'] is not None:
        _uid = get_id_by_username(fs_u[0]['val'])
        if _uid['code'] == 0 \
                and _uid['count'] > 0 \
                and str(_uid['data'][0]['id']) != str(id):
            return {'code': 50, 'msg': 'username already exists', 'count': 0, 'data': []}
        elif _uid['code'] != 0:
            return _uid

    # build sql string
    vstr_u = funcs.build_set_str(fs_u, setNull=False)
    if vstr_u is None:
        return {'code': 40, 'msg': 'parameters error', 'count': 0, 'data': []}
    vstr_p = funcs.build_set_str(fs_p, setNull=False)
    if vstr_p is None:
        return {'code': 40, 'msg': 'parameters error', 'count': 0, 'data': []}

    tbn_p = 'parent'
    tbn_u = 'user'
    sqlstr = 'update `{tbn}` set {0} where id={1};'
    try:
        conn = gv.dbpool.connection()
        cur = conn.cursor()
        cur.execute("SET NAMES UTF8;")
        sqlstr1 = sqlstr.format(
            vstr_u, str(id),
            tbn=tbn_u
        )
        sqlstr2 = sqlstr.format(
            vstr_p, str(id),
            tbn=tbn_p
        )
        if vstr_u is not None and len(vstr_u) > 2:
            cur.execute(sqlstr1.encode("utf-8", "ignore"))
        if vstr_p is not None and len(vstr_p) > 2:
            cur.execute(sqlstr2.encode("utf-8", "ignore"))
        conn.commit()
        cur.close()
        conn.close()
        res = {'code': 0, 'msg': '', 'count': 0, 'data': []}
        return res
    except:
        gv.logger.error(traceback.format_exc())
        res = {'code': 10, 'msg': 'database error', 'count': 0, 'data': []}
        return res
    return {'code': 0, 'msg': '', 'count': 0, 'data': []}


def insert_staff():
    # field define list
    uid = funcs.get_random_int64()
    fs_p = [
        {'fn': 'id', 'type': 'int', 'val': uid},
        {'fn': 'name', 'type': 'b64str', 'val': request.form.get('name')},
        {'fn': 'name_chi', 'type': 'b64str',
            'val': request.form.get('name_chi')},
        {'fn': 'gender', 'type': 'str', 'val': request.form.get('gender')},
        {'fn': 'group_id', 'type': 'int', 'val': request.form.get('group_id')}
    ]
    fs_u = [
        {'fn': 'id', 'type': 'int', 'val': uid},
        {'fn': 'username', 'type': 'b64str',
            'val': request.form.get('username')},
        {'fn': 'passwdmd5', 'type': 'str',
            'val': request.form.get('passwd_md5')},
        {'fn': 'email', 'type': 'b64str', 'val': request.form.get('email')},
        {'fn': 'role', 'type': 'str', 'val': 'staff'}
    ]

    # check params
    if fs_u[1]['val'] is None or len(fs_u[1]['val']) < 1:
        return {'code': 40, 'msg': 'username is needed', 'count': 0, 'data': []}
    if fs_u[2]['val'] is None or len(fs_u[2]['val']) < 1:
        return {'code': 40, 'msg': 'passwd_md5 is needed', 'count': 0, 'data': []}
    if check_username(fs_u[1]['val']):
        return {'code': 50, 'msg': 'username already exists', 'count': 0, 'data': []}

    # build sql string
    kstr_u = funcs.build_field_str(fs_u)
    vstr_u = funcs.build_values_str(fs_u)
    if vstr_u is None:
        return {'code': 40, 'msg': 'parameters error', 'count': 0, 'data': []}

    kstr_p = funcs.build_field_str(fs_p)
    vstr_p = funcs.build_values_str(fs_p)
    if vstr_p is None:
        return {'code': 40, 'msg': 'parameters error', 'count': 0, 'data': []}

    tbn_p = 'staff'
    tbn_u = 'user'
    sqlstr = "insert into `{tbn}`({0}) select {1} from dual where not exists (select 1 from `{tbn}` where `username`='{2}');"
    sqlstr_p = "insert into `{tbn}`({0}) select {1} from dual where not exists (select 1 from `{tbn}` where `id`='{2}');"
    try:
        conn = gv.dbpool.connection()
        cur = conn.cursor()
        cur.execute("SET NAMES UTF8;")
        sqlstr1 = sqlstr.format(
            kstr_u, vstr_u, funcs.b64encode(fs_u[1]['val']),
            tbn=tbn_u
        )
        cur.execute(sqlstr1.encode("utf-8", "ignore"))
        sqlstr1 = sqlstr_p.format(
            kstr_p, vstr_p, str(uid),
            tbn=tbn_p
        )
        cur.execute(sqlstr1.encode("utf-8", "ignore"))
        conn.commit()
        cur.close()
        conn.close()
    except:
        gv.logger.error(traceback.format_exc())
        res = {'code': 10, 'msg': 'database error', 'count': 0, 'data': []}
        return res
    return {'code': 0, 'msg': '', 'count': 0, 'data': []}


def update_staff():
    # field define list
    id = request.form.get('id')
    fs_p = [
        {'fn': 'name', 'type': 'b64str', 'val': request.form.get('name')},
        {'fn': 'name_chi', 'type': 'b64str',
            'val': request.form.get('name_chi')},
        {'fn': 'gender', 'type': 'str', 'val': request.form.get('gender')},
        {'fn': 'group_id', 'type': 'int', 'val': request.form.get('group_id')}
    ]
    fs_u = [
        {'fn': 'username', 'type': 'b64str',
            'val': request.form.get('username')},
        {'fn': 'email', 'type': 'b64str', 'val': request.form.get('email')}
    ]

    # check params
    if id is None or (type(id) == type('') and not str.isdigit(id)):
        return {'code': 40, 'msg': 'id is needed', 'count': 0, 'data': []}
    if fs_u[0]['val'] is not None:
        _uid = get_id_by_username(fs_u[0]['val'])
        if _uid['code'] == 0 \
                and _uid['count'] > 0 \
                and str(_uid['data'][0]['id']) != str(id):
            return {'code': 50, 'msg': 'username already exists', 'count': 0, 'data': []}
        elif _uid['code'] != 0:
            return _uid

    # build sql string
    vstr_u = funcs.build_set_str(fs_u, setNull=False)
    if vstr_u is None:
        return {'code': 40, 'msg': 'parameters error', 'count': 0, 'data': []}
    vstr_p = funcs.build_set_str(fs_p, setNull=False)
    if vstr_p is None:
        return {'code': 40, 'msg': 'parameters error', 'count': 0, 'data': []}

    tbn_p = 'staff'
    tbn_u = 'user'
    sqlstr = 'update `{tbn}` set {0} where id={1};'
    try:
        conn = gv.dbpool.connection()
        cur = conn.cursor()
        cur.execute("SET NAMES UTF8;")
        sqlstr1 = sqlstr.format(
            vstr_u, str(id),
            tbn=tbn_u
        )
        sqlstr2 = sqlstr.format(
            vstr_p, str(id),
            tbn=tbn_p
        )
        if vstr_u is not None and len(vstr_u) > 2:
            cur.execute(sqlstr1.encode("utf-8", "ignore"))
        if vstr_p is not None and len(vstr_p) > 2:
            cur.execute(sqlstr2.encode("utf-8", "ignore"))
        conn.commit()
        cur.close()
        conn.close()
        res = {'code': 0, 'msg': '', 'count': 0, 'data': []}
        return res
    except:
        gv.logger.error(traceback.format_exc())
        res = {'code': 10, 'msg': 'database error', 'count': 0, 'data': []}
        return res
    return {'code': 0, 'msg': '', 'count': 0, 'data': []}


# views------------------------------------------------


@api_user.route('/api/checkUsername', methods=['GET'])
def chk_username():
    _un = request.args.get('username')
    if _un is None:
        return {'code': 40, 'msg': 'username is needed', 'count': 0, 'data': []}
    if check_username(_un):
        return {'code': 0, 'msg': '', 'count': 1, 'data': [{'exists': 1}]}
    else:
        return {'code': 0, 'msg': '', 'count': 1, 'data': [{'exists': 0}]}


@api_user.route('/api/users/parents', methods=['GET'])
def users_parents_get():
    vres = verify_auto(request, allows=['admin', 'staff'])
    if not vres['code'] == 0:
        # verification failed
        vres['count'] = 0
        vres['data'] = []
        return vres
    page = request.args.get('page')
    limit = request.args.get('limit')
    
    if page is None or limit is None:
        page = 0
        limit = 0
    else:
        page = int(page)-1
        limit = int(limit)
    # is simple?
    simple = request.args.get('simple')
    if str(simple) == '1':
        simple = True
    else:
        simple = False
    parents = get_parents(page, limit, simple=simple)
    return parents


@api_user.route('/api/users/parent', methods=['GET'])
def users_parent_get():
    vres = verify_auto(request, allows=['admin', 'staff', 'parent'])
    if not vres['code'] == 0:
        # verification failed
        vres['count'] = 0
        vres['data'] = []
        return vres
    _sk = vres['msg']
    _id = gv.logged[_sk]['id']
    _role = gv.logged[_sk]['role']
    if _role in ['admin', 'staff']:
        _param_id = request.args.get('id')
        if _param_id is not None:
            _id = _param_id    
    parent = get_parent(_id)
    return parent


@api_user.route('/api/users/admin', methods=['GET'])
def users_admin_get():
    vres = verify_auto(request, allows=['admin'])
    if not vres['code'] == 0:
        # verification failed
        vres['count'] = 0
        vres['data'] = []
        return vres
    _id = gv.logged[vres['msg']]['id']
    _param_id = request.args.get('id')
    if _param_id is not None:
        _id = _param_id
    admin = get_userinfo(_id)
    return admin

@api_user.route('/api/users/parent/cids', methods=['GET'])
def users_parent_cids_get():
    vres = verify_auto(request, allows=['parent'])
    if not vres['code'] == 0:
        # verification failed
        vres['count'] = 0
        vres['data'] = []
        return vres
    _sk = vres['msg']
    _pid = gv.logged[_sk]['id']
    return get_child_ids(_pid)


@api_user.route('/api/users/parent', methods=['POST'])
def users_parent_post():
    vres = verify_auto(request, allows=['admin', 'staff'])
    if not vres['code'] == 0:
        # verification failed
        vres['count'] = 0
        vres['data'] = []
        return vres
    res = insert_parent()
    return res


@api_user.route('/api/users/parent', methods=['PUT'])
def users_parent_put():
    vres = verify_auto(request, allows=['admin', 'staff'])
    if not vres['code'] == 0:
        # verification failed
        vres['count'] = 0
        vres['data'] = []
        return vres
    res = update_parent()
    return res


@api_user.route('/api/users/parent', methods=['DELETE'])
def users_parent_delete():
    vres = verify_auto(request, allows=['admin', 'staff'])
    if not vres['code'] == 0:
        # verification failed
        vres['count'] = 0
        vres['data'] = []
        return vres
    res = delete_user_by_id('parent')
    return res


@api_user.route('/api/users/staffs', methods=['GET'])
def users_staffs_get():
    vres = verify_auto(request, allows=['admin'])
    if not vres['code'] == 0:
        # verification failed
        vres['count'] = 0
        vres['data'] = []
        return vres
    page = request.args.get('page')
    limit = request.args.get('limit')
    if page is None or limit is None:
        page = 0
        limit = 0
    else:
        page = int(page)-1
        limit = int(limit)
    staffs = get_staffs(page, limit)
    return staffs


@api_user.route('/api/users/staff', methods=['GET'])
def users_staff_get():
    vres = verify_auto(request, allows=['admin'])
    if not vres['code'] == 0:
        # verification failed
        vres['count'] = 0
        vres['data'] = []
        return vres
    id = request.args.get('id')
    if id is None:
        return {'code': 40, 'msg': 'id is needed', 'count': 0, 'data': []}
    staffs = get_staff(id)
    return staffs


@api_user.route('/api/users/staff', methods=['POST'])
def users_staff_post():
    vres = verify_auto(request, allows=['admin'])
    if not vres['code'] == 0:
        # verification failed
        vres['count'] = 0
        vres['data'] = []
        return vres
    res = insert_staff()
    return res


@api_user.route('/api/users/staff', methods=['PUT'])
def users_staff_put():
    vres = verify_auto(request, allows=['admin'])
    if not vres['code'] == 0:
        # verification failed
        vres['count'] = 0
        vres['data'] = []
        return vres
    res = update_staff()
    return res


@api_user.route('/api/users/staff', methods=['DELETE'])
def users_staff_delete():
    vres = verify_auto(request, allows=['admin'])
    if not vres['code'] == 0:
        # verification failed
        vres['count'] = 0
        vres['data'] = []
        return vres
    res = delete_user_by_id('staff')
    return res


@api_user.route('/api/passwd/sendVCode', methods=['GET'])
def send_vcode():
    # test username, email, time
    username = request.args.get('username')
    email = request.args.get('email')
    if username is None or username == '':
        return ee.PARAMERR(app=': username')
    if email is None or email == '':
        return ee.PARAMERR(app=': email')
    if username in gv.vcode:
        _t = int(time.time())
        if _t - gv.vcode[username]['time'] < 25:
            return ee.FREQ(app=': less than 25s')
    _user = get_id_by_username(username)
    if _user['code'] != 0:
        return ee.DBERR(': chk un')
    if len(_user['data']) == 0:
        return ee.IDERR(app=': username is incorrect')
    if _user['data'][0]['email'] != email:
        return ee.IDERR(app=': email is incorrect')
    gv.vcode[username] = {
        'email': email,
        'id': _user['data'][0]['id'],
        'time': int(time.time())
    }

    try:
        vcode = random.randint(0, 99999999)
        vcode = str(vcode).zfill(8)
        gv.vcode[username]['vcode'] = vcode
        _html = render_template('mail_vcode.html', vcode=vcode)
        app = current_app._get_current_object()
        thr = Thread(target=send_email, args=[app, username, _html])
        thr.start()
    except:
        emsg = 'Error when sending email\n' + traceback.format_exc()
        gv.logger.error(emsg)
        return ee.UNKNOWN()
    return ee.NORMAL()


def send_email(app, username, mailcont):
    with app.app_context():
        to_ = gv.vcode[username]['email']
        title = 'A verification code'
        msg = Message(title, sender=gv.mail_un, recipients=[to_])
        msg.html = mailcont
        gv.mail.send(msg)


@api_user.route('/api/passwd', methods=['PUT'])
def passwd_put():
    _un = request.form.get('username')
    _pw = request.form.get('passwd_md5')
    _vc = request.form.get('vcode')
    _pa = request.form.get('parent_allow')
    print("Debug")
    print(_un)
    print()
    if None in [_un, _pw, _vc, _pa]:
        return ee.PARAMERR()
    if _pa == 'Tm8=':
        return ee.PARAMERR(msg='account is disable')
    if _pw == '':
        return ee.PARAMERR(msg='invalid password')
    if _un not in gv.vcode:
        return ee.UNKNOWN()
    _ovc = gv.vcode[_un]['vcode']
    _t = gv.vcode[_un]['time']
    if int(time.time()) - _t > 1800:
        return ee.TIMEOUT(msg='verification code time out (more than 30min)')
    if str(_ovc) != str(_vc).zfill(8):
        return ee.VCODEERR()
    _id = gv.vcode[_un]['id']
    sqlstr = "update `user` set passwdmd5='{0}' where id={1};".format(
        _pw, _id)
    try:
        conn = gv.dbpool.connection()
        cur = conn.cursor()
        cur.execute("SET NAMES UTF8;")
        cur.execute(sqlstr.encode("utf-8", "ignore"))
        conn.commit()
        cur.close()
        conn.close()
        del gv.vcode[_un]
        return ee.NORMAL()
    except:
        emsg = 'DB error in update pw.\n'+traceback.format_exc()
        gv.logger.error(emsg)
        return ee.DBERR()
    return ee.UNKNOWN


