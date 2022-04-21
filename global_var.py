#!/usr/bin/env python3
# -*- coding:utf-8 -*-
"""
定義全局變量
    global fpid
    global config
    global dbconf
    global dbpool
    global logger
    global logged
    global enum_selector
    class enum_error
    global groups
    global selector_tbn_fn
    global secrets
    global mail
    global vcode
    global i18n
    global logintimeout
"""
import base64
import configparser
import traceback

import MySQLdb
from DBUtils.PooledDB import PooledDB
import os

# 一些常量
# manager的角色名称
from preenv import manager_role as mr
from preenv import tbn_fn
from copy import deepcopy

manager_role = mr


class enum_error():
    __NORMAL = {'code':0, 'msg':'', 'count':0, 'data':[]}
    __DBERR = {'code':10, 'msg':'database error', 'count':0, 'data':[]}
    __VERERR = {'code':20, 'msg':'verification failed', 'count':0, 'data':[]}
    __NOT_LOGGED = {'code':21, 'msg':'not logged in', 'count':0, 'data':[]}
    __TIMEOUT = {'code':22, 'msg':'login timeout', 'count':0, 'data':[]}
    __PWERR = {'code':23, 'msg':'password error', 'count':0, 'data':[]}
    __SIGNERR = {'code':24, 'msg':'sign error', 'count':0, 'data':[]}
    __NOAUTHORITY = {'code':30, 'msg':'no authority', 'count':0, 'data':[]}
    __PARAMERR = {'code':40, 'msg':'parameter error', 'count':0, 'data':[]}
    __UN_EXISTS = {'code':50, 'msg':'username already exists', 'count':0, 'data':[]}
    __IDERR = {'code':51, 'msg':'id is incorrect', 'count':0, 'data':[]}
    __VCODEERR = {'code':60, 'msg':'verification code is incorrect', 'count':0, 'data':[]}
    __FILE_TO_BIG = {'code':70, 'msg':'file is too large', 'count':0, 'data':[]}
    __FREQ = {'code':80, 'msg':'too frequent', 'count':0, 'data':[]}
    __UNKNOWN = {'code':-1, 'msg':'unknown error', 'count':0, 'data':[]}

    @classmethod
    def __setret(cls,e,msg,app):
        if msg is not None:
            e['msg'] = msg
        if app is not None:
            e['msg'] = e['msg'] + app
        return e

    @classmethod
    def NORMAL(cls,msg=None,app=None,count=0):
        e = deepcopy(cls.__NORMAL)
        e['count'] = count
        return cls.__setret(e, msg, app)
    @classmethod
    def DBERR(cls,msg=None,app=None):
        e = deepcopy(cls.__DBERR)
        return cls.__setret(e, msg, app)
    @classmethod
    def VERERR(cls,msg=None,app=None):
        e = deepcopy(cls.__VERERR)
        return cls.__setret(e, msg, app)
    @classmethod
    def NOT_LOGGED(cls,msg=None,app=None):
        e = deepcopy(cls.__NOT_LOGGED)
        return cls.__setret(e, msg, app)
    @classmethod
    def TIMEOUT(cls,msg=None,app=None):
        e = deepcopy(cls.__TIMEOUT)
        return cls.__setret(e, msg, app)
    @classmethod
    def PWERR(cls,msg=None,app=None):
        e = deepcopy(cls.__PWERR)
        return cls.__setret(e, msg, app)
    @classmethod
    def SIGNERR(cls,msg=None,app=None):
        e = deepcopy(cls.__SIGNERR)
        return cls.__setret(e, msg, app)
    @classmethod
    def NOAUTHORITY(cls,msg=None,app=None):
        e = deepcopy(cls.__NOAUTHORITY)
        return cls.__setret(e, msg, app)
    @classmethod
    def PARAMERR(cls,msg=None,app=None):
        e = deepcopy(cls.__PARAMERR)
        return cls.__setret(e, msg, app)
    @classmethod
    def UN_EXISTS(cls,msg=None,app=None):
        e = deepcopy(cls.__UN_EXISTS)
        return cls.__setret(e, msg, app)
    @classmethod
    def IDERR(cls,msg=None,app=None):
        e = deepcopy(cls.__IDERR)
        return cls.__setret(e, msg, app)
    @classmethod
    def VCODEERR(cls,msg=None,app=None):
        e = deepcopy(cls.__VCODEERR)
        return cls.__setret(e, msg, app)
    @classmethod
    def FILE_TO_BIG(cls,msg=None,app=None):
        e = deepcopy(cls.__FILE_TO_BIG)
        return cls.__setret(e, msg, app)
    @classmethod
    def UNKNOWN(cls,msg=None,app=None):
        e = deepcopy(cls.__UNKNOWN)
        return cls.__setret(e, msg, app)
    @classmethod
    def FREQ(cls,msg=None,app=None):
        e = deepcopy(cls.__FREQ)
        return cls.__setret(e, msg, app)

