from family_web import app, db
from flask import render_template, url_for, session, request, redirect, flash
from user.decorators import require_login, require_user_admin, is_user_already_logged_in
from testimonial.models import Idol, Testimonial
from user.models import User
from main.models import Event

@app.route('/testimonial')
@require_login
def testimonial():
	return "Works"

@app.route('/idol')
@require_login
def idol():
	idols = Idol.query.filter_by(live=True)
	return render_template('testimonial/idoladmin.html', idols=idols)
