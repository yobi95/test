#!/usr/bin/env python3
# -*- coding:utf-8 -*-
"""
    functions
"""

import hashlib
import logging
import os
import random
import sys
import time
import base64
import traceback

# encrypt----------------------------------------------


def get_random_int64():
    '''
    随机生成64bit长度内的正整数
    '''
    maxi = 0x7fffffffffffffff
    a = random.randint(0, maxi)
    return a


def get_md5(orgstr, encoding='utf-8'):
    _m2 = hashlib.md5()
    _m2.update(orgstr.encode(encoding, "ignore"))
    return _m2.hexdigest()


def b64encode(orgstr, encoding='utf-8'):
    '''
    转换时如果输入是None，则返回''
    :return : base64 string
    '''
    if orgstr is None:
        return ''
    return base64.b64encode(orgstr.encode('utf8')).decode()


def b64decode(b64str, encoding='utf-8'):
    '''
    转换时如果输入是None，则返回''
    :return : normal string
    '''
    if b64str is None:
        return ''
    return base64.b64decode(b64str).decode(encoding)

# database---------------------------------------------


def _build_flist(flist):
    """
    此函数无效。不要调用。仅参考flist定义
    :param flist:   字段定义列表，一个有序列表，每一个元素都定义一个字段，格式：
        flist = [
            {'fn':'id','type':'int' [,'val':val] [,'sorted':0][, 'as':'key']}
        ]
        其中，必选参数：
            fn:     field name，字段名
            type:   类型，可取值：int, float，str，b64str，
        可选参数
            val:    值
            sorted: 按字段排序，如果设置sorted，会按照此字段排序，多个字段设置只有一个会生效
                    0=升序，1=降序
            as:     在输出的时候指定输出字典中改字段的key
    """
    return None


def build_field_str(flist):
    """
    构建SQL字段字符串
    :param flist: 字段定义列表，格式见_build_flist的注释
    """
    return ','.join(['`'+line['fn']+'`' for line in flist])


def build_values_str(flist):
    """
    构建SQL值字符串
    :param flist: 字段定义列表，格式见_build_flist的注释
    :return : string or None
    """
    try:
        vssl = []
        for line in flist:
            if 'val' not in line:
                line['val'] = None
            if line['type'] == 'int':
                if line['val'] is not None:
                    if type(line['val']) == type(''):
                        if not is_number(line['val']):
                            return None
                    vssl.append(str(int(line['val'])))
                else:
                    vssl.append('null')
            elif line['type'] == 'float':
                if line['val'] is not None:
                    if type(line['val']) == type(''):
                        if not is_number(line['val']):
                            return None
                    vssl.append(str(float(line['val'])))
                else:
                    vssl.append('null')
            elif line['type'] == 'str':
                if line['val'] is None:
                    vssl.append("null")
                else:
                    vssl.append("'{0}'".format(formatSQL(str(line['val']))))
            elif line['type'] == 'b64str':
                if line['val'] is None:
                    vssl.append("null")
                else:
                    vssl.append("'{0}'".format(b64encode(str(line['val']))))
            else:
                return None
        return ','.join(vssl)
    except:
        return None


def build_set_str(flist, setNull=False):
    """
    构建SQL set字符串用于update语句
    :param flist: 字段定义列表，格式见_build_flist的注释
    :param setNull: 是否将空值放入set串中，true则设置空值，false则跳过空值
    :return : string or None
    """
    try:
        vssl = []
        for line in flist:
            fnpre = "`{0}`".format(line['fn'])
            if 'val' not in line:
                line['val'] = None
            if line['type'] == 'int':
                if line['val'] is not None:
                    if type(line['val']) == type(''):
                        if not is_number(line['val']):
                            return None
                    vssl.append(fnpre+"="+str(int(line['val'])))
                else:
                    if setNull:
                        vssl.append(fnpre+"=null")
            elif line['type'] == 'float':
                if line['val'] is not None:
                    if type(line['val']) == type(''):
                        if not is_number(line['val']):
                            return None
                    vssl.append(fnpre+"="+str(float(line['val'])))
                else:
                    if setNull:
                        vssl.append(fnpre+'=null')
            elif line['type'] == 'str':
                if line['val'] is None:
                    if setNull:
                        vssl.append(fnpre+"="+"null")
                else:
                    vssl.append(
                        fnpre+"='{0}'".format(formatSQL(str(line['val']))))
            elif line['type'] == 'b64str':
                if line['val'] is not None:
                    vssl.append(
                        fnpre+"='{0}'".format(b64encode(str(line['val']))))
                else:
                    if setNull:
                        vssl.append(fnpre+"="+"null")
            else:
                return None
        return ','.join(vssl)
    except:
        return None


