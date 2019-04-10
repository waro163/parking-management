# -*- coding: utf-8 -*-
from flask import jsonify, g, url_for, current_app,request
from .. import db
from ..models import  Order
from . import api
from .decorators import permission_required,login_require
from .errors import alert
from werkzeug.utils import secure_filename
import os.path

def allowed_file(filename):
    _extension = None
    _is_photo = False
    if '.' in filename:
        _extension = filename.rsplit('.',1)[1].lower()
        if _extension in current_app.config.get('ALLOWED_PHOTO_EXTENSIONS'):
            _is_photo = True
    return _is_photo,_extension

@api.route('/orders', methods = ['POST'])
@login_require
def get_orders():
    _orders = g.current_user.orders.all()
    return jsonify({
        'head':{'resultCode':'1'},
        'status':{'code':'','message': ''},
        'body':{'orders':[_order.to_json() for _order in _orders]}
    })

@api.route('order/pay',methods = ['POST'])
@login_require
def order_pay():
    _order_id = int(g.body.get('order_id'))
    _order = Order.query.get(_order_id)
    _order.pay_order()
    db.session.commit()
    return jsonify({
        'head': {'resultCode': '1'},
        'status': {'code': '', 'message': ''},
        'body': {'order':_order.to_json()}
    })

@api.route('order/upload',methods=['POST'])
@login_require
def upload_photo():
    if 'file' not in request.files:
        return alert(10016,'can not find the file in request')
    f = request.files['file']
    _order_id = g.body.get('order_id')
    if not f:
        return alert(20011,'file is none')
    _is_photo,_extension = allowed_file(f.filename)
    if not _is_photo:
        return alert(20012,'photo type is wrong')
    filename = _order_id + _extension
    filename = secure_filename(filename)
    f.save(current_app.config.get('UPLOAD_ROOT_FOLDER'),filename)

    return jsonify({
        'head': {'resultCode': '1'},
        'status': {'code': '', 'message': ''},
        'body': {'photo_url': url_for('static',filename=os.path.join(current_app.config.get('PHOTO_SUB_FOLDER'),filename),_external=True)}
    })