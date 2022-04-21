#!/usr/bin/env python3
# -*- coding:utf-8 -*-
"""
status API蓝图
定义蓝图api_status，实现status相关操作蓝图
视图含义见对应api文档
"""
import datetime
import time
import traceback

from flask import Blueprint, request

import funcs
import global_var as gv
from api_loginout import verify_auto
from api_user import get_id_by_username
from db_params import status_tables as sttb
from db_params import get_index
from db_params import status_type_tbn as tptbn
from api_children import get_cid_by_child_no
from global_var import enum_error as ee
import copy

# 定义蓝图-------------------------------------------------
api_status = Blueprint(
    'api_status',
    __name__,
    template_folder='templates'
)

# functions--------------------------------------------


def child_exists(cid):
    '''
    判断孩子id是否存在
    '''
    sqlstr = "select 1 from child where id={cid};".format(cid=str(cid))
    try:
        conn = gv.dbpool.connection()
        cur = conn.cursor()
        cur.execute("SET NAMES UTF8;")
        cur.execute(sqlstr.encode("utf-8", "ignore"))
        res = cur.fetchall()
        if res is None:
            _ex = ee.DBERR(app=(': when check child id'))
        elif len(res) > 0:
            _ex = ee.NORMAL()
            _ex['data'].append({'exists': True})
        else:
            _ex = ee.NORMAL()
            _ex['data'].append({'exists': False})
        cur.close()
        conn.close()
        return _ex
    except:
        estr = traceback.format_exc()
        gv.logger.error('database error!\n'+estr)
        return ee.DBERR()
    return ee.UNKNOWN()

# get ========


def do_query_status(stype):
    vres = verify_auto(request, allows=['admin', 'staff'])
    if not vres['code'] == 0:
        # verification failed
        vres['count'] = 0
        vres['data'] = []
        return vres
    sid = request.args.get('id')
    if sid is None:
        return ee.PARAMERR(app=': id')
    if type(sid) == type('') and not str.isdigit(sid):
        return ee.PARAMERR(app=': id')
    res = get_status_by_id(stype, sid=sid)
    return res


def get_status_by_id(stype, sid):
    '''
    get status by id
    '''
    tdef = copy.deepcopy(sttb[stype])
    cidi = get_index(tdef['flist'], 'child_id')
    if cidi is not None:
        tdef['flist'][cidi]['type']='str'
    wstr = 'where id={0}'.format(str(sid))
    try:
        conn = gv.dbpool.connection()
        cur = conn.cursor()
        cur.execute("SET NAMES UTF8;")
        datas = funcs.get_datas(cur, tdef['tbn'], tdef['flist'],
                                wstr=wstr, logger=gv.logger)
        if stype != 'temperature':
            for line in datas['data']:
                if line['status'] is not None:
                    line['status'] = gv.enum_selector[tptbn[stype]][int(line['status'])]
        cur.close()
        conn.close()
        return datas
    except:
        estr = traceback.format_exc()
        gv.logger.error('database error!\n'+estr)
        return ee.DBERR()
    return ee.UNKNOWN()


# delete ========


def do_delete_status(stype):
    vres = verify_auto(request, allows=['admin', 'staff'])
    if not vres['code'] == 0:
        # verification failed
        vres['count'] = 0
        vres['data'] = []
        return vres
    sid = request.form.get('id')
    if sid is None:
        return ee.PARAMERR(app=': id')
    if type(sid) == type('') and not str.isdigit(sid):
        return ee.PARAMERR(app=': id')
    res = delete_status(stype, sid=sid)
    return res


def delete_status(stbn, sid):
    '''
    从数据库删除状态信息
    :param stbn:    表名
    :param sid:     状态信息id
    :return :       
    '''
    try:
        conn = gv.dbpool.connection()
        cur = conn.cursor()
        cur.execute("SET NAMES UTF8;")
        sqlstr = 'delete from `{0}` where id={1};'.format(stbn, str(sid))
        cur.execute(sqlstr.encode("utf-8", "ignore"))
        conn.commit()
        cur.close()
        conn.close()
        return ee.NORMAL()
    except:
        estr = traceback.format_exc()
        gv.logger.error('database error!\n'+estr)
        return ee.DBERR()
    return ee.UNKNOWN()


