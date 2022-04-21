#!/usr/bin/env python3
# -*- coding:utf-8 -*-
"""
files API蓝图
定义蓝图api_files，实现files相关操作蓝图
视图含义见对应api文档
"""
import datetime
import time
import traceback

from flask import Blueprint, request, Response,render_template
from urllib.parse import unquote, quote
import pandas.io.sql as sql
import funcs
import os
import global_var as gv
from api_loginout import verify_auto,loggeduser
from api_children import get_cid_by_child_no
from global_var import enum_error as ee
from db_params import get_index
from copy import deepcopy

# 定义蓝图-------------------------------------------------
api_files = Blueprint(
    'api_files',
    __name__,
    template_folder='templates'
)

# functions--------------------------------------------
flist = [
    {'fn': 'id', 'type': 'int', 'sorted':1},
    {'fn': 'child_id', 'type': 'int'},
    {'fn': 'filename', 'type': 'str'},
    {'fn': 'originfn', 'type': 'b64str'}
]

filedir = 'files'


def get_file_list(page=0, limit=0, cid=None):
    '''
    get file list from database
    :param page:
    :param limit:
    :param cid:     child id, 空则不限制
    '''
    fl = deepcopy(flist)
    fl[1]['type'] = 'str'
    del fl[2]
    fl[2]['as'] = 'filename'
    wstr = ''
    if cid is not None:
        wstr = 'where child_id={0}'.format(str(cid))
    try:
        conn = gv.dbpool.connection()
        cur = conn.cursor()
        cur.execute("SET NAMES UTF8;")
        datas = funcs.get_datas(cur, 'files', fl, page=page, limit=limit,
                                wstr=wstr, logger=gv.logger)
        cur.close()
        conn.close()
        return datas
    except:
        estr = traceback.format_exc()
        gv.logger.error('database error!\n'+estr)
        return ee.DBERR()
    return ee.UNKNOWN()


def get_file_info(fid):
    '''
    get file list from database
    :param fid:     file id
    '''
    wstr = 'where id={0}'.format(str(fid))
    fl = deepcopy(flist)
    fl[1]['type'] = 'str'
    try:
        conn = gv.dbpool.connection()
        cur = conn.cursor()
        cur.execute("SET NAMES UTF8;")
        datas = funcs.get_datas(cur, 'files', flist,
                                wstr=wstr, logger=gv.logger)
        cur.close()
        conn.close()
        return datas
    except:
        estr = traceback.format_exc()
        gv.logger.error('database error!\n'+estr)
        return ee.DBERR()
    return ee.UNKNOWN()

def delete_file(fid):
    '''
    delete file from database and disk
    '''
    finfo = get_file_info(fid)
    if finfo['code']!=0:
        return finfo
    if len(finfo['data'])==0:
        return ee.IDERR(msg='file with this id not found')
    finfo = finfo['data'][0]
    _fn = finfo['filename']
    _fpath = os.path.join(filedir, _fn)
    if os.path.exists(_fpath):
        try:
            os.remove(_fpath)
        except:
            return ee.UNKNOWN(msg='error occured when deleting file')
    # delete info in db
    sqlstr = 'delete from files where id={};'.format(str(fid))
    try:
        conn = gv.dbpool.connection()
        cur = conn.cursor()
        cur.execute("SET NAMES UTF8;")
        cur.execute(sqlstr.encode('utf-8', 'ignore'))
        conn.commit()
        cur.close()
        conn.close()
        return ee.NORMAL()
    except:
        estr = traceback.format_exc()
        gv.logger.error('database error!\n'+estr)
        return ee.DBERR()
    return ee.UNKNOWN()



def insert_file_info(cid, filename, originfn):
    '''
    insert file info into database
    '''
    fl = deepcopy(flist)
    del fl[0]
    fl[0]['val'] = cid
    fl[1]['val'] = filename
    fl[2]['val'] = originfn
    try:
        conn = gv.dbpool.connection()
        cur = conn.cursor()
        cur.execute("SET NAMES UTF8;")
        res = funcs.insert_if_not_exists(
            cur, 'files', fl, chkfn=None, logger=gv.logger)
        conn.commit()
        cur.close()
        conn.close()
        return res
    except:
        estr = traceback.format_exc()
        gv.logger.error('database error!\n'+estr)
        return ee.DBERR()
    return ee.UNKNOWN()


# views------------------------------------------------


