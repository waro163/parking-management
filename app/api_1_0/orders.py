# -*- coding: utf-8 -*-
from flask import jsonify, request, g, url_for, current_app
from .. import db
from ..models import  Permission
from . import api
from .decorators import permission_required,login_require
from .errors import forbidden

@api.route('/orders', methods = ['POST'])
@login_require
def get_orders():

    return jsonify({'head':{'resultCode':'1'},'status':{'code':'','message': ''},'body':{}})