# post ========
def do_insert_status(stype):
    vres = verify_auto(request, allows=['admin', 'staff'])
    if not vres['code'] == 0:
        # verification failed
        vres['count'] = 0
        vres['data'] = []
        return vres
    res = insert_status(stype)
    return res


def insert_status(stype):
    '''
    '''
    tdef = copy.deepcopy(sttb[stype])
    del tdef['flist'][get_index(tdef['flist'], 'id')]
    # get and check params
    for fd in tdef['flist']:
        if fd['fn'] == 'staff':
            # 直接获取当前登录id，不需取值
            _sk = request.form.get('secret_key')
            fd['val'] = gv.logged[_sk]['id']
            continue
        val = request.form.get(fd['fn'])
        if fd['type'] == 'int':
            if type(val) == type(''):
                if not str.isdigit(val):
                    return ee.PARAMERR(app=': '+fd['fn'])
            if fd['fn'] == 'child_id':
                if val is None:
                    # check alias 
                    _alias = request.form.get('alias')
                    if _alias is None:
                        return ee.PARAMERR(app=': child_id or alias is needed')
                    _cid = get_cid_by_child_no(_alias)
                    if _cid['code']!=0:
                        return _cid
                    if len(_cid['data'])==0:
                        return ee.IDERR(app=': alias not exists')
                    val = _cid['data'][0]['id']
                else:
                    _ex = child_exists(val)
                    if _ex['code'] != 0:
                        return _ex
                    if not _ex['data'][0]['exists']:
                        return ee.IDERR(app=': child id incorrect')
        elif fd['fn'] == 'time':
            if type(val) == type(''):
                try:
                    # check
                    datetime.datetime.strptime(val, '%Y-%m-%d %H:%M:%S')
                except:
                    return ee.PARAMERR(app=': '+fd['fn'])
            elif val is not None:
                return ee.PARAMERR(app=': '+fd['fn'])
            else:
                val = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
        fd['val'] = val
    
    # insert
    try:
        conn = gv.dbpool.connection()
        cur = conn.cursor()
        cur.execute("SET NAMES UTF8;")
        res = funcs.insert_if_not_exists(cur, tdef['tbn'], tdef['flist'],
                                         chkfn=None, logger=gv.logger)
        conn.commit()
        cur.close()
        conn.close()
        return res
    except:
        estr = traceback.format_exc()
        gv.logger.error('database error!\n'+estr)
        return ee.DBERR()
    return ee.UNKNOWN()


# put ========
def do_update_status(stype):
    vres = verify_auto(request, allows=['admin', 'staff'])
    if not vres['code'] == 0:
        # verification failed
        vres['count'] = 0
        vres['data'] = []
        return vres
    sid = request.args.get('id')
    if sid is None:
        return ee.PARAMERR(app=': id')
    if type(sid) == type('') and not str.isdigit(sid):
        return ee.PARAMERR(app=': id')
    res = update_status(stype, sid)
    return res


def update_status(stype, sid):
    '''
    '''
    tdef = copy.deepcopy(sttb[stype])
    del tdef['flist'][get_index(tdef['flist'], 'id')]
    # get and check params
    for fd in tdef['flist']:
        if fd['fn'] == 'staff':
            # 直接获取当前登录id，不需取值
            _sk = request.form.get('secret_key')
            fd['val'] = gv.logged[_sk]['id']
            continue
        val = request.form.get(fd['fn'])
        if fd['type'] == 'int':
            # 检验是否是int
            if type(val) == type(''):
                if not str.isdigit(val):
                    return ee.PARAMERR(app=': '+fd['fn'])
            # child id 需要检验存在性
            if fd['fn'] == 'child_id':
                if val is None:
                    return ee.PARAMERR(app=': '+fd['fn']+' is needed')
                _ex = child_exists(val)
                if _ex['code'] != 0:
                    return _ex
                if not _ex['data'][0]['exists']:
                    return ee.IDERR(app=': child id incorrect')
        elif fd['fn'] == 'time':
            if type(val) == type(''):
                try:
                    # check
                    datetime.datetime.strptime(val, '%Y-%m-%d %H:%M:%S')
                except:
                    return ee.PARAMERR(app=': '+fd['fn'])
            elif val is not None:
                return ee.PARAMERR(app=': '+fd['fn'])
        fd['val'] = val
    sstr = funcs.build_set_str(tdef['flist'])
    if sstr is None:
        return ee.PARAMERR()
    if sstr == '':
        return ee.PARAMERR(app=': no values to update')
    sqlstr = 'update `{tbn}` set {sstr} where id={sid};'.format(
        tbn=tdef['tbn'], sstr=sstr, sid=str(sid))
    # update
    try:
        conn = gv.dbpool.connection()
        cur = conn.cursor()
        cur.execute("SET NAMES UTF8;")
        cur.execute(sqlstr.encode("utf-8", "ignore"))
        conn.commit()
        cur.close()
        conn.close()
        return ee.NORMAL()
    except:
        estr = traceback.format_exc()
        gv.logger.error('database error!\n'+estr)
        return ee.DBERR()
    return ee.UNKNOWN()