def parse_datas(datas, flist, htmlp=True):
    """
    根据flist定义，从数据库查询结果中生成记录字典列表
    :param datas:   数据库查询结果
    :param flist:   field list
    :param htmlp:   转译html标签，False=不转译
    :return :       list,每个元素是一条记录，每条记录的格式为{'字段名1':val1,...}
                    flist错误会返回None
    """
    fcount = len(flist)
    res = []
    for line in datas:
        if len(line) != fcount:
            continue
        ld = {}
        for fi, fd in enumerate(flist):
            _fn = fd['fn']
            if 'as' in fd:
                _fn = fd['as']
            if fd['type'] == 'int':
                if line[fi] is None:
                    ld[_fn] = None
                elif type(line[fi]) == type('') and is_number(line[fi]):
                    ld[_fn] = int(line[fi])
                else:
                    ld[_fn] = int(line[fi])
            elif fd['type'] == 'float':
                if line[fi] is None:
                    ld[_fn] = None
                elif type(line[fi]) == type('') and is_number(line[fi]):
                    ld[_fn] = float(line[fi])
                else:
                    ld[_fn] = float(line[fi])
            elif fd['type'] == 'str':
                if line[fi] is None:
                    ld[_fn] = None
                else:
                    if htmlp:
                        ld[_fn] = formatHTML(str(line[fi]))
                    else:
                        ld[_fn] = str(line[fi])
            elif fd['type'] == 'b64str':
                if line[fi] is None:
                    ld[_fn] = None
                else:
                    if htmlp:
                        ld[_fn] = formatHTML(b64decode(line[fi]))
                    else:
                        ld[_fn] = b64decode(line[fi])
            else:
                return None
        res.append(ld)
    return res


def _get_value_key_val(flist, chkfn):
    '''
    get key value: (flist[x]['fn']==chkfn)
    return None or formated sql str
    '''
    resstr = None
    for line in flist:
        if line['fn'] == chkfn:
            resstr = build_field_str([line])
    return resstr


def insert_if_not_exists(cur, tbn, flist, chkfn='id', logger=None):
    '''
    向数据库插入数据，使用utf8编码
    注意，仅插入数据，不commit，调用后要注意是否需要commit
    :param cur:     数据库游标
    :param tbn:     表名
    :param flist:   field list，格式见_build_flist的注释
    :param chkfn:   唯一值约束字段名，默认id字段，None=不检查
    :param logger:  出错的话记录错误的logger，None=仅控制台输出
    :return :       dict，统一格式，若数据库错误，错误码为10
    '''
    # build sql
    istr = "insert into `{tbn}`({0}) select {1} from dual {estr};"
    kstr = build_field_str(flist)
    vstr = build_values_str(flist)
    if vstr is None or kstr is None:
        return {'code': 40, 'msg': 'parameters error', 'count': 0, 'data': []}
    estr = ''
    if type(chkfn) == type(''):
        estr = "where not exists (select 1 from `{tbn}` where `{chkfn}`={kval})"
        kval = _get_value_key_val(flist, chkfn)
        if kval is None:
            return {'code': 40, 'msg': 'parameters error', 'count': 0, 'data': []}
        estr = estr.format(tbn=tbn, chkfn=chkfn, kval=kval)
    sqlstr = istr.format(kstr, vstr, tbn=tbn, estr=estr)
    #Debug
    #logger.info("Debug insert SQL...")
    #logger.info(sqlstr)
    
    # insert
    try:
        cur.execute("SET NAMES UTF8;")
        cur.execute(sqlstr.encode("utf-8", "ignore"))
        return {'code': 0, 'msg': '', "count": 0, 'data': []}
    except:
        estr = traceback.format_exc()
        if logger is None:
            print(estr)
        else:
            logger.error("database error!\n" + estr)
        return {'code': 10, 'msg': 'database error', "count": 0, 'data': []}
    return {'code': -1, 'msg': 'unknown error', "count": 0, 'data': []}


