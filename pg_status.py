#!/usr/bin/env python3
# -*- coding:utf-8 -*-
"""
status蓝图
定义蓝图pg_status，实现status相关页面蓝图
"""
from urllib import parse
import io
from flask import Blueprint, redirect, render_template, request, abort
import pandas as pd
import sys,time
import flask_excel as excel
import xlrd, os, xlwt
import funcs, base64
import global_var as gv
import pandas.io.sql as sql
from api_loginout import loggeduser, verify_auto
# 定义蓝图-------------------------------------------------
pg_status = Blueprint(
    'pg_status',
    __name__,
    template_folder='templates'
)

# views------------------------------------------------

@pg_status.route('/statuslist', methods=['GET'])
def statuslist_get():
    _un, _role = loggeduser(request)
    if _un is None:
        return redirect('/login')
    if _role == 'parent':
        return '<h1>No authority!</h1><p>Login as admin or staff please.</p>'
    return render_template('statuslist.html', loggeduser=_un)

@pg_status.route('/addstatus', methods=['GET'])
def addstatus_get():
    _un, _role = loggeduser(request)
    if _un is None:
        return redirect('/login')
    if _role == 'parent':
        return '<h1>No authority!</h1><p>Login as admin or staff please.</p>'
    _type = request.args.get('type')
    if _type is None:
        abort(404)
    return render_template('addstatus.html',type=_type,loggeduser=_un)
# explore excel views------------------------------------------------
    '''
data = xlrd.open_workbook(os.path.abspath('.')+'/photo/name.xlsx')
table = data.sheets()[0]
@pg_status.route('/export_excel', methods=['GET','POST'])
def export_excel(export):
 _un, _role = loggeduser(request)
 if _un is None:
        return redirect('/login')
 if _role == 'parent':
        return render_template('contactus.html', loggeduser=_un)
 if request.method == 'GET':
    conn = gv.dbpool.connection()
    cur = conn.cursor()
    conn.close()
    cur.close()
    pf = pd.DataFrame(list(export))
    order = ['diaper','health','meal','nap','perform']
    pf = pf[order]
    columns_map = {
      'diaper':'1',
      'health':'2',
      'meal':'3',
      'nap':'4',
      'perform':'5'
    }
    pf.rename(columns = columns_map,inplace = True)
    file_path = pd.ExcelWriter('name.xlsx')
    pf.fillna(' ',inplace = True)
    pf.to_excel(file_path,encoding = 'utf-8',index = False)
    file_path.save()
    return render_template('export_excel.html', loggeduser=_un)
if __name__ == '__main__':
    export_excel(table)
   '''
# explore excel other table type views------------------------------------------------
'''  
@pg_status.route('/export_excel', methods=['GET','POST'])
def export_excel2():
 _un, _role = loggeduser(request)
 if _un is None:
        return redirect('/login')
 if _role == 'parent':
        return render_template('contactus.html', loggeduser=_un)
 conn = gv.dbpool.connection()
 df=sql.read_sql('select * from va_meal_id',conn)
 df2=sql.read_sql('select * from va_diaper_id',conn)
 df3=sql.read_sql('select * from va_diaper_status_id',conn)
 df4=sql.read_sql('select * from va_health_id',conn)
 df5=sql.read_sql('select * from va_health_status_id',conn)
 df6=sql.read_sql('select * from va_meal_id',conn)
 df7=sql.read_sql('select * from va_qty_unit',conn)
 df8=sql.read_sql('select * from va_nap_id',conn)
 df9=sql.read_sql('select * from va_napquality_id',conn)
 df10=sql.read_sql('select * from va_perform_id',conn)
 df11=sql.read_sql('select * from va_position_id',conn)
 df12=sql.read_sql('select * from va_position_detail',conn)
 print(df2,df3,df4,df5,df6,df7,df8,df9,df10,df11,df12)
 df.to_excel('name.xlsx')
 return render_template('export_excel.html', loggeduser=_un)
 '''
 
