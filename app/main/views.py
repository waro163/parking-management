# -*- coding: utf-8 -*-
from . import main
from flask import request,url_for,make_response,jsonify,render_template
from .. import db
from ..models import Permission,Role,User

@main.route('/')
def index():
    # response=jsonify({'message':'Hello World!'})
    # return response
    return render_template('index.html')