def get_datas_status_search(cur, tbn, fstr, flist, page=0, limit=0, wstr='', logger=None, htmlp=True):
    
    # build string
    sqlstr = 'select {fstr} from {tbn} {wstr} {sstr} {lstr};'
    sqlstr_c = 'select count(1) from {tbn} {wstr};'.format(
        tbn=tbn, wstr=wstr)
    lstr = ''
    if page is not None and limit is not None and limit > 0:
        if page < 0:
            page = 0
        lstr = 'limit {0},{1}'.format(str(page*limit), str(limit))
    sstr = ''
    #remove sorted fields
    """for fd in flist:
        if 'sorted' in fd:
            sstr = 'order by `{0}`'.format(fd['fn'])
            if fd['sorted'] == 1:
                sstr = sstr + ' desc'"""
    sqlstr1 = sqlstr.format(
        fstr=fstr,
        tbn=tbn,
        wstr=wstr,
        sstr=sstr,
        lstr=lstr
    )
    #Debug
    logger.info("Debug SQL...")
    logger.info(sqlstr_c)
    logger.info(sqlstr1)
    
    # query
    try:
        cur.execute("SET NAMES UTF8;")
        # get count
        cur.execute(sqlstr_c.encode("utf-8", "ignore"))
        res_c = cur.fetchall()
        if res_c is None or len(res_c) == 0:
            return {'code': 10, 'msg': 'database error', "count": 0, 'data': []}
        count = int(res_c[0][0])
        # get datas
        print("DEBUG SQL ...")
        print(sqlstr1)
        cur.execute(sqlstr1.encode("utf-8", "ignore"))
        res = cur.fetchall()
        if res is None:
            return {'code': 10, 'msg': 'database error', "count": 0, 'data': []}
        data = parse_datas(res, flist, htmlp=htmlp)
        if data is not None:
            return {'code': 0, 'msg': '', "count": count, 'data': data}
        return {'code': 40, 'msg': 'parameters error', 'count': 0, 'data': []}
    except:
        estr = traceback.format_exc()
        if logger is None:
            print(estr)
        else:
            logger.error("database error!\n" + estr)
        return {'code': 10, 'msg': 'database error', "count": 0, 'data': []}
    return {'code': -1, 'msg': 'unknown error', "count": 0, 'data': []}


def get_datas(cur, tbn, flist, page=0, limit=0, wstr='', logger=None, htmlp=True):
    """
    从数据库获取信息，使用utf8编码
    :param cur:     数据库游标
    :param tbn:     表名
    :param flist:   field list，格式见_build_flist的注释
    :param page:    页码,0 based
    :param limit:   每页数量，设为0时，不限，直接返回所有数据
    :param wstr:    SQL语句的where xxx
    :param logger:  出错的话记录错误的logger，None=仅控制台输出
    :param htmlp:   转译html标签，False=不转译
    :return :       dict，统一格式，若数据库错误，错误码为10
    """
    # build string
    sqlstr = 'select {fstr} from `{tbn}` {wstr} {sstr} {lstr};'
    sqlstr_c = 'select count(1) from `{tbn}` {wstr};'.format(
        tbn=tbn, wstr=wstr)
    fstr = build_field_str(flist)
    lstr = ''
    if page is not None and limit is not None and limit > 0:
        if page < 0:
            page = 0
        lstr = 'limit {0},{1}'.format(str(page*limit), str(limit))
    sstr = ''
    for fd in flist:
        if 'sorted' in fd:
            sstr = 'order by `{0}`'.format(fd['fn'])
            if fd['sorted'] == 1:
                sstr = sstr + ' desc'
    sqlstr1 = sqlstr.format(
        fstr=fstr,
        tbn=tbn,
        wstr=wstr,
        sstr=sstr,
        lstr=lstr
    )
    #Debug
    #logger.info("Debug SQL...")
    #logger.info(sqlstr_c)
    #logger.info(sqlstr1)
    
    # query
    try:
        cur.execute("SET NAMES UTF8;")
        # get count
        cur.execute(sqlstr_c.encode("utf-8", "ignore"))
        res_c = cur.fetchall()
        if res_c is None or len(res_c) == 0:
            return {'code': 10, 'msg': 'database error', "count": 0, 'data': []}
        count = int(res_c[0][0])
        # get datas
        print("Debug SQL...")
        print(sqlstr1)
        cur.execute(sqlstr1.encode("utf-8", "ignore"))
        res = cur.fetchall()
        if res is None:
            return {'code': 10, 'msg': 'database error', "count": 0, 'data': []}
        data = parse_datas(res, flist, htmlp=htmlp)
        if data is not None:
            return {'code': 0, 'msg': '', "count": count, 'data': data}
        return {'code': 40, 'msg': 'parameters error', 'count': 0, 'data': []}
    except:
        estr = traceback.format_exc()
        if logger is None:
            print(estr)
        else:
            logger.error("database error!\n" + estr)
        return {'code': 10, 'msg': 'database error', "count": 0, 'data': []}
    return {'code': -1, 'msg': 'unknown error', "count": 0, 'data': []}


