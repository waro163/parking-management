# -*- coding: utf-8 -*-
from flask import jsonify, g, url_for, current_app
from .. import db
from ..models import  Order
from . import api
from .decorators import permission_required,login_require
from .errors import forbidden

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