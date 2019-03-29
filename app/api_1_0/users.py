# -*- coding: utf-8 -*-
from flask import jsonify, request, current_app, url_for
from . import api
from ..models import User, Post
from .errors import  alert
import requests, json
import os
from consts import Wxcode2SessionUrl
from ..utils import WXBizDataCrypt
from .decorators import login_require
from .. import db

@api.route('/user/register',methods=['GET','POST'])
def get_user():
    # print(request.json)
    try:
        _code = request.json['body'].get('code')
        _iv = request.json['body'].get('iv')
        _encryptedData = request.json['body'].get('encryptedData')
    except Exception:
        return alert(10001,'Register data not found in post data')

    _wxcode2sessionurl =  Wxcode2SessionUrl.format(APPID=current_app.config['APPID'],SECRET=current_app.config['APPSECRET'],JSCODE=_code)
    _wxlogincode = requests.get(_wxcode2sessionurl)
    r = json.loads(_wxlogincode.text)
    if r.get('errcode') != 0:
        return alert(30001,'cannot get the session_key and openid from wechat server')
    _session_key = r.get('session_key')
    _openid = r.get('openid')
    _pc = WXBizDataCrypt(current_app.config.get('APPID'),_session_key)
    _res = _pc.decrypt(_encryptedData,_iv)
    if not _res:
        return alert(30002, 'Invalid encrypte data')
    print('user inf has:',dir(_res))
    user = User.query.filter_by(openid = _openid).first()
    if not user:
        _location = '{country},{province},{city}'.format(country=_res.get('country'),province=_res.get('province'),city=_res.get('city'))
        user_new = User(location= _location,avatar_url=_res.get('avatarUrl'),open_id=_openid,gender=_res.get('gender'))
        _session_id = user_new.generate_auth_token()
        db.session.commit()
        return jsonify({'head':{},'info':{},'body':{'sessionId':_session_id}})
    else:
        _session_id = user.generate_auth_token()
        db.session.commit()
        return jsonify({'head':{},'info':{},'body':{'sessionId':_session_id}})

@api.route('/user/',methods=['GET','POST'])
def login():
    return jsonify({'head':{},'info':{},'body':{}})