def get_datas_status(cur, tbn, flist, page=0, limit=0, wstr='', logger=None, htmlp=True):
    """
    从数据库获取信息，使用utf8编码
    :param cur:     数据库游标
    :param tbn:     表名
    :param flist:   field list，格式见_build_flist的注释
    :param page:    页码,0 based
    :param limit:   每页数量，设为0时，不限，直接返回所有数据
    :param wstr:    SQL语句的where xxx
    :param logger:  出错的话记录错误的logger，None=仅控制台输出
    :param htmlp:   转译html标签，False=不转译
    :return :       dict，统一格式，若数据库错误，错误码为10
    
    with remark : 
    :diaper
        sqlstr = 'select t.`id`,`child_no`,`time`,`diaper_id`,`diaper_status_id`,`staff`,`count`,`remark` \
                from `diaper` t LEFT JOIN `diaper_status` sub \
                ON t.`id` = sub.`id` \
                INNER JOIN `child` c ON c.`id` = t.`child_id` {wstr} {sstr} {lstr};'
    
    :skin'
        sqlstr = 'select t.`id`,`child_no`,`time`,`condition_id`,`position_id`,`position_detail`,`remark` \
                `staff`,`count`,`remark` from `skin` t LEFT JOIN `skin_position` sub \
                ON t.`id` = sub.`id` \
                INNER JOIN `child` c ON c.`id` = t.`child_id` {wstr} {sstr} {lstr};'

    """
    # build string
    # sqlstr = 'select {fstr} from `{tbn}` {wstr} {sstr} {lstr};'
    if tbn == 'diaper':
        sqlstr = 'select t.`id`,`child_no`,`name`,`name_chi`,`time`,`diaper_id`,`diaper_status_id`,`staff`,`count`,`remark` \
                from `diaper` t LEFT JOIN `diaper_status` sub \
                ON t.`id` = sub.`id` \
                INNER JOIN `child` c ON c.`id` = t.`child_id` {wstr} {sstr} {lstr};'
    
    elif tbn == 'skin':
        sqlstr = 'select t.`id`,`child_no`,`name`,`name_chi`,`time`,`condition_id`,`position_id`,`position_detail`, \
                `staff`,`count`,`remark` from `skin` t LEFT JOIN `skin_position` sub \
                ON t.`id` = sub.`id` \
                INNER JOIN `child` c ON c.`id` = t.`child_id` {wstr} {sstr} {lstr};'
    
    else:
        sqlstr = 'select t.{fstr} from `{tbn}` t \
        INNER JOIN `child` c ON c.`id` = t.`child_id` {wstr} {sstr} {lstr};'
    
    sqlstr_c = 'select count(1) from `{tbn}` {wstr};'.format(tbn=tbn, wstr=wstr)
    fstr = build_field_str(flist)
    lstr = ''
    if page is not None and limit is not None and limit > 0:
        if page < 0:
            page = 0
        lstr = 'limit {0},{1}'.format(str(page*limit), str(limit))
    sstr = ''
    for fd in flist:
        if 'sorted' in fd:
            sstr = 'order by `{0}`'.format(fd['fn'])
            if fd['sorted'] == 1:
                sstr = sstr + ' desc'

    sqlstr1 = sqlstr.format(
        fstr=fstr,
        tbn=tbn,
        wstr=wstr,
        sstr=sstr,
        lstr=lstr
    )
    
    #Debug
    #if(tbn == "skin"):
    #logger.info(tbn)
    #logger.info(flist)
    logger.info("Debug SQL...")
    logger.info(sqlstr_c)
    logger.info(sqlstr1)
    
    # query
    try:
        cur.execute("SET NAMES UTF8;")
        # get count
        cur.execute(sqlstr_c.encode("utf-8", "ignore"))
        res_c = cur.fetchall()
        if res_c is None or len(res_c) == 0:
            return {'code': 10, 'msg': 'database error', "count": 0, 'data': []}
        count = int(res_c[0][0])
        # get datas
        cur.execute(sqlstr1.encode("utf-8", "ignore"))
        res = cur.fetchall()
        #Debug
        #if(tbn == "skin"):
        #    logger.info(res)
        if res is None:
            return {'code': 10, 'msg': 'database error', "count": 0, 'data': []}
        
        #logger.info("DEBUG RES")
        #logger.info(res)
        #logger.info(flist)
        
        data = parse_datas(res, flist, htmlp=htmlp)
        
        #Debug
        #logger.info(data)
        
        if data is not None:
            return {'code': 0, 'msg': '', "count": count, 'data': data}
        return {'code': 40, 'msg': 'parameters error', 'count': 0, 'data': []}
    except:
        estr = traceback.format_exc()
        if logger is None:
            print(estr)
        else:
            logger.error("database error!\n" + estr)
        return {'code': 10, 'msg': 'database error', "count": 0, 'data': []}
    return {'code': -1, 'msg': 'unknown error', "count": 0, 'data': []}

