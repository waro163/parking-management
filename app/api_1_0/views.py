# -*- coding: utf-8 -*-
from .. import email
from . import api
from flask import render_template,session,redirect,url_for,request,jsonify,current_app
from .decorators import login_require

@api.route('/',methods=['GET','POST'])
# @auth.login_required
def index():
    return 'Hello World'

@api.route('/test/<name>',methods=['GET','POST'])
@api.route('/test/',methods=['GET','POST'])
@login_require
def test(name=None):
    if name:
        return jsonify({'name':name, 'code':'random123'})
    return 'Hello Stranger'