# explore excel main table type views------------------------------------------------
@pg_status.route('/export_excel', methods=['GET','POST'])
def export_excel():
 _un, _role = loggeduser(request)
 if _un is None:
        return redirect('/login')
 if _role == 'parent':
        return render_template('contactus.html', loggeduser=_un)
 conn = gv.dbpool.connection()
 now = time.strftime("%Y-%m-%d-%H_%M_%S",time.localtime(time.time()))
 #get all day
 df1=sql.read_sql('select h.child_id as "Child ID",c.child_no as "Child Number", \
                  CONVERT(FROM_BASE64(c.name_chi),CHAR) as "Chinese Name",c.name as "English Name", \
                  CONVERT(FROM_BASE64(vhi.value_chi),CHAR) as "Health", \
                  CONVERT(FROM_BASE64(vhsi.value_chi),CHAR) as "Health Status", \
                  h.remark as "Remark",h.staff as "Staff",h.time as "Timestamp" from health h \
                  LEFT join child c on c.id = h.child_id \
                  LEFT Join va_health_id vhi on h. health_id = vhi.id \
                  LEFT Join va_health_status_id vhsi on h.health_status_id = vhsi.id \
                  ORDER BY h.child_id DESC',conn)
                  
 df2=sql.read_sql('Select m.child_id as "child ID",c.child_no as "Child Number", \
                   CONVERT(FROM_BASE64(c.name_chi),CHAR) as "Chinese Name",c.name as "English Name", \
                   CONVERT(FROM_BASE64(vmi.value_chi),CHAR) as "Meal Type", \
                   CONVERT(FROM_BASE64(vqu.value_chi),CHAR) as "Unit", \
                   m.qty as "Quantity",m.remark as "Remark",m.staff as "Staff",m.time as "Timpestamp" from meal m \
                   LEFT join child c on c.id = m.child_id \
                   LEFT Join va_meal_id vmi on m.meal_id = vmi.id \
                   LEFT Join va_qty_unit vqu on m.qty_unit = vqu.id \
                   ORDER BY m.child_id DESC',conn)
                   
 df3=sql.read_sql('Select n.child_id as "Child ID",c.child_no as "Child Number", \
                   CONVERT(FROM_BASE64(c.name_chi),CHAR) as "Chinese Name",c.name as "English Name", \
                   CONVERT(FROM_BASE64(vni.value_chi),CHAR) as "Sleep Status" , \
                   CONVERT(FROM_BASE64(vnqi.value_chi),CHAR) as " Sleep Quality", \
                   n.remark as "Remark",n.staff as "Staff",n.time as "Timestamp" from nap n \
                   LEFT join child c on c.id = n.child_id \
                   LEFT Join va_nap_id vni on n.nap_id = vni.id \
                   LEFT Join va_napquality_id vnqi on n. napquality_id = vnqi.id \
                   ORDER BY n.child_id DESC',conn)
                   
 df4=sql.read_sql('Select p.child_id as "Child ID",c.child_no as "Child Number", \
                   CONVERT(FROM_BASE64(c.name_chi),CHAR) as "Chinese Name",c.name as "English Name", \
                   CONVERT(FROM_BASE64(vpi.value_chi),CHAR) as "Perform", \
                   p.remark as "Remark",p.staff as "Staff",p.time as "Timestamp" from perform p \
                   LEFT join child c on c.id = p.child_id \
                   LEFT Join va_perform_id vpi on p.perform_id = vpi.id \
                   ORDER BY p.child_id DESC',conn)
                   
 df5=sql.read_sql('Select s.child_id as "Child ID",c.child_no as "Child Number", \
                   CONVERT(FROM_BASE64(c.name_chi),CHAR) as "Chinese Name",c.name as "English Name", \
                   CONVERT(FROM_BASE64(vpi.value_chi),CHAR) as "Child Skin Problem", \
	               CONVERT(FROM_BASE64(vpd.value_chi),CHAR) as "Child Skin Problem location", \
	               CONVERT(FROM_BASE64(vci.value_chi),CHAR) as "Child Skin Condition Status", \
                   s.remark as "Remark",s.staff as "Staff",s.time as "Timpestamp" from skin s \
	               LEFT Join va_condition_id vci on s. condition_id = vci.id \
	               LEFT join child c on c.id = s.child_id \
	               LEFT join skin_position sp on sp.id = s.child_id \
	               LEFT Join va_position_id vpi on sp.position_id = vpi.id \
	               LEFT Join va_position_detail vpd on sp.position_detail = vpd.id \
	               ORDER BY s.child_id DESC',conn)
	                
 df6=sql.read_sql('select t.child_id as "Child ID",c.child_no as "Child Number",CONVERT(FROM_BASE64(c.name_chi),CHAR) as "Chinese Name",c.name as "English Name", \
			t.temperature as "Temperature",staff as "Staff",t.time as "Timpestamp" from temperature t \
			LEFT join child c on c.id = t.child_id \
                        ORDER BY t.child_id DESC',conn)
 
 #print(df,df2,df3,df4,df5,df6,df7,df8)
 #get today
 df7=sql.read_sql('select h.child_id as "Child ID",c.child_no as "Child Number", \
                   CONVERT(FROM_BASE64(c.name_chi),CHAR) as "Chinese Name",c.name as "English Name", \
                   CONVERT(FROM_BASE64(vhi.value_chi),CHAR) as "Health", \
                   CONVERT(FROM_BASE64(vhsi.value_chi),CHAR) as "Health Status", \
                   h.remark as "Remark",h.staff as "Staff",h.time as "Timestamp" from health h \
                   LEFT join child c on c.id = h.child_id \
                   LEFT Join va_health_id vhi on h. health_id = vhi.id \
                   LEFT Join va_health_status_id vhsi on h.health_status_id = vhsi.id \
                   WHERE h.time > DATE_ADD(NOW(), INTERVAL -24 HOUR) \
                   ORDER BY h.child_id DESC',conn)
                   
 df8=sql.read_sql('Select m.child_id as "child ID",c.child_no as "Child Number", \
                   CONVERT(FROM_BASE64(c.name_chi),CHAR) as "Chinese Name",c.name as "English Name", \
                   CONVERT(FROM_BASE64(vmi.value_chi),CHAR) as "Meal Type", \
                   CONVERT(FROM_BASE64(vqu.value_chi),CHAR) as "Unit", \
                   m.qty as "Quantity",m.remark as "Remark",m.staff as "Staff",m.time as "Timpestamp" from meal m \
                   LEFT join child c on c.id = m.child_id \
                   LEFT Join va_meal_id vmi on m.meal_id = vmi.id \
                   LEFT Join va_qty_unit vqu on m.qty_unit = vqu.id \
                    WHERE m.time > DATE_ADD(NOW(), INTERVAL -24 HOUR) \
                    ORDER BY m.child_id DESC',conn)
                   
 df9=sql.read_sql('Select n.child_id as "Child ID",c.child_no as "Child Number", \
                    CONVERT(FROM_BASE64(c.name_chi),CHAR) as "Chinese Name",c.name as "English Name", \
                    CONVERT(FROM_BASE64(vni.value_chi),CHAR) as "Sleep Status" , \
                    CONVERT(FROM_BASE64(vnqi.value_chi),CHAR) as " Sleep Quality", \
                    n.remark as "Remark",n.staff as "Staff",n.time as "Timestamp" from nap n \
                    LEFT join child c on c.id = n.child_id \
                    LEFT Join va_nap_id vni on n.nap_id = vni.id \
                    LEFT Join va_napquality_id vnqi on n. napquality_id = vnqi.id \
                    WHERE n.time > DATE_ADD(NOW(), INTERVAL -24 HOUR) \
                    ORDER BY n.child_id DESC',conn)
                   
 df10=sql.read_sql('Select p.child_id as "Child ID",c.child_no as "Child Number", \
                    CONVERT(FROM_BASE64(c.name_chi),CHAR) as "Chinese Name",c.name as "English Name", \
                    CONVERT(FROM_BASE64(vpi.value_chi),CHAR) as "Perform", \
                    p.remark as "Remark",p.staff as "Staff",p.time as "Timestamp" from perform p \
                    LEFT join child c on c.id = p.child_id \
                    LEFT Join va_perform_id vpi on p.perform_id = vpi.id \
                    WHERE p.time > DATE_ADD(NOW(), INTERVAL -24 HOUR) \
                    ORDER BY p.child_id DESC',conn)
                   
 df11=sql.read_sql('Select s.child_id as "Child ID",c.child_no as "Child Number", \
                    CONVERT(FROM_BASE64(c.name_chi),CHAR) as "Chinese Name",c.name as "English Name", \
                    CONVERT(FROM_BASE64(vpi.value_chi),CHAR) as "Child Skin Problem", \
	                CONVERT(FROM_BASE64(vpd.value_chi),CHAR) as "Child Skin Problem location", \
	                CONVERT(FROM_BASE64(vci.value_chi),CHAR) as "Child Skin Condition Status", \
                    s.remark as "Remark",s.staff as "Staff",s.time as "Timpestamp" from skin s \
	                LEFT Join va_condition_id vci on s. condition_id = vci.id \
	                LEFT join child c on c.id = s.child_id \
	                LEFT join skin_position sp on sp.id = s.child_id \
	                LEFT Join va_position_id vpi on sp.position_id = vpi.id \
	                LEFT Join va_position_detail vpd on sp.position_detail = vpd.id \
	                WHERE s.time > DATE_ADD(NOW(), INTERVAL -24 HOUR) \
	                ORDER BY s.child_id DESC',conn)
	                
 df12=sql.read_sql('select t.child_id as "Child ID",c.child_no as "Child Number",CONVERT(FROM_BASE64(c.name_chi),CHAR) as "Chinese Name",c.name as "English Name", \
			t.temperature as "Temperature",staff as "Staff",t.time as "Timpestamp" from temperature t \
			LEFT join child c on c.id = t.child_id \
			WHERE t.time > DATE_ADD(NOW(), INTERVAL -24 HOUR) \
                        ORDER BY t.child_id DESC',conn)
                    
 #print(df9,df10,df11,df12,df13,df14,df15,df16)
 #get before 7 day
 df13=sql.read_sql('select h.child_id as "Child ID",c.child_no as "Child Number", \
                    CONVERT(FROM_BASE64(c.name_chi),CHAR) as "Chinese Name",c.name as "English Name", \
                    CONVERT(FROM_BASE64(vhi.value_chi),CHAR) as "Health", \
                    CONVERT(FROM_BASE64(vhsi.value_chi),CHAR) as "Health Status", \
                    h.remark as "Remark",h.staff as "Staff",h.time as "Timestamp" from health h \
                    LEFT join child c on c.id = h.child_id \
                    LEFT Join va_health_id vhi on h. health_id = vhi.id \
                    LEFT Join va_health_status_id vhsi on h.health_status_id = vhsi.id \
                    WHERE h.time > DATE_ADD(NOW(), INTERVAL -7 DAY) \
                    ORDER BY h.child_id DESC',conn)
                    
 df14=sql.read_sql('Select m.child_id as "child ID",c.child_no as "Child Number", \
                   CONVERT(FROM_BASE64(c.name_chi),CHAR) as "Chinese Name",c.name as "English Name", \
                   CONVERT(FROM_BASE64(vmi.value_chi),CHAR) as "Meal Type", \
                   CONVERT(FROM_BASE64(vqu.value_chi),CHAR) as "Unit", \
                   m.qty as "Quantity",m.remark as "Remark",m.staff as "Staff",m.time as "Timpestamp" from meal m \
                   LEFT join child c on c.id = m.child_id \
                   LEFT Join va_meal_id vmi on m.meal_id = vmi.id \
                   LEFT Join va_qty_unit vqu on m.qty_unit = vqu.id \
                    WHERE m.time > DATE_ADD(NOW(), INTERVAL -7 DAY) \
                    ORDER BY m.child_id DESC',conn)
                    
 df15=sql.read_sql('Select n.child_id as "Child ID",c.child_no as "Child Number", \
                    CONVERT(FROM_BASE64(c.name_chi),CHAR) as "Chinese Name",c.name as "English Name", \
                    CONVERT(FROM_BASE64(vni.value_chi),CHAR) as "Sleep Status" , \
                    CONVERT(FROM_BASE64(vnqi.value_chi),CHAR) as " Sleep Quality", \
                    n.remark as "Remark",n.staff as "Staff",n.time as "Timestamp" from nap n \
                    LEFT join child c on c.id = n.child_id \
                    LEFT Join va_nap_id vni on n.nap_id = vni.id \
                    LEFT Join va_napquality_id vnqi on n. napquality_id = vnqi.id \
                    WHERE n.time > DATE_ADD(NOW(), INTERVAL -7 DAY) \
                    ORDER BY n.child_id DESC',conn)
                    
 df16=sql.read_sql('Select p.child_id as "Child ID",c.child_no as "Child Number", \
                    CONVERT(FROM_BASE64(c.name_chi),CHAR) as "Chinese Name",c.name as "English Name", \
                    CONVERT(FROM_BASE64(vpi.value_chi),CHAR) as "Perform", \
                    p.remark as "Remark",p.staff as "Staff",p.time as "Timestamp" from perform p \
                    LEFT join child c on c.id = p.child_id \
                    LEFT Join va_perform_id vpi on p.perform_id = vpi.id \
                    WHERE p.time > DATE_ADD(NOW(), INTERVAL -7 DAY) \
                    ORDER BY p.child_id DESC',conn)
                    
 df17=sql.read_sql('Select s.child_id as "Child ID",c.child_no as "Child Number", \
                    CONVERT(FROM_BASE64(c.name_chi),CHAR) as "Chinese Name",c.name as "English Name", \
                    CONVERT(FROM_BASE64(vpi.value_chi),CHAR) as "Child Skin Problem", \
	                CONVERT(FROM_BASE64(vpd.value_chi),CHAR) as "Child Skin Problem location", \
	                CONVERT(FROM_BASE64(vci.value_chi),CHAR) as "Child Skin Condition Status", \
                    s.remark as "Remark",s.staff as "Staff",s.time as "Timpestamp" from skin s \
	                LEFT Join va_condition_id vci on s. condition_id = vci.id \
	                LEFT join child c on c.id = s.child_id \
	                LEFT join skin_position sp on sp.id = s.child_id \
	                LEFT Join va_position_id vpi on sp.position_id = vpi.id \
	                LEFT Join va_position_detail vpd on sp.position_detail = vpd.id \
	                WHERE s.time > DATE_ADD(NOW(), INTERVAL -7 DAY) \
	                ORDER BY s.child_id DESC',conn)
	                
 df18=sql.read_sql('select t.child_id as "Child ID",c.child_no as "Child Number",CONVERT(FROM_BASE64(c.name_chi),CHAR) as "Chinese Name",c.name as "English Name", \
			t.temperature as "Temperature",staff as "Staff",t.time as "Timpestamp" from temperature t \
			LEFT join child c on c.id = t.child_id \
			WHERE t.time > DATE_ADD(NOW(), INTERVAL -7 DAY) \
                        ORDER BY t.child_id DESC',conn)
                    
 #print(df17,df18,df19,df20,df21,df22,df23,df24)
 #get before 30 day
 df19=sql.read_sql('select h.child_id as "Child ID",c.child_no as "Child Number", \
                    CONVERT(FROM_BASE64(c.name_chi),CHAR) as "Chinese Name",c.name as "English Name", \
                    CONVERT(FROM_BASE64(vhi.value_chi),CHAR) as "Health", \
                    CONVERT(FROM_BASE64(vhsi.value_chi),CHAR) as "Health Status", \
                    h.remark as "Remark",h.staff as "Staff",h.time as "Timestamp" from health h \
                    LEFT join child c on c.id = h.child_id \
                    LEFT Join va_health_id vhi on h. health_id = vhi.id \
                    LEFT Join va_health_status_id vhsi on h.health_status_id = vhsi.id \
                    WHERE time > DATE_ADD(NOW(), INTERVAL -1 MONTH) \
                    ORDER BY h.child_id DESC',conn)
                    
 df20=sql.read_sql('Select m.child_id as "child ID",c.child_no as "Child Number", \
                    CONVERT(FROM_BASE64(c.name_chi),CHAR) as "Chinese Name",c.name as "English Name", \
                    CONVERT(FROM_BASE64(vmi.value_chi),CHAR) as "Meal Type", \
                    CONVERT(FROM_BASE64(vqu.value_chi),CHAR) as "Unit", \
                    m.qty as "Quantity",m.remark as "Remark",m.staff as "Staff",m.time as "Timpestamp" from meal m \
                    LEFT join child c on c.id = m.child_id \
                    LEFT Join va_meal_id vmi on m.meal_id = vmi.id \
                    LEFT Join va_qty_unit vqu on m.qty_unit = vqu.id \
                    WHERE m.time > DATE_ADD(NOW(), INTERVAL -1 MONTH) \
                    ORDER BY m.child_id DESC',conn)
                    
 df21=sql.read_sql('Select n.child_id as "Child ID",c.child_no as "Child Number", \
                    CONVERT(FROM_BASE64(c.name_chi),CHAR) as "Chinese Name",c.name as "English Name", \
                    CONVERT(FROM_BASE64(vni.value_chi),CHAR) as "Sleep Status" , \
                    CONVERT(FROM_BASE64(vnqi.value_chi),CHAR) as " Sleep Quality", \
                    n.remark as "Remark",n.staff as "Staff",n.time as "Timestamp" from nap n \
                    LEFT join child c on c.id = n.child_id \
                    LEFT Join va_nap_id vni on n.nap_id = vni.id \
                    LEFT Join va_napquality_id vnqi on n. napquality_id = vnqi.id \
                    WHERE n.time > DATE_ADD(NOW(), INTERVAL -1 MONTH) \
                    ORDER BY n.child_id DESC',conn)
                    
 df22=sql.read_sql('Select p.child_id as "Child ID",c.child_no as "Child Number", \
                    CONVERT(FROM_BASE64(c.name_chi),CHAR) as "Chinese Name",c.name as "English Name", \
                    CONVERT(FROM_BASE64(vpi.value_chi),CHAR) as "Perform", \
                    p.remark as "Remark",p.staff as "Staff",p.time as "Timestamp" from perform p \
                    LEFT join child c on c.id = p.child_id \
                    LEFT Join va_perform_id vpi on p.perform_id = vpi.id \
                    WHERE p.time > DATE_ADD(NOW(), INTERVAL -1 MONTH) \
                    ORDER BY p.child_id DESC',conn)
                    
 df23=sql.read_sql('Select s.child_id as "Child ID",c.child_no as "Child Number", \
                    CONVERT(FROM_BASE64(c.name_chi),CHAR) as "Chinese Name",c.name as "English Name", \
                    CONVERT(FROM_BASE64(vpi.value_chi),CHAR) as "Child Skin Problem", \
	                CONVERT(FROM_BASE64(vpd.value_chi),CHAR) as "Child Skin Problem location", \
	                CONVERT(FROM_BASE64(vci.value_chi),CHAR) as "Child Skin Condition Status", \
                    s.remark as "Remark",s.staff as "Staff",s.time as "Timpestamp" from skin s \
	                LEFT Join va_condition_id vci on s. condition_id = vci.id \
	                LEFT join child c on c.id = s.child_id \
	                LEFT join skin_position sp on sp.id = s.child_id \
	                LEFT Join va_position_id vpi on sp.position_id = vpi.id \
	                LEFT Join va_position_detail vpd on sp.position_detail = vpd.id \
	                WHERE s.time > DATE_ADD(NOW(), INTERVAL -1 MONTH) \
	                ORDER BY s.child_id DESC',conn)
	                
 df24=sql.read_sql('select t.child_id as "Child ID",c.child_no as "Child Number",CONVERT(FROM_BASE64(c.name_chi),CHAR) as "Chinese Name",c.name as "English Name", \
			t.temperature as "Temperature",staff as "Staff",t.time as "Timpestamp" from temperature t \
			LEFT join child c on c.id = t.child_id \
			WHERE t.time > DATE_ADD(NOW(), INTERVAL -1 MONTH) \
                        ORDER BY t.child_id DESC',conn)

 df28=sql.read_sql('Select d.id as "Child ID",c.child_no as "Child Number", \
                    CONVERT(FROM_BASE64(c.name_chi),CHAR) as "Chinese Name",c.name as "English Name", \
                    CONVERT(FROM_BASE64(vdi.value_chi),CHAR) as "Child Diaper type", \
                    CONVERT(FROM_BASE64(vds.value_chi),CHAR) as "Child Diaper Status", \
                    d.remark as "Remark",d.staff as "Staff",d.time as "Timpestamp" from diaper d \
	                LEFT join child c on c.id = d.child_id \
	                LEFT join diaper_status ds on d.id=ds.id \
	                LEFT Join va_diaper_id vdi on d.diaper_id = vdi.id \
	                LEFT Join va_diaper_status_id vds on ds.diaper_status_id = vds.id',conn)
	                
 df29=sql.read_sql('Select d.id as "Child ID",c.child_no as "Child Number", \
                    CONVERT(FROM_BASE64(c.name_chi),CHAR) as "Chinese Name",c.name as "English Name", \
                    CONVERT(FROM_BASE64(vdi.value_chi),CHAR) as "Child Diaper type", \
                    CONVERT(FROM_BASE64(vds.value_chi),CHAR) as "Child Diaper Status", \
                    d.remark as "Remark",d.staff as "Staff",d.time as "Timpestamp" from diaper d \
	                LEFT join child c on c.id = d.child_id \
	                LEFT join diaper_status ds on d.id=ds.id \
	                LEFT Join va_diaper_id vdi on d.diaper_id = vdi.id \
	                LEFT Join va_diaper_status_id vds on ds.diaper_status_id = vds.id \
	                WHERE d.time > DATE_ADD(NOW(), INTERVAL -24 HOUR) \
	                ORDER BY d.id DESC',conn)
	                
 df30=sql.read_sql('Select d.id as "Child ID",c.child_no as "Child Number", \
                    CONVERT(FROM_BASE64(c.name_chi),CHAR) as "Chinese Name",c.name as "English Name", \
                    CONVERT(FROM_BASE64(vdi.value_chi),CHAR) as "Child Diaper type", \
                    CONVERT(FROM_BASE64(vds.value_chi),CHAR) as "Child Diaper Status", \
                    d.remark as "Remark",d.staff as "Staff",d.time as "Timpestamp" from diaper d \
	                LEFT join child c on c.id = d.child_id \
	                LEFT join diaper_status ds on d.id=ds.id \
	                LEFT Join va_diaper_id vdi on d.diaper_id = vdi.id \
	                LEFT Join va_diaper_status_id vds on ds.diaper_status_id = vds.id \
	                WHERE d.time > DATE_ADD(NOW(), INTERVAL -7 DAY) \
	                ORDER BY d.id DESC',conn)
 df31=sql.read_sql('Select d.id as "Child ID",c.child_no as "Child Number", \
                    CONVERT(FROM_BASE64(c.name_chi),CHAR) as "Chinese Name",c.name as "English Name", \
                    CONVERT(FROM_BASE64(vdi.value_chi),CHAR) as "Child Diaper type", \
                    CONVERT(FROM_BASE64(vds.value_chi),CHAR) as "Child Diaper Status", \
                    d.remark as "Remark",d.staff as "Staff",d.time as "Timpestamp" from diaper d \
	                LEFT join child c on c.id = d.child_id \
	                LEFT join diaper_status ds on d.id=ds.id \
	                LEFT Join va_diaper_id vdi on d.diaper_id = vdi.id \
	                LEFT Join va_diaper_status_id vds on ds.diaper_status_id = vds.id \
	                WHERE d.time > DATE_ADD(NOW(), INTERVAL -1 MONTH) \
	                ORDER BY d.id DESC',conn)
 