# tools-----------------------------------------------

def get_datas_status_with_name(cur, tbn, flist, page=0, limit=0, wstr='', logger=None, htmlp=True):
    """
    从数据库获取信息，使用utf8编码
    :param cur:     数据库游标
    :param tbn:     表名
    :param flist:   field list，格式见_build_flist的注释
    :param page:    页码,0 based
    :param limit:   每页数量，设为0时，不限，直接返回所有数据
    :param wstr:    SQL语句的where xxx
    :param logger:  出错的话记录错误的logger，None=仅控制台输出
    :param htmlp:   转译html标签，False=不转译
    :return :       dict，统一格式，若数据库错误，错误码为10
    
    with remark : 
    :diaper
        sqlstr = 'select FROM_BASE64(c.`name_chi`),c.`name`,t.`id`,`child_no`,`time`,`diaper_id`,`diaper_status_id`,`staff`,`count`,`remark` \
                from `diaper` t LEFT JOIN `diaper_status` sub \
                ON t.`id` = sub.`id` \
                INNER JOIN `child` c ON c.`id` = t.`child_id` {wstr} {sstr} {lstr};'
    
    :skin'
        sqlstr = 'select FROM_BASE64(c.`name_chi`),c.`name`,t.`id`,`child_no`,`time`,`condition_id`,`position_id`,`position_detail`,`remark` \
                `staff`,`count` from `skin` t LEFT JOIN `skin_position` sub \
                ON t.`id` = sub.`id` \
                INNER JOIN `child` c ON c.`id` = t.`child_id` {wstr} {sstr} {lstr};'

    """
    # build string
    # sqlstr = 'select {fstr} from `{tbn}` {wstr} {sstr} {lstr};'
    if tbn == 'diaper':
        sqlstr = 'select t.`id`,`child_no`,`name`,`name_chi`,`time`,`diaper_id`,`diaper_status_id`,`staff`,`count`,`remark` \
                from `diaper` t LEFT JOIN `diaper_status` sub \
                ON t.`id` = sub.`id` \
                INNER JOIN `child` c ON c.`id` = t.`child_id` {wstr} {sstr} {lstr};'
    
    elif tbn == 'skin':
        sqlstr = 'select t.`id`,`child_no`,`name`,`name_chi`,`time`,`condition_id`,`position_id`,`position_detail`,`remark` \
                `staff`,`count`,`remark` from `skin` t LEFT JOIN `skin_position` sub \
                ON t.`id` = sub.`id` \
                INNER JOIN `child` c ON c.`id` = t.`child_id` {wstr} {sstr} {lstr};'
    
    else:
        sqlstr = 'select t.{fstr} from `{tbn}` t \
        INNER JOIN `child` c ON c.`id` = t.`child_id` {wstr} {sstr} {lstr};'
    
    sqlstr_c = 'select count(1) from `{tbn}` {wstr};'.format(tbn=tbn, wstr=wstr)
    fstr = build_field_str(flist)
    lstr = ''
    if page is not None and limit is not None and limit > 0:
        if page < 0:
            page = 0
        lstr = 'limit {0},{1}'.format(str(page*limit), str(limit))
    sstr = ''
    for fd in flist:
        if 'sorted' in fd:
            sstr = 'order by `{0}`'.format(fd['fn'])
            if fd['sorted'] == 1:
                sstr = sstr + ' desc'

    sqlstr1 = sqlstr.format(
        fstr=fstr,
        tbn=tbn,
        wstr=wstr,
        sstr=sstr,
        lstr=lstr
    )
    
    #Debug
    #if(tbn == "skin"):
    #logger.info(tbn)
    #logger.info(flist)
    #logger.info("Debug SQL...")
    #logger.info(sqlstr_c)
    #logger.info(sqlstr1)
    print("Debug SQL... : ")
    print(sqlstr1)
    
    # query
    try:
        cur.execute("SET NAMES UTF8;")
        # get count
        cur.execute(sqlstr_c.encode("utf-8", "ignore"))
        res_c = cur.fetchall()
        if res_c is None or len(res_c) == 0:
            return {'code': 10, 'msg': 'database error', "count": 0, 'data': []}
        count = int(res_c[0][0])
        # get datas
        cur.execute(sqlstr1.encode("utf-8", "ignore"))
        res = cur.fetchall()
        #Debug
        #if(tbn == "skin"):
        #    logger.info(res)
        if res is None:
            return {'code': 10, 'msg': 'database error', "count": 0, 'data': []}
            
        #name_chi_dict = {'fn': 'FROM_BASE64(c.name_chi)', 'type': 'str', 'as': 'name_chi'}
        #name_dict = {'fn': 'c.name', 'type': 'str', 'as': 'name'}
        #flist.insert(0,name_chi_dict)
        #flist.insert(1,name_dict)    
        data = parse_datas(res, flist, htmlp=htmlp)
        #Debug
        #if(tbn == "skin"):
        #    logger.info(data)
        
        if data is not None:
            return {'code': 0, 'msg': '', "count": count, 'data': data}
        return {'code': 40, 'msg': 'parameters error', 'count': 0, 'data': []}
    except:
        estr = traceback.format_exc()
        if logger is None:
            print(estr)
        else:
            logger.error("database error!\n" + estr)
        return {'code': 10, 'msg': 'database error', "count": 0, 'data': []}
    return {'code': -1, 'msg': 'unknown error', "count": 0, 'data': []}

