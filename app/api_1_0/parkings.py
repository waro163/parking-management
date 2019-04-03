# -*- coding: utf-8 -*-
from flask import jsonify, g, url_for, current_app
from .. import db
from ..models import ParkingS,Order
from . import api
from .decorators import permission_required,login_require
from .errors import alert
from ..utils import getRectRange

@api.route('/parkings', methods = ['POST'])
@login_require
def get_parkings():
    _latitude = g.body.get('latitude')
    _longitude = g.body.get('longitude')
    _distance = g.body.get('distance',5)
    maxLat, minLat, maxLon, minLon = getRectRange(_latitude,_longitude,_distance)
    parkings = ParkingS.query.filter_by(latitude >= minLat, latitude < maxLat, longitude >= minLon, longitude < maxLon).all()
    return jsonify({
        'head':{'resultCode':'1'},
        'status':{'code':'','message': ''},
        'body':{parking.to_json() for parking in parkings}
        })

@api.route('/parkings/ping', methods = ['GET','POST'])
def parkings_ping():
    _parking_id = g.body.get('parking_id')
    _parking = ParkingS.query.get(_parking_id)
    if not _parking:
        alert(10002,'the parking id is wrong')
    _parking_status = _parking.ping()
    db.session.commit()
    return jsonify({
        'head':{'resultCode':'1'},
        'status':{'code':'','message': ''},
        'body':{'parking_status':_parking_status}
    })

@api.route('/parkings/unlock',methods = ['POST'])
def parking_unlock():
    _parking_id = g.body.get('parking_id')
    _parking = ParkingS.query.get(_parking_id)
    if not _parking:
        alert(10002,'the parking number is not exist')
    if _parking.islocked():
        _parking_status = _parking.unlock()
        _order = Order(user=g.current_user,parking=_parking)#创建用户订单
        db.session.add(_order)
        db.session.commit()
        return jsonify({
            'head':{'resultCode':'1'},
            'status':{'code':'','message': ''},
            'body':{'order_id':_order.id,'parking_status':_parking_status,'parking_id':_parking_id}
        })
    return alert(20007,'the parking space had been unlocked by other people')

@api.route('/parkings/lock',methods = ['POST'])
def parking_lock():
    _parking_id = g.body.get('parking_id')
    _order_id = g.body.get('order_id')
    _parking = ParkingS.query.get(_parking_id)
    _order = Order.query.get(_order_id)
    if not _parking:
        return alert(10009,'parking number is not exist')
    if not _order:
        return alert(10010,'order number is not exist')
    _parking.lock()
    _price_minute = _parking.get_price()

    return jsonify({
        'head': {'resultCode': '1'},
        'status': {'code': '', 'message': ''},
        'body': {'parking_status': 0}
    })

@api.route('parkings/rating',methods = ['POST'])
def parking_rating():
    return jsonify({
        'head': {'resultCode': '1'},
        'status': {'code': '', 'message': ''},
        'body': {'parking_status': 0}
    })