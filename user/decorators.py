# creating decorators for checking whether logged in etc

from functools import wraps
from flask import session, request, redirect, url_for, abort, flash

def require_login(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get('username') is None:
            flash("You need to be logged in to view this page")
            return redirect(url_for('login', next=request.url))
        return f(*args, **kwargs)
    return decorated_function

def require_user_admin(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get('is_admin') is False:
            abort(403)
        return f(*args, **kwargs)
    return decorated_function

def is_user_already_logged_in(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get('username'):
            flash("You are already logged in! Please logout first.")
            return redirect(url_for('index'))
        return f(*args, **kwargs)
    return decorated_function