def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        pass

    try:
        import unicodedata
        unicodedata.numeric(s)
        return True
    except (TypeError, ValueError):
        pass

    return False


def formatSQL(sqlstr):
    """
        format sql string
    """
    sqlstr = sqlstr.replace("'", "''")
    sqlstr = sqlstr.replace("\\", "\\\\")
    return sqlstr


def formatHTML(htmlstr):
    """
    format HTML string to avoid XSS attack
    """
    resstr = htmlstr.replace('<', '&lt;')
    resstr = resstr.replace('>', '&gt;')
    resstr = resstr.replace("'", '&#039;')
    resstr = resstr.replace('"', '&quot;')
    return resstr


def buildLogger(newlogger, logfn, istocon, logname=__name__):
    """
    配置log, 定义log
    :param newlogger:   待设定的logger，如果为
                        空，则会返回新建的logger
    :param logfn:   log文件名，空则不输出到文件
    :param istocon: 是否输出到控制台，true=输出
    :param logname: logger的名字，只影响新建的logger
    :retrun:    a logger
    """
    reslogger = newlogger
    if newlogger is None:
        reslogger = logging.getLogger(logname)
        reslogger.setLevel(level=logging.INFO)
    if logfn is not None and logfn != "":
        handler = logging.FileHandler(logfn)
        handler.setLevel(logging.INFO)
        formatter1 = logging.Formatter(
            '[%(asctime)s][%(levelname)s]\
[%(filename)s,%(lineno)d,%(funcName)s]%(message)s'
        )
        handler.setFormatter(formatter1)
        reslogger.addHandler(handler)

    if istocon:
        console = logging.StreamHandler()
        console.setLevel(logging.INFO)
        formatter2 = logging.Formatter(
            '[%(asctime)s][%(levelname)s][%(filename)s,%(lineno)d]%(message)s')
        console.setFormatter(formatter2)
        reslogger.addHandler(console)

    return reslogger


def mkdir(dirname):
    """
        if dirname is not exists, make this dir
    """
    # create output dir
    if not os.path.exists(dirname):
        print("[INFO ]Create dir \"" + dirname + "\"!")
        os.mkdir(dirname)


def sort_by_value(keys, values, threshold, limit=0):
    """
        sort_by_value
        Parameters:
            keys:       <list>  a list of keys
            values:     <list>  values of keys
            threshold:  <float> é˜ˆå€¼
            limit:      <int>   max number of output list, 0 for unlimited
        Return:
            sorted list like [[key, value]...]
    """
    backitems = []
    for i in range(len(keys)):
        backitems.append([values[i], keys[i]])
    backitems.sort(reverse=True)
    imax = limit
    if limit == 0 or limit > len(backitems):
        imax = len(backitems)
    res = []
    for i in range(imax):
        if backitems[i][0] < threshold:
            break
        res.append([backitems[i][1], backitems[i][0]])
    return res
