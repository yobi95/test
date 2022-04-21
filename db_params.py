#!/usr/bin/env python3
# -*- coding:utf-8 -*-
"""
定义数据库结构模板
"""
temperature = {
    'tbn' : 'temperature',
    'flist': [
        {'fn':'id', 'type':'int', 'as':'id'},
        {'fn':'child_no', 'type':'str', 'as':'child_no'},
        {'fn':'name', 'type':'str', 'as':'name'},
        {'fn':'name_chi', 'type':'b64str', 'as':'name_chi'},
        {'fn':'time', 'type':'str', 'as':'time'},
        {'fn':'temperature', 'type':'float', 'as':'status'},
        {'fn':'staff', 'type':'str', 'as':'staff'}
        #,{'fn':'count', 'type':'int', 'as':'count'}
    ]
}

skin = {
    'tbn' : 'skin',
    'flist': [
        {'fn':'id', 'type':'int', 'as':'id'},
        {'fn':'child_no', 'type':'str', 'as':'child_no'},
        {'fn':'name', 'type':'str', 'as':'name'},
        {'fn':'name_chi', 'type':'b64str', 'as':'name_chi'},
        {'fn':'time', 'type':'str', 'as':'time'},
        {'fn':'condition_id', 'type':'int', 'as':'status'},
        {'fn':'position_id', 'type':'int', 'as':'substatus'},
        {'fn':'position_detail', 'type':'int', 'as':'substatus_detail'},
        {'fn':'staff', 'type':'str', 'as':'staff'},
        {'fn':'count', 'type':'int', 'as':'count'},
        {'fn':'remark', 'type':'str', 'as':'remark'}
    ]
}

meal = {
    'tbn' : 'meal',
    'flist': [
        {'fn':'id', 'type':'int', 'as':'id'},
        {'fn':'child_no', 'type':'str', 'as':'child_no'},
        {'fn':'name', 'type':'str', 'as':'name'},
        {'fn':'name_chi', 'type':'b64str', 'as':'name_chi'},
        {'fn':'time', 'type':'str', 'as':'time'},
        {'fn':'meal_id', 'type':'int', 'as':'status'},
        {'fn':'qty', 'type':'str', 'as':'substatus'},
        {'fn':'qty_unit', 'type':'int', 'as':'substatus_detail'},
        {'fn':'staff', 'type':'str', 'as':'staff'},
        {'fn':'count', 'type':'int', 'as':'count'},
        {'fn':'remark', 'type':'str', 'as':'remark'}
    ]
}

nap = {
    'tbn' : 'nap',
    'flist': [
        {'fn':'id', 'type':'int', 'as':'id'},
        {'fn':'child_no', 'type':'str', 'as':'child_no'},
        {'fn':'name', 'type':'str', 'as':'name'},
        {'fn':'name_chi', 'type':'b64str', 'as':'name_chi'},
        {'fn':'time', 'type':'str', 'as':'time'},
        {'fn':'nap_id', 'type':'int', 'as':'status'},
        {'fn':'napquality_id', 'type':'int', 'as':'substatus'},
        {'fn':'staff', 'type':'str', 'as':'staff'},
        {'fn':'count', 'type':'int', 'as':'count'},
        {'fn':'remark', 'type':'str', 'as':'remark'}
    ]
}

diaper = {
    'tbn' : 'diaper',
    'flist': [
        {'fn':'id', 'type':'int', 'as':'id'},
        {'fn':'child_no', 'type':'str', 'as':'child_no'},
        {'fn':'name', 'type':'str', 'as':'name'},
        {'fn':'name_chi', 'type':'b64str', 'as':'name_chi'},
        {'fn':'time', 'type':'str', 'as':'time'},
        {'fn':'diaper_id', 'type':'int', 'as':'status'},
        {'fn':'diaper_status_id', 'type':'int', 'as':'substatus'},
        {'fn':'staff', 'type':'str', 'as':'staff'},
        {'fn':'count', 'type':'int', 'as':'count'},
        {'fn':'remark', 'type':'str', 'as':'remark'}
    ]
}


health = {
    'tbn' : 'health',
    'flist': [
        {'fn':'id', 'type':'int', 'as':'id'},
        {'fn':'child_no', 'type':'str', 'as':'child_no'},
        {'fn':'name', 'type':'str', 'as':'name'},
        {'fn':'name_chi', 'type':'b64str', 'as':'name_chi'},
        {'fn':'time', 'type':'str', 'as':'time'},
        {'fn':'health_id', 'type':'int', 'as':'status'},
        {'fn':'health_status_id', 'type':'int', 'as':'substatus'},
        {'fn':'staff', 'type':'str', 'as':'staff'},
        {'fn':'count', 'type':'int', 'as':'count'},
        {'fn':'remark', 'type':'str', 'as':'remark'}
    ]
}

perform = {
    'tbn' : 'perform',
    'flist': [
        {'fn':'id', 'type':'int', 'as':'id'},
        {'fn':'name', 'type':'str', 'as':'name'},
        {'fn':'name_chi', 'type':'b64str', 'as':'name_chi'},
        {'fn':'child_no', 'type':'str', 'as':'child_no'},
        {'fn':'time', 'type':'str', 'as':'time'},
        {'fn':'perform_id', 'type':'int', 'as':'status'},
        {'fn':'staff', 'type':'str', 'as':'staff'},
        {'fn':'count', 'type':'int', 'as':'count'},
        {'fn':'remark', 'type':'str', 'as':'remark'}
    ]
}

status_tables = {
    'temperature': temperature,
    'skin': skin,
    'meal': meal,
    'nap':nap,
    'diaper':diaper,
    'health':health,
    'perform':perform
}

status_type_tbn = {
    'skin':"va_condition_id",
    'diaper':"va_diaper_id",
    'health':"va_health_id",
    "meal":"va_meal_id",
    'nap':"va_nap_id",
    "perform":"va_perform_id"
}

substatus_type_tbn = {
    'skin' : "va_position_id",
    'diaper' : "va_diaper_status_id",
    'health' : "va_health_status_id",
    'meal' : "va_qty_unit",
    'nap' : "va_napquality_id"
}

substatus_detail_type_tbn = {
    'skin' : "va_position_detail"
}


def get_index(flist, fn):
    '''
    get index of fn in flist
    '''
    for i, v in enumerate(flist):
        if v['fn'] == fn:
            return i