# views------------------------------------------------


@api_status.route('/api/status/temperature', methods=['GET'])
def status_temperature_get():
    return do_query_status('temperature')


@api_status.route('/api/status/skin', methods=['GET'])
def status_skin_get():
    return do_query_status('skin')


@api_status.route('/api/status/meal', methods=['GET'])
def status_meal_get():
    return do_query_status('meal')


@api_status.route('/api/status/nap', methods=['GET'])
def status_nap_get():
    return do_query_status('nap')


@api_status.route('/api/status/diaper', methods=['GET'])
def status_diaper_get():
    return do_query_status('diaper')


@api_status.route('/api/status/health', methods=['GET'])
def status_health_get():
    return do_query_status('health')


@api_status.route('/api/status/perform', methods=['GET'])
def status_perform_get():
    return do_query_status('perform')


@api_status.route('/api/status/temperature', methods=['DELETE'])
def status_temperature_delete():
    return do_delete_status('temperature')


@api_status.route('/api/status/skin', methods=['DELETE'])
def status_skin_delete():
    return do_delete_status('skin')


@api_status.route('/api/status/meal', methods=['DELETE'])
def status_meal_delete():
    return do_delete_status('meal')


@api_status.route('/api/status/nap', methods=['DELETE'])
def status_nap_delete():
    return do_delete_status('nap')


@api_status.route('/api/status/diaper', methods=['DELETE'])
def status_diaper_delete():
    return do_delete_status('diaper')


@api_status.route('/api/status/health', methods=['DELETE'])
def status_health_delete():
    return do_delete_status('health')


@api_status.route('/api/status/perform', methods=['DELETE'])
def status_perform_delete():
    return do_delete_status('perform')


@api_status.route('/api/status/temperature', methods=['POST'])
def status_temperature_post():
    return do_insert_status('temperature')


@api_status.route('/api/status/skin', methods=['POST'])
def status_skin_post():
    return do_insert_status('skin')


@api_status.route('/api/status/meal', methods=['POST'])
def status_meal_post():
    return do_insert_status('meal')


@api_status.route('/api/status/nap', methods=['POST'])
def status_nap_post():
    return do_insert_status('nap')


@api_status.route('/api/status/diaper', methods=['POST'])
def status_diaper_post():
    return do_insert_status('diaper')


@api_status.route('/api/status/health', methods=['POST'])
def status_health_post():
    return do_insert_status('health')


@api_status.route('/api/status/perform', methods=['POST'])
def status_perform_post():
    return do_insert_status('perform')


@api_status.route('/api/status/temperature', methods=['PUT'])
def status_temperature_put():
    return do_update_status('temperature')


@api_status.route('/api/status/skin', methods=['PUT'])
def status_skin_put():
    return do_update_status('skin')


@api_status.route('/api/status/meal', methods=['PUT'])
def status_meal_put():
    return do_update_status('meal')


@api_status.route('/api/status/nap', methods=['PUT'])
def status_nap_put():
    return do_update_status('nap')


@api_status.route('/api/status/diaper', methods=['PUT'])
def status_diaper_put():
    return do_update_status('diaper')


@api_status.route('/api/status/health', methods=['PUT'])
def status_health_put():
    return do_update_status('health')


@api_status.route('/api/status/perform', methods=['PUT'])
def status_perform_put():
    return do_update_status('perform')