def init_global(applogger, appmail, glbconfig):
    """
    init global
    Only call when app start
    """
    global fpid
    global config
    global dbconf
    global dbpool
    global logger
    global logged
    global groups
    global enum_selector
    global selector_tbn_fn
    global secrets
    global mail
    global mail_un
    global vcode
    global logintimeout
    vcode = {}  # key: username, val: {'email','time','vcode','id'}
    logger = applogger
    selector_tbn_fn = tbn_fn
    secrets = {}
    mail = appmail
    mail_un = glbconfig.get('mail', 'username')
    logintimeout = glbconfig.getint('web', 'logintimeout')
    # database
    try:
        fpid = "135790"    # 标记本次进程的
        config = glbconfig
        # 数据库连接池
        # database info
        dbconf = \
            {
                "user": config.get("database", "user"),
                "passwd": config.get("database", "passwd"),
                "host": config.get("database", "host"),
                "port": config.getint("database", "port"),
                "db": config.get("database", "db"),
                "charset": config.get("database", "charset")
            }
        dbpool = PooledDB(MySQLdb, 10, **dbconf)
        logged = {}     # 已登录用户和token
        # 獲取selector
        enum_selector = get_selectors(dbpool,logger)
        groups = get_groups(dbpool)
        load_i18n(logger)
    except:
        msg1 = traceback.format_stack()
        msgstr = "\n".join(msg1)
        msgstr += "\n" + traceback.format_exc()
        logger.fatal("Error in init...\n"+str(msgstr))
        exit(-1)


def load_i18n(logger):
    '''
    load i18n file
    '''
    global i18n
    i18ndir = os.path.join('static', 'i18n')
    i18n = {}
    if not os.path.exists(i18ndir):
        logger.warning('static/i18n directory is not found!')
        return
    try:
        for _path,_subpath,_fns in os.walk(i18ndir):
            for _sp in _subpath:
                i18n[_sp] = {}
                _np = os.path.join(_path, _sp)
                for _p,_s,_f in os.walk(_np):
                    for _fn in _f:
                        _fp = os.path.join(_p, _fn)
                        _file = open(_fp, encoding='utf-8')
                        _lines = _file.readlines()
                        _file.close()
                        i18n[_sp][_fn] = ''.join(_lines)
    except:
        emsg = traceback.format_exc()
        logger.fatal('error when init i18n' + emsg)
        exit(-1)



def get_selectors(dbpool,logger):
    """
    get selectors from db
    """
    resenum = {}
    sqlstr1 = "select `id`,`{f1}`,`{f2}` from `{tbn}`;"
    #Debug
    #logger.info(sqlstr1)
    conn = dbpool.connection()
    cur = conn.cursor()
    cur.execute("SET NAMES UTF8;")
    # status
    for tbi, tbv in selector_tbn_fn.items():
        sqlstr = sqlstr1.format(tbn=tbi, f1=tbv['f1'], f2=tbv['f2'])
        #cur.execute(sqlstr.encode("utf-8", "ignore"))
        cur.execute(sqlstr.encode("cp1252", "ignore"))
        res = cur.fetchall()
        resenum[tbi] = {}
        if res is None:
            continue
        for line in res:
            resenum[tbi][int(line[0])]={
                'id':int(line[0]),
                'val': line[1],
                'val_chi': base64.b64decode(line[2]).decode('utf8')
            }
    cur.close()
    conn.close()
    return resenum

def get_groups(dbpool):
    """
    get groups from db
    """
    # groups
    resenum = []
    sqlstr = "select `id`,`smon`,`emon`,`name` from `group`;"
    conn = dbpool.connection()
    cur = conn.cursor()
    cur.execute("SET NAMES UTF8;")
    cur.execute(sqlstr.encode("utf-8", "ignore"))
    res = cur.fetchall()
    if res is not None:
        for line in res:
            resenum.append({
                'id': int(line[0]),
                'smon': int(line[1]),
                'emon': int(line[2]),
                'name': line[3]
            })
    cur.close()
    conn.close()
    return resenum