@api_files.route('/api/files', methods=['GET'])
def files_get():
    vres = verify_auto(request, allows=['admin', 'staff'])
    if not vres['code'] == 0:
        # verification failed
        vres['count'] = 0
        vres['data'] = []
        return vres
    page = request.args.get('page')
    limit = request.args.get('limit')
    cid = request.args.get('child_id')
    if page is None or limit is None:
        page = 0
        limit = 0
    else:
        page = int(page)-1
        limit = int(limit)
    if type(cid) == type('') and not str.isdigit(cid):
        return ee.PARAMERR(app=": child_id")
    if cid is None:
        _child_no = request.args.get('child_no')
        if _child_no is not None:
            _cidfa = get_cid_by_child_no(_child_no)
            if _cidfa['code']!=0:
                return _cidfa
            if len(_cidfa['data'])>0:
                cid=_cidfa['data'][0]['id']
    res = get_file_list(page, limit, cid)
    return res

@api_files.route('/api/file', methods=['DELETE'])
def file_delete():
    vres = verify_auto(request, allows=['admin', 'staff'])
    if not vres['code'] == 0:
        # verification failed
        vres['count'] = 0
        vres['data'] = []
        return vres
    fid = request.form.get('id')
    if type(fid) == type('') and not str.isdigit(fid):
        return ee.PARAMERR(app=": id")
    res = delete_file(fid)
    return res

@api_files.route('/api/file', methods=['POST'])
def file_post():
    vres = verify_auto(request, allows=['admin', 'staff'])
    if not vres['code'] == 0:
        # verification failed
        vres['count'] = 0
        vres['data'] = []
        return vres
    cid = request.form.get('child_id')
    if type(cid) == type('') and not str.isdigit(cid):
        return ee.PARAMERR(app=": child_id")
    if cid is None:
        _child_no = request.form.get('child_no')
        if _child_no is None:
            return ee.PARAMERR(app=': child_id or child_no is needed')
        _cidfa = get_cid_by_child_no(_child_no)
        if _cidfa['code']!=0:
            return _cidfa
        if len(_cidfa['data'])>0:
            cid=_cidfa['data'][0]['id']
    if cid is None:
        return ee.IDERR(app=': incorrect id or child_no')
    file = request.files['file']
    if file is None:
        return ee.PARAMERR(': no file')

    originfn = file.filename
    if originfn is None or len(originfn) < 1:
        return ee.PARAMERR(app=": filename error")
    filename = funcs.get_md5(originfn+str(cid))
    filepath = os.path.join(filedir, filename)
    if os.path.exists(filepath):
        return ee.PARAMERR(': file already exists')
    funcs.mkdir(filedir)
    file.save(filepath)
    res = insert_file_info(cid, filename, originfn)
    return res


@api_files.route('/api/file', methods=['GET'])
def file_get():
    vres = verify_auto(request, allows=['admin', 'staff'])
    if not vres['code'] == 0:
        # verification failed
        vres['count'] = 0
        vres['data'] = []
        return vres
    fid = request.args.get('id')
    if not (type(fid)==type('') and str.isdigit(fid)):
        return ee.PARAMERR(app=": id")
    finfo = get_file_info(fid)
    if finfo['code']!=0:
        return finfo
    if len(finfo['data'])==0:
        return ee.IDERR(msg='file id is incorrect')
    fullfilename = os.path.join(filedir, finfo['data'][0]['filename'])
    if not os.path.exists(fullfilename):
        return ee.IDERR('file not found')
    # 普通下载
    # response = make_response(send_from_directory(filepath, filename, as_attachment=True))
    # response.headers["Content-Disposition"] = "attachment; filename={}".format(filepath.encode().decode('latin-1'))
    # return send_from_directory(filepath, filename, as_attachment=True)
    # 流式读取

    _block_size = 8 * 1024 * 1024
    def send_file():
        store_path = fullfilename
        with open(store_path, 'rb') as targetfile:
            while 1:
                data = targetfile.read(_block_size)
                if not data:
                    break
                yield data

    response = Response(send_file(), content_type='application/octet-stream')
    # 设置文件名，url编码以适应中文
    _fn = quote(finfo['data'][0]['originfn'])
    response.headers['Content-disposition'] = "attachment; filename*=utf-8''{}".format(_fn)
    #response.headers["Content-disposition"] = 'attachment; filename=%s' % finfo['data'][0]['originfn']
    return response
    
    
    
