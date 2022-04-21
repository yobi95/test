#!/usr/bin/env python3
# -*- coding:utf-8 -*-
"""
準備一些環境

以main運行，將：
    讀取設定檔
    構建必要的資料庫和錶結構
    存入管理員用戶配寘
    存入初始化數據
    對應的配寘、增改數據等請參照注釋調整常數定義

關於資料檔案：
    資料檔案必須按格式書寫
    數據檔案格式要求：
    1. csv格式，對應表的每個欄位都需要體現，即使該欄位沒有值，也應該留空
    2.數據以英文分號分隔，無文本標記
    3.資料檔案不包含標題
    3.例：1;1;2;;5;1
    關於初始化清單：
        定義在常數datas中，格式示例：
        datas = {
            "room": {"fn":"room.txt", "parser":initRoom}
        }
    對應含義：
        datas = {
            "錶名": {"fn":"數據檔名", "parser":處理函數名}
        }
關於處理函數：
    按初始化清單定義調用處理函數，無返回值，參數列表如下：
    :param datafn:      數據檔名（全路徑）
    :param tablename:   錶名
    :param cur:         數據庫遊標
    :param clear:       是否先清空原有數據，True=清空原數據
    :param logger:      logger
"""
import configparser
import logging
import os

import MySQLdb

import funcs

# 一些常量--------------------------------------------------
manager_role = 'admin'
configfn = "config.conf"
logfn = "logs/main.log"
# 数据库表列表
tables = [
    'user',
    'staff',
    'child',
    'files',
    'parent',
    'group',
    'temperature',
    'skin',
    'va_condition_id',
    'va_position_id',
    'va_position_detail',
    'diaper',
    'va_diaper_id',
    'va_diaper_status_id',
    'meal',
    'va_meal_id',
    'va_qty_unit',
    'nap',
    'va_nap_id',
    'va_napquality_id',
    'health',
    'va_health_id',
    'va_health_status_id',
    'perform',
    'va_perform_id',
    'diaper_status',
    'skin_position'
]
# 初始化数据
# 从数据文件读取数据并插入数据库中
datadir = "data"
datas = {}

datas = {
    "va_condition_id": {"fn": "va_condition_id.txt", "parser": "initStatus"},
    "va_diaper_id": {"fn": "va_diaper_id.txt", "parser": "initStatus"},
    "va_diaper_status_id": {"fn": "va_diaper_status_id.txt", "parser": "initStatus"},
    "va_health_id": {"fn": "va_health_id.txt", "parser": "initStatus"},
    "va_health_status_id": {"fn": "va_health_status_id.txt", "parser": "initStatus"},
    "va_meal_id": {"fn": "va_meal_id.txt", "parser": "initStatus"},
    "va_qty_unit": {"fn": "va_qty_unit.txt", "parser": "initStatus"},
    "va_nap_id": {"fn": "va_nap_id.txt", "parser": "initStatus"},
    "va_napquality_id": {"fn": "va_napquality_id.txt", "parser": "initStatus"},
    "va_perform_id": {"fn": "va_perform_id.txt", "parser": "initStatus"},
    "va_position_id": {"fn": "va_position_id.txt", "parser": "initStatus"},
    "va_position_detail": {"fn": "va_position_detail.txt", "parser": "initStatus"},
    "group": {"fn": "group.txt", "parser": "initGroup"}
}

# 建库sql文件名
sqlfn = "build.sql"

# 字段名稱對應，用於相似結構的status系列表的初始化
tbn_fn = {
    "va_condition_id": {'f1': 'value', 'f2': 'value_chi'},
    "va_diaper_id": {'f1': 'value', 'f2': 'value_chi'},
    "va_diaper_status_id": {'f1': 'value', 'f2': 'value_chi'},
    "va_health_id": {'f1': 'value', 'f2': 'value_chi'},
    "va_health_status_id": {'f1': 'value', 'f2': 'value_chi'},
    "va_meal_id": {'f1': 'value', 'f2': 'value_chi'},
    "va_qty_unit": {'f1': 'value', 'f2': 'value_chi'},
    "va_nap_id": {'f1': 'value', 'f2': 'value_chi'},
    "va_napquality_id": {'f1': 'value', 'f2': 'value_chi'},
    "va_perform_id": {'f1': 'value', 'f2': 'value_chi'},
    "va_position_id": {'f1': 'value', 'f2': 'value_chi'},
    "va_position_detail": {'f1': 'value', 'f2': 'value_chi'}
}

# functions--------------------------------------------