#print(df25,df26,df27,df28,df29,df30,df31)
 #expore all data
 df1.to_excel('./static/excel/childstatus_health.xlsx',sheet_name ='Childstatus_Health'+now,index=False, header=True)
 df2.to_excel('./static/excel/childstatus_meal.xlsx',sheet_name ='Childstatus_Meal'+now,index=False, header=True)
 df3.to_excel('./static/excel/childstatus_nap.xlsx',sheet_name ='Childstatus_Nap'+now,index=False, header=True)
 df4.to_excel('./static/excel/childstatus_perform.xlsx',sheet_name ='Childstatus_Perform'+now,index=False, header=True)
 df5.to_excel('./static/excel/childstatus_skin.xlsx',sheet_name ='Childstatus_Skin'+now,index=False, header=True)
 df6.to_excel('./static/excel/childstatus_temperature.xlsx',sheet_name ='Childstatus_Temperature'+now,index=False, header=True)
 #expore today data
 df7.to_excel('./static/excel/childstatus_health_today.xlsx',sheet_name ='Childstatus_Health_Today'+now,index=False, header=True)
 df8.to_excel('./static/excel/childstatus_meal_today.xlsx',sheet_name ='Childstatus_Meal_Today'+now,index=False, header=True)
 df9.to_excel('./static/excel/childstatus_nap_today.xlsx',sheet_name ='Childstatus_Nap_Today'+now,index=False, header=True)
 df10.to_excel('./static/excel/childstatus_perform_today.xlsx',sheet_name ='Childstatus_Perform_Today'+now,index=False, header=True)
 df11.to_excel('./static/excel/childstatus_skin_today.xlsx',sheet_name ='Childstatus_Skin_Today'+now,index=False, header=True)
 df12.to_excel('./static/excel/childstatus_temperature_today.xlsx',sheet_name ='Childstatus_Temperature_Today'+now,index=False, header=True)
 #expore before 7 data
 df13.to_excel('./static/excel/childstatus_health_before_7day.xlsx',sheet_name ='Childstatus_Health_Before_7day'+now,index=False, header=True)
 df14.to_excel('./static/excel/childstatus_meal_before_7day.xlsx',sheet_name ='Childstatus_Meal_Before_7day'+now,index=False, header=True)
 df15.to_excel('./static/excel/childstatus_nap_before_7day.xlsx',sheet_name ='Childstatus_Nap_Before_7day'+now,index=False, header=True)
 df16.to_excel('./static/excel/childstatus_perform_before_7day.xlsx',sheet_name ='Childstatus_Perform_Before_7day'+now,index=False, header=True)
 df17.to_excel('./static/excel/childstatus_skin_before_7day.xlsx',sheet_name ='Childstatus_Skin_Before_7day'+now,index=False, header=True)
 df18.to_excel('./static/excel/childstatus_temperature_before_7_day.xlsx',sheet_name ='Childstatus_Temp_Before_7day'+now,index=False, header=True)
 #expore before 30 data
 df19.to_excel('./static/excel/childstatus_health_before_30day.xlsx',sheet_name ='Childstatus_Health_30day'+now,index=False, header=True)
 df20.to_excel('./static/excel/childstatus_meal_before_30day.xlsx',sheet_name ='Childstatus_Meal_30day'+now,index=False, header=True)
 df21.to_excel('./static/excel/childstatus_nap_before_30day.xlsx',sheet_name ='Childstatus_Nap_30day'+now,index=False, header=True)
 df22.to_excel('./static/excel/childstatus_perform_before_30day.xlsx',sheet_name ='Childstatus_Perform_30day'+now,index=False, header=True)
 df23.to_excel('./static/excel/childstatus_skin_before_30day.xlsx',sheet_name ='Childstatus_Skin_30day'+now,index=False, header=True)
 df24.to_excel('./static/excel/childstatus_temperature_before_30day.xlsx',sheet_name ='Childstatus_Temp_30day'+now,index=False, header=True)
 df28.to_excel('./static/excel/childstatus_diaper.xlsx',sheet_name ='Childstatus_Diaper'+now,index=False, header=True)
 df29.to_excel('./static/excel/childstatus_diaper_today.xlsx',sheet_name ='Childstatus_Diaper_Today'+now,index=False, header=True)
 df30.to_excel('./static/excel/childstatus_diaper_before_7day.xlsx',sheet_name ='Childstatus_Diaper_Before_7day'+now,index=False, header=True)
 df31.to_excel('./static/excel/childstatus_diaper_before_30day.xlsx',sheet_name ='Childstatus_Diaper_30day'+now,index=False, header=True)
 return (render_template('export_excel.html', loggeduser=_un),conn.close())
 
