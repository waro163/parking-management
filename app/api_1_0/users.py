# -*- coding: utf-8 -*-
from flask import jsonify, request, current_app, url_for,g
from . import api
from ..models import User
from ..email import send_email
from .errors import  alert
import json
import re
from .decorators import login_require
from .. import db

@api.route('/user/register',methods=['GET','POST'])
def register():
    _account = g.body.get('account')
    _password = g.body.get('password')
    _token = g.body.get('token')
    if not (_account and _password and _token):
        return alert(10001,'Register data not found in post data')
    user = User.query.filter_by(email = _account).first()
    if not user:
        return alert(20003,'please get token firstly')
    if not user.confirm(_token):
        return alert(20004,'your token is wrong, please check again')
    user.password = _password
    db.session.add(user)
    _session_id = user.generate_session_token()
    db.session.commit()
    return jsonify({'head':{'resultCode':'1'},'status':{'code':'', 'message': ''},\
                    'body':{'session_id':_session_id, 'account':_account}})

@api.route('/user/gettoken',methods=['GET','POST'])
def gettoken():
    _account =  g.body.get('account')
    if not _account:
        return alert(10001,'account number not found in post data')
    _email_pattern = re.compile(current_app.config.get('EMAIL_PATTERN'))
    if not _email_pattern.match(_account):
        return alert(20001,'please check your eamil number, it must be xxx@yy.com|cn')
    _user = User.query.filter_by(email = _account).first()
    if _user:
        if _user.email_confirmed:
            return alert(20002,'you had register the email account and confirm it')
        else:
            _token = _user.generate_confirmation_token()
            send_email(_account,'Confirm Your Account','email/token',token = _token)
    else:
        user_new = User(email = _account)
        db.session.add(user_new)
        _token = user_new.generate_confirmation_token()
        send_email(_account,'Confirm Your Account','email/token',token = _token)
    db.session.commit()
    return jsonify({'head':{'resultCode':'1'},'status':{'code':'','message': ''},'body':{'msg':'please check your email to fill your token'}})

@api.route('/user/login',methods = ['GET','POST'])
def login():
    _account = g.body.get('account')
    _password = g.body.get('password')
    user = User.query.filter_by(email = _account).first()
    if not user:
        return alert(20005,'your email account is not exit, please sign in firstly')
    if not user.verify_password(_password):
        return alert(20006,'your password is wrong, please check again')
    _session_id = user.generate_session_token()
    db.session.commit()
    return jsonify({'head':{'resultCode':'1'},'status':{'code':'','message': ''},\
                    'body':{'sessionId':_session_id, 'account':_account}})