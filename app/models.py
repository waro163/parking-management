from datetime import datetime
import time,random
from werkzeug.security import generate_password_hash, check_password_hash
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flask import current_app, request, url_for
from flask_login import UserMixin, AnonymousUserMixin
from app.exceptions import ValidationError
from . import db, login_manager


class Permission:
    FOLLOW = 1
    COMMENT = 2
    WRITE = 4
    MODERATE = 8
    ADMIN = 16

class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    default = db.Column(db.Boolean, default=False, index=True)
    permissions = db.Column(db.Integer)
    users = db.relationship('User', backref='role', lazy='dynamic')

    def __init__(self, **kwargs):
        super(Role, self).__init__(**kwargs)
        if self.permissions is None:
            self.permissions = 0

    @staticmethod
    def insert_roles():
        roles = {
            'User': [Permission.FOLLOW, Permission.COMMENT, Permission.WRITE],
            'Moderator': [Permission.FOLLOW, Permission.COMMENT,
                          Permission.WRITE, Permission.MODERATE],
            'Administrator': [Permission.FOLLOW, Permission.COMMENT,
                              Permission.WRITE, Permission.MODERATE,
                              Permission.ADMIN],
        }
        default_role = 'User'
        for r in roles:
            role = Role.query.filter_by(name=r).first()
            if role is None:
                role = Role(name=r)
            role.reset_permissions()
            for perm in roles[r]:
                role.add_permission(perm)
            role.default = (role.name == default_role)
            db.session.add(role)
        db.session.commit()

    def add_permission(self, perm):
        if not self.has_permission(perm):
            self.permissions += perm

    def remove_permission(self, perm):
        if self.has_permission(perm):
            self.permissions -= perm

    def reset_permissions(self):
        self.permissions = 0

    def has_permission(self, perm):
        return self.permissions & perm == perm

    def __repr__(self):
        return '<Role %r>' % self.name



class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(64), unique=True, index=True)
    phone_number = db.Column(db.String(64),index=True)
    username = db.Column(db.String(64), index=True)
    password_hash = db.Column(db.String(128))
    token = db.Column(db.String(6))#发送给用户的邮件确认验证码或手机确认验证码
    email_confirmed = db.Column(db.Boolean, default=False)
    phone_number_confirmed = db.Column(db.Boolean, default=False)
    location = db.Column(db.String(64))
    about_me = db.Column(db.Text())
    avatar_url = db.Column(db.String(128))#头像
    gender = db.Column(db.Integer)#性别
    session_id = db.Column(db.String(32),unique=True)#服务器与客户端的临时session
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))
    orders = db.relationship('Order',backref = 'user',lazy = 'dynamic')


    def __init__(self, **kwargs):
        super(User, self).__init__(**kwargs)
        if self.role is None:
            if self.email == current_app.config['FLASKY_ADMIN']:
                self.role = Role.query.filter_by(name='Administrator').first()
            if self.role is None:
                self.role = Role.query.filter_by(default=True).first()

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    def generate_confirmation_token(self, expiration=3600):
        _token = ''
        for i in range(6):
            _token += str(random.randint(0,9))
        self.token = _token
        db.session.add(self)
        return _token

    def confirm(self, token):
        if self.token != token:
            return False
        self.email_confirmed = True
        db.session.add(self)
        return True

    def generate_reset_token(self, expiration=3600):
        s = Serializer(current_app.config['SECRET_KEY'], expiration)
        return s.dumps({'reset': self.id}).decode('utf-8')

    @staticmethod
    def reset_password(token, new_password):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token.encode('utf-8'))
        except:
            return False
        user = User.query.get(data.get('reset'))
        if user is None:
            return False
        user.password = new_password
        db.session.add(user)
        return True

    def generate_email_change_token(self, new_email, expiration=3600):
        s = Serializer(current_app.config['SECRET_KEY'], expiration)
        return s.dumps(
            {'change_email': self.id, 'new_email': new_email}).decode('utf-8')

    def change_email(self, token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token.encode('utf-8'))
        except:
            return False
        if data.get('change_email') != self.id:
            return False
        new_email = data.get('new_email')
        if new_email is None:
            return False
        if self.query.filter_by(email=new_email).first() is not None:
            return False
        self.email = new_email
        self.avatar_hash = self.gravatar_hash()
        db.session.add(self)
        return True

    def can(self, perm):
        return self.role is not None and self.role.has_permission(perm)

    def is_administrator(self):
        return self.can(Permission.ADMIN)

    def ping(self):
        self.last_seen = datetime.utcnow()
        db.session.add(self)

    def gravatar(self, url):
        self.avatar_url = url
        db.session.add(self)

    def to_json(self):
        json_user = {
            'url': url_for('api.get_user', id=self.id,_external=True),
            'username': self.username,
            'member_since': self.member_since,
            'last_seen': self.last_seen,
            'posts_url': url_for('api.get_user_posts', id=self.id),
            'followed_posts_url': url_for('api.get_user_followed_posts',
                                          id=self.id),
            'post_count': self.posts.count()
        }
        return json_user

    def generate_session_token(self, expiration=3600):
        s = Serializer(current_app.config['SECRET_KEY'],
                       expires_in=expiration)
        self.session_id = s.dumps({'id': self.id}).decode('utf-8')
        db.session.add(self)
        return self.session_id

    def __repr__(self):
        return '<User %r>' % self.username