# explore excel download views------------------------------------------------    
@pg_status.route("/download", methods=['GET'])
def download_file():
   _un, _role = loggeduser(request)
   if _un is None:
        return redirect('/login')
   if _role == 'parent':
        return render_template('contactus.html', loggeduser=_un)
   output = io.BytesIO() 
   writer = pd.ExcelWriter(output, engine='xlsxwriter')
   conn = gv.dbpool.connection()
   df=sql.read_sql('select * from status',conn)
   df.to_excel(writer, sheet_name='status')
   writer.save()
   output.seek(0)
   excelDownload=output.read()
   return (excel.make_response(excelDownload,attachment_filename='status.xlsx',as_attachment=True),conn.close())
# decode child and parent excel file------------------------------------------------
@pg_status.route('/export_excel_parent_child', methods=['GET','POST'])
def export_excel_parent_child():
 _un, _role = loggeduser(request)
 if _un is None:
        return redirect('/login')
 if _role == 'parent':
        return render_template('contactus.html', loggeduser=_un)
 conn = gv.dbpool.connection()
 df25=sql.read_sql('Select CONVERT(FROM_BASE64(name),CHAR)as"Name", \
                    CONVERT(FROM_BASE64(name_chi),CHAR) as "Chinese Name",child_ids as"Child Serial Number",tel as "Tel", \
                    CONVERT(FROM_BASE64(edu),CHAR)as"Edu", CONVERT(FROM_BASE64(occupation),CHAR)as"Occupation",\
                    CONVERT(FROM_BASE64(reason),CHAR)as"Reason" From parent',conn)
                    
 df25.to_excel('./static/excel/parent.xlsx',sheet_name ='parent',index=False, header=True)
 df26=sql.read_sql('Select c.name as "English Name", CONVERT(FROM_BASE64(c.name_chi),CHAR) as "Chinese Name", \
                    CONVERT(FROM_BASE64(c.email),CHAR) as "Email", child_no as "Child Number",x.name as "Group", \
                    CONVERT(FROM_BASE64(g.name),CHAR) as "Gender",c.birth_cert_no as "HKID",c.born_day as "Born Day", \
                    c.date_in as "Join Center Date", Tel From child c \
                    LEFT Join gender g on c.gender_id = g.id LEFT Join `group` x on c.group_id = g.id',conn)
                    
 df26.to_excel('./static/excel/child.xlsx',sheet_name ='child',index=False, header=True)
 df27=sql.read_sql('Select c.name as "English Name", CONVERT(FROM_BASE64(c.name_chi),CHAR) as "Chinese Name", \
                    CONVERT(FROM_BASE64(c.email),CHAR) as "Email", child_no as "Child Number",x.name as "Group", \
                    CONVERT(FROM_BASE64(g.name),CHAR) as "Gender",c.birth_cert_no as "HKID",c.born_day as "Born day", \
                    c.date_in as "Join Center Date", Tel From child c LEFT Join gender g on c.gender_id = g.id \
                    LEFT Join `group` x on c.group_id = g.id \
                    where date_in > DATE_ADD(NOW(), INTERVAL -1 MONTH)',conn)
                    
 df27.to_excel('./static/excel/child_1month.xlsx',sheet_name ='child',index=False, header=True)
 return (render_template('export_excel_parent_child.html', loggeduser=_un),conn.close())
#it can delete------------------------------------------------------------------------------
'''
@pg_status.route('/export_excel_two', methods=['GET','POST'])
def export_excel_two():
 conn = gv.dbpool.connection()
 df100=sql.read_sql('select * from child',conn)
 df100.to_excel('./static/excel/child.xls',sheet_name ='child',index=False, header=True)
 base64.decode(open("child.xls"),conn)
 return render_template('export_excel_two.html')
 
@pg_status.route('/export_excel_three', methods=['GET','POST'])
def export_excel_three():
 conn = gv.dbpool.connection()
 df33=sql.read_sql('Select FROM_BASE64(name) From parent',conn)
 df33.to_excel('./static/excel/parent.xls',sheet_name ='parent',index=False, header=True)
 test = './static/excel/parent.xls'
 base64.b64decode(test)
 data = open('./static/excel/parent.xls').read()
 decoded = base64.b64decode(data+ b'===').decode('utf-8')
 print (decoded)
 return render_template('export_excel_three.html')
 '''
 #------------------------------------------------------------------------------
