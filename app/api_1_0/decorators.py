from functools import wraps
from flask import g
from .errors import forbidden,alert
from ..models import User

def permission_required(permission):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if not g.current_user.can(permission):
                return forbidden('Insufficient permissions')
            return f(*args, **kwargs)
        return decorated_function
    return decorator

def login_require(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        try:
            _session_id = g.body.get('session_id')
        except Exception:
            return alert(10002,'SessionId not found in post data')
        else:
            user = User.query.filter_by(session_id=_session_id).first()
            if not user:
                return alert(20002,'invalid sessionId, ')
            g.current_user = user
        return f(*args, **kwargs)
    return decorated