class AnonymousUser(AnonymousUserMixin):
    def can(self, permissions):
        return False

    def is_administrator(self):
        return False

login_manager.anonymous_user = AnonymousUser


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class Order(db.Model):#订单
    __tablename__ = 'orders'
    id = db.Column(db.Integer,primary_key=True)
    parkin_time = db.Column(db.DateTime(), default=datetime.now)
    parkout_time = db.Column(db.DateTime())
    parktotal_time = db.Column(db.Float)
    pay_money = db.Column(db.Float)
    is_paied = db.Column(db.Boolean,default=False)
    score = db.Column(db.Integer)
    comment = db.Column(db.String(128))
    parking_id = db.Column(db.Integer,db.ForeignKey('parkings.id'))
    user_id = db.Column(db.Integer,db.ForeignKey('users.id'))

    def finalize_order(self,price):
        self.parkout_time = datetime.now()
        self.parktotal_time = (self.parkout_time-self.parkin_time).seconds/60.0
        self.pay_money = price * self.parktotal_time
        db.session.add(self)

    def pay_order(self):
        self.is_paied = True
        db.session.add(self)
        return self.is_paied

    def rate_order(self,score,comment):
        self.score = score
        self.comment = comment
        db.session.add(self)

    def to_json(self):
        order = {
            'order_id':self.id,
            'parkin_time':self.parkin_time,
            'parkout_time':self.parkout_time,
            'money':self.pay_money,
            'is_paied':self.is_paied,
            'score':self.score,
            'comment':self.comment
        }
        return order

    def __repr__(self):
        return '<Order %r>' % self.id

class ParkingS(db.Model):#停车位
    __tablename__ = 'parkings'
    id = db.Column(db.Integer, primary_key=True)
    longitude = db.Column(db.Float ,nullable=False)
    latitude = db.Column(db.Float , nullable=False)
    price_minute = db.Column(db.Float, nullable=False)
    last_seen = db.Column(db.DateTime(),default=datetime.now)
    park_status = db.Column(db.Boolean,default=False)
    online_status = db.Column(db.Boolean,default=True)
    orders = db.relationship('Order',backref='parking',lazy = 'dynamic')

    @staticmethod
    def insert_parkings(file_name):
        with open(file_name) as f:
            for _each_line in f:
                format_line = _each_line.strip()
                if not format_line.startswith('#'):
                    data_line = format_line.split('#')[0]
                    _lat,_lon,_pri = [ data.strip() for data in data_line.split(',')]
                    if _lon and _lat and _pri:
                        _lon = float(_lon)
                        _lat = float(_lat)
                        _pri = float(_pri)
                        _parking = ParkingS(longitude=_lon,latitude=_lat,price_minute=_pri)
                        db.session.add(_parking)
            db.session.commit()
        f.close()

    def lock(self):
        self.park_status = False
        db.session.add(self)
        return self.park_status

    def islocked(self):
        return not self.park_status

    def unlock(self):
        self.park_status = True
        db.session.add(self)
        return self.park_status

    def ping(self):
        self.last_seen = datetime.utcnow()
        self.online_status = True
        db.session.add(self)
        return self.park_status

    def get_price(self):
        return self.price_minute

    def to_json(self):
        parking = {
            'parking_id' : self.id,
            'park_status' : self.park_status,
            'online_status' : self.online_status,
            'latitude' : self.latitude,
            'longitude' : self.longitude,
            'price_minute' : self.price_minute
        }
        return parking

    def __repr__(self):
        return '<Parking %r>' % self.id
