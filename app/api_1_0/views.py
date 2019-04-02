# -*- coding: utf-8 -*-
from .. import email
from . import api
from flask import render_template,g,redirect,url_for,request,jsonify,current_app
from .decorators import login_require

@api.route('/',methods=['GET','POST'])
def index():
    return 'Hello World'

@api.route('/testrequest',methods=['GET','POST'])
def test_request():
    print(request.form.get('head'))
    print(request.form.get('body'))
    print('type is: ',type(request.form.get('body')))
    print('g body:',g.body.get('account'))
    print('g body:', type(g.body.get('token')))
    return jsonify({'head':{'resultCode':'1'},'status':{'code':200,'message': 'test request successfully'},'body':{'msg':'yes, you got it'}})

@api.route('/test/<name>',methods=['GET','POST'])
@api.route('/test/',methods=['GET','POST'])
@login_require
def test(name=None):
    if name:
        return jsonify({'name':name, 'code':'random123'})
    return 'Hello Stranger'
