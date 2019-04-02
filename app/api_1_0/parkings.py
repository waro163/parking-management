# -*- coding: utf-8 -*-
from flask import jsonify, request, g, url_for, current_app
from .. import db
from ..models import ParkingS
from . import api
from .decorators import permission_required,login_require
from .errors import alert
from ..utils import getRectRange

@api.route('/parkings', methods = ['POST'])
@login_require
def get_parkings():
    _latitude = g.body.get('latitude')
    _longtitude = g.body.get('longtitude')
    _distance = g.body.get('distance',5)
    maxLat, minLat, maxLon, minLon = getRectRange(_latitude,_longtitude,_distance)
    parkings = ParkingS.query.filter_by(latitude >= minLat, latitude < maxLat, longtitude >= minLon, longtitude < maxLon).all()
    return jsonify({
        'head':{'resultCode':'1'},
        'status':{'code':'','message': ''},
        'body':{parking.to_json() for parking in parkings}
        })

@api.route('/parkings/ping', methods = ['GET','POST'])
def parkings_ping():
    parking_id = g.body.get('id')
    parking = ParkingS.query.get(parking_id)
    if not parking:
        alert(10002,'the parking id is wrong')


    return jsonify({'head':{'resultCode':'1'},'status':{'code':'','message': ''},'body':{}})