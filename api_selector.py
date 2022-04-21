#!/usr/bin/env python3
# -*- coding:utf-8 -*-
"""
select API蓝图
定义蓝图api_selector，实现selector相关操作蓝图
用於返回預定義常量
视图含义见对应api文档
"""
import traceback

from flask import Blueprint, request
import time
import datetime

import funcs
import global_var as gv
from global_var import enum_error as ee

# 定义蓝图-------------------------------------------------
api_selector = Blueprint(
    'api_selector',
    __name__,
    template_folder='templates'
)

# functions--------------------------------------------

def get_selectors(name):
    resdata = gv.enum_selector[name].values()
    resdata = sorted(resdata, key=lambda x: x['id'])
    res = ee.NORMAL()
    res['data'] = resdata
    res['count'] = len(resdata)
    return res

# views------------------------------------------------

@api_selector.route('/api/group', methods=['GET'])
def get_group_selector():
    res = ee.NORMAL()
    res['data'] = gv.groups
    res['count'] = len(res['data'])
    return res

@api_selector.route('/api/va_condition_id', methods=['GET'])
def get_va_condition_id_selector():
    return get_selectors('va_condition_id')

@api_selector.route('/api/va_diaper_id', methods=['GET'])
def get_va_diaper_id_selector():
    return get_selectors('va_diaper_id')

@api_selector.route('/api/va_diaper_status', methods=['GET'])
def get_va_diaper_status_selector():
    return get_selectors('va_diaper_status')
    
@api_selector.route('/api/va_health_id', methods=['GET'])
def get_va_health_id_selector():
    return get_selectors('va_health_id')

@api_selector.route('/api/va_health_status_id', methods=['GET'])
def get_va_health_status_id_selector():
    return get_selectors('va_health_status_id')

@api_selector.route('/api/va_meal_id', methods=['GET'])
def get_va_meal_id_selector():
    return get_selectors('va_meal_id')

@api_selector.route('/api/va_qty_unit', methods=['GET'])
def get_va_qty_unit_selector():
    return get_selectors('va_qty_unit')

@api_selector.route('/api/va_nap_id', methods=['GET'])
def get_va_nap_id_selector():
    return get_selectors('va_nap_id')

@api_selector.route('/api/va_perform_detail', methods=['GET'])
def get_va_perform_detail_selector():
    return get_selectors('va_perform_detail')

@api_selector.route('/api/va_napquality_id', methods=['GET'])
def get_va_napquality_id_selector():
    return get_selectors('va_napquality_id')

@api_selector.route('/api/va_position_id', methods=['GET'])
def get_va_position_id_selector():
    return get_selectors('va_position_id')

@api_selector.route('/api/va_position_detail', methods=['GET'])
def get_va_position_detail_selector():
    return get_selectors('va_position_detail')