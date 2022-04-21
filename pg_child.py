#!/usr/bin/env python3
# -*- coding:utf-8 -*-
"""
孩子蓝图
定义蓝图pg_child，实现孩子相关页面蓝图
"""
from urllib import parse

from flask import Blueprint, redirect, render_template, request, abort, flash
import os.path
import funcs,boto3,logging
import global_var as gv
import sys,time
import matplotlib.pyplot as plt 
import matplotlib.image as mpimg
from api_loginout import loggeduser, verify_auto
from werkzeug.utils import secure_filename
from botocore.exceptions import NoCredentialsError,ClientError
from boto3.session import Session
# 定义蓝图-------------------------------------------------
pg_child = Blueprint(
    'pg_child',
    __name__,
    template_folder='templates'
)

# views------------------------------------------------


@pg_child.route('/childinfo', methods=['GET'])
def childinfo_get():
    _cid = request.args.get('id')
    if _cid is None:
        abort(404)
    _un, _role = loggeduser(request)
    return render_template('infopage.html', loggeduser=_un,
                           uid=_cid, role='childinfo')


@pg_child.route('/addchild', methods=['GET'])
def addchild_get():
    _un, _role = loggeduser(request)
    return render_template('addchild.html', loggeduser=_un)

@pg_child.route('/childlist', methods=['GET'])
def childlist_get():
    _un, _role = loggeduser(request)
    return render_template('childlist.html', loggeduser=_un)

@pg_child.route('/alterchild', methods=['GET'])
def alterchild_get():
    _cid = request.args.get('id')
    if _cid is None:
        abort(404)
    _un, _role = loggeduser(request)
    return render_template('alterchild.html', loggeduser=_un, cid=_cid)

@pg_child.route('/filelist', methods=['GET'])
def filelist_get():
    _un, _role = loggeduser(request)
    return render_template('filelist.html', loggeduser=_un)
@pg_child.route('/file', methods=['GET'])
def file_get():
    _fid = request.args.get('id')
    if _fid is None:
        abort(404)
    _un, _role = loggeduser(request)
    return render_template('file.html', loggeduser=_un, fid=_fid)
@pg_child.route('/upfile', methods=['GET', 'POST'])
def upfile():
    _un, _role = loggeduser(request)
    if _un is None:
        return redirect('/login')
    return render_template('upfile.html', loggeduser=_un)
    
@pg_child.route('/common', methods=['GET', 'POST'])
def common():
    _un, _role = loggeduser(request)
    if _un is None:
        return redirect('/login')
    return render_template('common.html', loggeduser=_un)
    
@pg_child.route('/contactus', methods=['GET', 'POST'])
def contactus():
    _un, _role = loggeduser(request)
    if _un is None:
        return redirect('/login')
    return render_template('contactus.html', loggeduser=_un)
    
    
@pg_child.route('/export_excel_two', methods=['GET', 'POST'])
def export_excel_two():
    _un, _role = loggeduser(request)
    if _un is None:
        return redirect('/login')
    return render_template('export_excel_two.html', loggeduser=_un)
    
    
    #*******************************************************
    #for upload file to AWS S3 BUCKET method
'''
@pg_child.route('/upload', methods=['POST','GET'])
def uploads():
    #bucket, s3_file
    ACCESS_KEY ='XXXXXXXXXXXXXXXXXX'
    SECRET_KEY ='XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX'
    session = Session(aws_access_key_id=ACCESS_KEY,aws_secret_access_key=SECRET_KEY,region_name='us-east-1')
    #s3_client = boto3.client('s3')
    bucket = ('XXXXXXXXXX')
    s3_file = ('XXXXXXXXXXXX')
    s3 = boto3.client('s3')
    s3 = boto3.resource('s3')
    s3 = session.resource('s3')
    s3 = boto3.client('s3', aws_access_key_id=ACCESS_KEY, aws_secret_access_key=SECRET_KEY)
    _un, _role = loggeduser(request)
    if _un is None:
        return redirect('/login')
    if _role == 'parent':
        return render_template('contactus.html', loggeduser=_un)
    if _role == 'staff':
        return '<h1>No authority!</h1><p>Login as admin please.</p>'
    try:
        s3.upload_file(s3_file,bucket,'test.png')
        print("Upload Successful")
        return True
    except FileNotFoundError:
        print("The file was not found")
        return render_template('error.html', loggeduser=_un)
    except NoCredentialsError:
        print("Credentials not available")
        return render_template('error.html', loggeduser=_un)
    return render_template('upload.html', loggeduser=_un)
'''
    #*******************************************************
    #for upload file to local system method
    # seting upload file sytle
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'JPG', 'PNG'])
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS
    
