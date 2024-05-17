from functools import wraps
from flask import jsonify, request
from .util import *
from flask_jwt_extended import verify_jwt_in_request
from flask_jwt_extended import get_jwt

def admin_required():
    def wrapper(fn):
        @wraps(fn)
        def decorator(*args, **kwargs):
            verify_jwt_in_request()
            claims = get_jwt()
            if "role" in claims and claims['role'] == 'admin':
                if 'info' in claims:
                    return claims['info']
                else:
                    return fn(*args, **kwargs)
            else:
                return jsonify(msg="Admins only!"), 403
        return decorator
    return wrapper

def doctor_required():
    def wrapper(fn):
        @wraps(fn)
        def decorator(*args, **kwargs):
            verify_jwt_in_request()
            claims = get_jwt()
            if "role" in claims and claims['role'] == 'doctor':
                if 'info' in claims:
                    return claims['info']
                else:
                    return fn(*args, **kwargs)
            else:
                return jsonify(msg="Doctors only!"), 403
        return decorator
    return wrapper

def nurse_required():
    def wrapper(fn):
        @wraps(fn)
        def decorator(*args, **kwargs):
            verify_jwt_in_request()
            claims = get_jwt()
            if "role" in claims and claims['role'] == 'nurse':
                if 'info' in claims:
                    return claims['info']
                else:
                    return fn(*args, **kwargs)
            else:
                return jsonify(msg="Nurse only!"), 403
        return decorator
    return wrapper

def triage_required():
    def wrapper(fn):
        @wraps(fn)
        def decorator(*args, **kwargs):
            verify_jwt_in_request()
            claims = get_jwt()
            if "triage" in claims:
                if claims["triage"]:
                    return fn(*args, **kwargs)
            else:
                return jsonify(msg="Triage only!"), 403
        return decorator
    return wrapper