def initDB(logger):
    """
    init database
    """
    config = configparser.ConfigParser()
    config.read(configfn, encoding='utf-8')
    # database info
    _dbconf = \
        {
            "user": config.get("database", "user"),
            "passwd": config.get("database", "passwd"),
            "host": config.get("database", "host"),
            "port": config.getint("database", "port"),
            "db": config.get("database", "db")
        }
    logger.info("Testing database...")
    logger.info(config.get("database", "user"))
    logger.info(config.get("database", "passwd"))
    logger.info(config.get("database", "host"))
    logger.info(config.getint("database", "port"))
    logger.info(config.get("database", "db"))
    conn = MySQLdb.connect(**_dbconf)
    conn.autocommit(True)
    cur = conn.cursor()
    cur.execute("SET NAMES UTF8;")
    # test if database is exist
    cur.execute("show databases;")
    dbs = cur.fetchall()
    dbs = set([i[0].lower() for i in dbs])
    dbn = config.get("database", "db")
    if not dbn in dbs:
        logger.info("Building database "+dbn+"...")
        cur.execute(
            "CREATE SCHEMA `{dbname}` DEFAULT CHARACTER SET utf8 ;".format(dbname=dbn))
    # test if tables is exist
    cur.execute("use {dbname};".format(dbname=dbn))
    cur.execute("show tables;")
    tbs = cur.fetchall()
    if len(tbs) > 0:
        tbs = set([i[0].lower() for i in tbs])
    else:
        tbs = set()
    # check tables
    tablesok = True
    for t in tables:
        if t not in tbs:
            tablesok = False
    if not tablesok:
        logger.info("Building tables by build.sql ...")
        # build Database by build.sql - START  
        """ 
        sqlf = open(sqlfn, 'r', encoding="utf8")
        lines = sqlf.readlines()
        sqlf.close()
        sqlstr = "".join(lines)
        cur.execute(sqlstr.encode("utf-8", "ignore"))
        """ 
        # build Database by build.sql - END
        
        # init data
        # initData(datas, datadir, cur, True, logger)
    # init manager account
    initAdmin('admin.txt', 'user', cur, False, logger)

    cur.close()
    conn.close()
    logger.info("Database is OK!")


def initData(datadict, datadir, cur, clear, logger):
    """
    按初始化列表初始化数据
    """
    for k, v in datadict.items():
        eval(v["parser"])(datadir+"/"+v["fn"], k, cur, clear, logger)


def _readlines(datafn, logger):
    if not os.path.exists(datafn):
        logger.error("Data file {fn} not exists!".format(fn=datafn))
        return None
    f = open(datafn, 'r', encoding='utf-8')
    lines = f.readlines()
    f.close()
    res = []
    nolist = set(["", " ", "\n", "\r\n", " \n", " \r\n"])
    for line in lines[1:]:
        if line is not None and line not in nolist:
            # 除行尾换行
            tl = line
            tl = tl.strip('\n')
            tl = tl.strip('\r')
            tl = tl.strip(' ')
            # 分割
            res.append(tl.split(";"))
    return res


def initAdmin(datafn, tablename, cur, clear, logger):
    """
    读取data文件并初始化数据库中的对应表
    变量定义见模块注释
    """
    logger.info("Start init admin.")
    lines = _readlines(datafn, logger)
    if lines is None or len(lines) == 0:
        logger.error("End init admin.")
        return
    sqlstr1 = "insert into `user`(id,`username`,`passwdmd5`,email,role)" \
        " values({4},'{0}','{1}','{2}','{3}');"
    sqlstr2 = "update `user` set " \
        " `username`='{0}'," \
        " passwdmd5='{1}'," \
        " email='{2}'," \
        " role='{3}'" \
        " where `username`='{0}' and role='admin';"
    chksql = "select id from `user` where `username`='{0}';"
    warnstr = "Admin account '{0}' defined in admin.txt exists!"
    for line in lines:
        if len(line) != 3:
            continue
        # 判断管理员账号是否已存在，选定账号
        sqlstr = ''
        musern = funcs.b64encode(line[0])
        chksqlstr = chksql.format(musern)
        # print(chksqlstr)
        cur.execute(chksqlstr.encode("utf-8", "ignore"))
        munids = cur.fetchall()
        if len(munids) > 0:
            logger.warning(warnstr.format(line[0]))
            sqlstr = sqlstr2
        else:
            sqlstr = sqlstr1
        # get md5 of passwd
        tpwmd5 = funcs.get_md5(line[1])
        # insert
        sqlstr3 = sqlstr.format(
            funcs.b64encode(line[0]),
            tpwmd5,
            funcs.b64encode(line[2]),
            'admin',
            funcs.get_random_int64()
        )
        # print(sqlstr2)
        cur.execute(sqlstr3.encode("utf-8", "ignore"))
    logger.info("End init admin.")


