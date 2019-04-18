# -*- coding: utf-8 -*-
from flask import jsonify, g, url_for, current_app, request
from .. import db
from ..models import ParkingS,Order
from . import api
from .decorators import permission_required,login_require
from .errors import alert
from ..utils import getRectRange

@api.route('/parkings', methods = ['POST'])
@login_require
def get_parkings():
    try:
        _latitude = float(g.body.get('latitude'))
        _longitude = float(g.body.get('longitude'))
        _distance = float(g.body.get('distance',5))
    except Exception as e:
        return alert(10002, 'the latitude/longitude/distance is wrong')
    maxLat, minLat, maxLon, minLon = getRectRange.GetRectRange(_latitude,_longitude,_distance)
    # print(maxLat,minLat,maxLon,minLon)
    parkings = ParkingS.query.filter(ParkingS.latitude >= minLat, ParkingS.latitude < maxLat, ParkingS.longitude >= minLon, ParkingS.longitude < maxLon).all()
    return jsonify({
        'head': {'resultCode': '1'},
        'status': {'code': '', 'message': ''},
        'body': {'parkings': [parking.to_json() for parking in parkings]}
    })

@api.route('/parkings/ping', methods = ['POST'])
def parkings_ping():
    try:
        _parking_id = int(g.body.get('parking_id'))
    except Exception as e:
        return alert(10002, 'the parking id is wrong')
    _parking = ParkingS.query.get(_parking_id)
    if not _parking:
        return alert(10002,'the parking id is wrong')
    _parking_status = _parking.ping()
    db.session.commit()
    return jsonify({
        'head':{'resultCode':'1'},
        'status':{'code':'','message': ''},
        'body':{'parking_status':_parking_status}
    })

@api.route('/parking/ping', methods = ['GET'])
def parkings_ping_get():
    try:
        _parking_id = int(request.args.get('parking_id'))
    except Exception as e:
        return alert(10002, 'the parking id is wrong')
    _parking = ParkingS.query.get(_parking_id)
    if not _parking:
        return alert(10002,'the parking id is wrong')
    _parking_status = _parking.ping()
    db.session.commit()
    return jsonify({
        'head':{'resultCode':'1'},
        'status':{'code':'','message': ''},
        'body':{'parking_status':_parking_status}
    })

@api.route('/parkings/unlock',methods = ['POST'])
@login_require
def parking_unlock():
    try:
        _parking_id = int(g.body.get('parking_id'))
    except Exception as e:
        return alert(10002, 'parking id is wrong')
    _parking = ParkingS.query.get(_parking_id)
    if not _parking:
        return alert(10002,'the parking number is not exist')
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
@login_require
def parking_lock():
    try:
        _parking_id = int(g.body.get('parking_id'))
    except Exception as e:
        return alert(10002, 'the parking_id/order_id is wrong')
    _parking = ParkingS.query.get(_parking_id)
    _order = _parking.orders.filter(Order.parkout_time.is_(None)).first()
    print('order id',_order.id)
    if not _parking:
        return alert(10009,'parking number is not exist')
    if not _order:
        return alert(10010,'order number is not exist')
    if _parking.islocked():
        return alert(200010,'the parking zone had beed locked')
    _parking.lock()
    _price_minute = _parking.get_price()
    _order.finalize_order(_price_minute)
    db.session.commit()
    _order_data = _order.to_json()
    _order_data.update(_parking.to_json())
    return jsonify({
        'head': {'resultCode': '1'},
        'status': {'code': '', 'message': ''},
        'body': {'order': _order_data}
    })

@api.route('parkings/rating',methods = ['POST'])
@login_require
def parking_rating():
    try:
        _order_id = int(g.body.get('order_id'))
        _star = int(g.body.get('score'))
        _comment = g.body.get('comment')
    except Exception as e:
        return alert(10002, 'order_id/score is wrong')
    _order = Order.query.get(_order_id)
    if not _order:
        return alert(10010,'order number is not exist')
    _order.rate_order(_star,_comment)
    db.session.commit()
    return jsonify({
        'head': {'resultCode': '1'},
        'status': {'code': '', 'message': ''},
        'body': {}
    })

@api.route('parkings/status',methods = ['POST'])
@login_require
def parkings_status():
    all_parkings = ParkingS.query.all()
    return jsonify({
        'head': {'resultCode': '1'},
        'status': {'code': '', 'message': ''},
        'body': {'parkings': [parking.to_json() for parking in all_parkings]}
    })