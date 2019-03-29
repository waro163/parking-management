from flask import Blueprint

api = Blueprint('api',__name__)

from . import authentication,views,users,posts,comments,errors