def initUser(datafn, tablename, cur, clear, logger):
    """
    读取data文件并初始化数据库中的对应表
    变量定义见模块注释
    """
    logger.info("Start init user.")
    lines = _readlines(datafn, logger)
    if lines is None or len(lines) == 0:
        logger.error("End init user.")
        return
    sqlstr1 = "insert into `user`(`username`,`passwdmd5`,email,role)" \
        " values('{0}','{1}','{2}','{3}');"
    chksql = "select id from `user` where `username`='{0}';"
    warnstr = "User account '{0}' defined in user.txt exists!"
    for line in lines:
        if len(line) != 4:
            continue
        # 判断管理员账号是否已存在，选定账号
        sqlstr = ''
        musern = funcs.b64encode(line[0])
        chksqlstr = chksql.format(musern)
        # print(chksqlstr)
        cur.execute(chksqlstr.encode("utf-8", "ignore"))
        munids = cur.fetchall()
        if len(munids) > 0:
            logger.warning(warnstr.format(line[0]))
            continue
        else:
            sqlstr = sqlstr1
        # get md5 of passwd
        tpwmd5 = funcs.get_md5(line[1])
        # insert
        sqlstr3 = sqlstr.format(
            funcs.b64encode(line[0]),
            tpwmd5,
            funcs.b64encode(line[2]),
            funcs.formatSQL(line[3]),
        )
        # print(sqlstr2)
        cur.execute(sqlstr3.encode("utf-8", "ignore"))
        # get id
        cur.execute(('select id from `user` where `username`=\''+funcs.b64encode(line[0])+'\';').encode("utf-8", "ignore"))
        uid = cur.fetchall()[0][0]
        # insert info
        cur.execute(('insert into '+funcs.formatSQL(line[3])+'(id,`name`) values('+str(uid)+',\''+funcs.b64encode('name'+str(uid))+'\');').encode("utf-8", "ignore"))

    logger.info("End init user.")


def initStatus(datafn, tablename, cur, clear, logger):
    """
    读取data文件并初始化数据库中的对应表
    变量定义见模块注释
    """
    _initStatus(datafn, tablename,
                cur, clear, logger,
                tbn_fn[tablename]['f1'],
                tbn_fn[tablename]['f2'])


def _initStatus(datafn, tablename, cur, clear, logger, f1, f2):
    """
    读取data文件并初始化数据库中的对应表
    变量定义见模块注释
    :param f1:  字段1名稱
    :param f2:  字段2名稱
    """
    logger.info("Start init "+tablename+".")
    
    lines = _readlines(datafn, logger)
    
    if lines is None or len(lines) == 0:
        logger.error("End init "+tablename+".")
        return
    # clear

    if clear:
        sqlstr = "delete from `{tbn}`;".format(tbn=tablename)
        cur.execute(sqlstr.encode("utf-8", "ignore"))
    
    sqlstr1 = "insert into `{tbn}`(`id`,`{f1}`,`{f2}`)" \
        " values({0},'{1}','{2}');"
        
    #Debug 1/4/2020
    #logger.info(sqlstr1);
    for line in lines:
        if len(line) != 3:
            continue
        sqlstr = sqlstr1.format(
            line[0],
            funcs.formatSQL(line[1]),
            funcs.b64encode(line[2]),
            tbn=tablename,
            f1=f1,
            f2=f2
        )
        cur.execute(sqlstr.encode("utf-8", "ignore"))


def initGroup(datafn, tablename, cur, clear, logger):
    """
    """
    logger.info("Start init "+tablename+".")
    lines = _readlines(datafn, logger)
    if lines is None or len(lines) == 0:
        logger.error("End init "+tablename+".")
        return
    # clear
    if clear:
        sqlstr = "delete from `{tbn}`;".format(tbn=tablename)
        cur.execute(sqlstr.encode("utf-8", "ignore"))
    sqlstr1 = "insert into `{tbn}`(`id`,`{f1}`,`{f2}`,`{f3}`)" \
        " values({0},{1},{2},'{3}');"
    for line in lines:
        if len(line) != 4:
            continue
        sqlstr = sqlstr1.format(
            line[0],
            line[1],
            line[2],
            funcs.formatSQL(line[3]),
            tbn=tablename, f1='smon', f2='emon', f3='name'
        )
        cur.execute(sqlstr.encode("utf-8", "ignore"))


if __name__ == "__main__":
    config = configparser.ConfigParser()
    config.read(configfn)
    logger = funcs.buildLogger(None, logfn, True, "initDB")
    initDB(logger)
