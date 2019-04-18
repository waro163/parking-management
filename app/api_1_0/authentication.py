# -*- coding: utf-8 -*-
from flask import g, jsonify, request
from flask_httpauth import HTTPBasicAuth
from functools import wraps
from ..models import User,AnonymousUser
from . import api
from .errors import unauthorized, alert
import json

# auth = HTTPBasicAuth()
#
# @auth.verify_password
# def verify_password(email_or_token, password):
#     if email_or_token == '':
#         return False
#     if password == '':
#         g.current_user = User.verify_auth_token(email_or_token)
#         g.token_used = True
#         return g.current_user is not None
#     user = User.query.filter_by(email=email_or_token).first()
#     if not user:
#         return False
#     g.current_user = user
#     g.token_used = False
#     return user.verify_password(password)
#
#
# @auth.error_handler
# def auth_error():
#     return unauthorized('Invalid credentials')
#
# @api.before_request
# @auth.login_required
# def before_request():
#     if not g.current_user.is_anonymous and \
#             not g.current_user.confirmed:
#         return forbidden('Unconfirmed account')

@api.before_request
def before_request():
    g.request = request
    g.current_user = AnonymousUser()
    g.head = {}
    g.body = {}
    print('request.data:', request.data)
    print('request.json:', request.json)
    try:
        _request_head = request.json.get('head')
        _request_body = request.json.get('body')
    except Exception as e:
        print("before request",e)
    else:
        print(_request_head,_request_body)
        g.head = _request_head
        g.body = _request_body