@pg_child.route('/upload', methods=['POST', 'GET'])
def upload():
    _un, _role = loggeduser(request)
    if _un is None:
        return redirect('/login')
    if _role == 'parent':
        return render_template('contactus.html', loggeduser=_un)
    if _role == 'staff':
        return '<h1>No authority!</h1><p>Login as admin please.</p>'
    if request.method == 'POST':
        # from file label to get files 
        f = request.files['file']
        #check file style
        if not (f and allowed_file(f.filename)):
            print({"error": 1001, "msg": "photo style：png、PNG、jpg、JPG"})#forbid other type
            return render_template('upload_error.html', loggeduser=_un)
        # Path of current file
        # basepath = os.path.dirname(_file_)
        # FILE NAME
        # rename photo to localtime
        now = time.strftime("%Y-%m-%d-%H_%M_%S",time.localtime(time.time()))#auto change photo name
        UPLOAD_FOLDER = '/var/www/html/childcare/uploads/notice_board/'+ now + secure_filename(f.filename)
        # save photo
        f.save(UPLOAD_FOLDER)
        # return to the upload success interface
        print("upload success")
        return render_template('upload.html')
    # Return to the upload interface
    return render_template('upload.html', loggeduser=_un)
   #*******************************************************
@pg_child.route('/parent_upload', methods=['POST', 'GET'])
def parent_upload():
    _un, _role = loggeduser(request)
    if _un is None:
        return redirect('/login')
    if _role == 'parent':
        return render_template('contactus.html', loggeduser=_un)
    if request.method == 'POST':
        # from file label to get files 
        f = request.files['file']
        #check file style
        if not (f and allowed_file(f.filename)):
            print({"error": 1001, "msg": "photo style：png、PNG、jpg、JPG"})#forbid other type
            return render_template('upload_error.html', loggeduser=_un)
        # Path of current file
        # basepath = os.path.dirname(_file_)
        # FILE NAME
        # rename photo to localtime
        now = time.strftime("%Y-%m-%d-%H_%M_%S",time.localtime(time.time()))#auto change photo name
        UPLOAD_FOLDER = '/var/www/html/childcare/uploads/parent_notice_board/'+ now + secure_filename(f.filename)
        # save photo
        f.save(UPLOAD_FOLDER)
        # return to the upload success interface
        print("upload success")
        return render_template('parent_upload.html')
    # Return to the upload interface
    return render_template('parent_upload.html', loggeduser=_un)
   #*******************************************************
   #not in use
    '''
@pg_child.route('/showphoto', methods=['GET','POST'])
def showphoto():
    _un, _role = loggeduser(request)
    if _un is None:
        return redirect('/login')
    if _role == 'parent':
        return render_template('upload.html', loggeduser=_un)
    photo = './static/notice_board/.PNG'
    img = mpimg.imread(photo)
    plt.imshow(img)
    print(photo)
    return render_template('showphoto.html', loggeduser=_un)
    '''   
    #*******************************************************
    
@pg_child.route('/parent_show', methods=['GET','POST'])
def parent_show():
    _un, _role = loggeduser(request)
    if _un is None:
        return render_template('/login')
    return render_template('parent_show.html', loggeduser=_un)
 #*******************************************************
 
@pg_child.route('/showphoto', methods=['GET','POST'])
def showphoto():
    _un, _role = loggeduser(request)
    if _un is None:
        return redirect('/login')
    if _role == 'parent':
        return render_template('contactus.html', loggeduser=_un)
    return render_template('showphoto.html', loggeduser=_un)
    
@pg_child.route('/redirect', methods=['GET','POST'])
def redirectShowphoto():
    _un, _role = loggeduser(request)
    if _un is None:
        return render_template('/login')
    return render_template('redirect.html', loggeduser=_un)
    #*******************************************************
    #not in use
'''
@pg_child.route('/showphoto', methods=['GET','POST'])
def showphoto():
    _un, _role = loggeduser(request)
    if _un is None:
        return redirect('/login')
    if _role == 'parent':
        return render_template('contactus.html', loggeduser=_un)
    folder="./static/notice_board/"
    images = []
    for filename in os.listdir(folder):
        img = mpimg.imread(os.path.join(folder,filename))
        if img is not None:
            images.append(img)
    return render_template('showphoto.html', loggeduser=_un)
'''
#*******************************************************
#not in use
'''
@pg_child.route('/recommend', methods=['GET','PUT'])
def recommend():
    _un = loggeduser(request)
    if request.method == 'GET':
        return render_template('recommend.html', loggeduser=_un)
        
    if request.method == 'POST':
        name = request.form.get('name')
        age = request.form.get('age')
        
        print("done")
        return render_template('recommend.html', loggeduser=_un)
     '''   
# --------------------------------------------
#not in use
'''
@pg_child.route('/recommend', methods=['GET', 'POST'])
def recommend():
    if request.method == 'GET':
        return render_template('recommend.html')
        
@pg_child.route('/say', methods=['GET', 'POST'])
def say():
    if request.method == 'GET':
        return render_template('say.html')
'''        