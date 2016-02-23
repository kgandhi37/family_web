from family_web import app, db
from flask import render_template, url_for, session, request, redirect, flash
from user.decorators import require_login, require_user_admin, is_user_already_logged_in
from user.models import User

@app.route('/')
@app.route('/index')
def index():
	if (session.get('username')):
		return redirect(url_for('home'))
	return render_template('main/index.html')

@app.route('/home')
@require_login
def home():
	return render_template('main/home.html')

@app.route('/userlist', methods=('GET', 'POST'))
@require_login
def userlist():
	users = User.query
	if (request.args.get('id')):
		if (session.get('is_admin') is False):
			flash("You need to be an admin to complete this action")
			return redirect(url_for('userlist'))
		else:
			target_id = request.args.get('id')
			target_user = User.query.filter_by(id=target_id).first()
			if (target_user.is_admin is False):
				target_user.is_admin = True
				db.session.commit()
				flash(target_user.username + " is now an Admin")
				return redirect(url_for('userlist'))
			else:
				if session.get('username') == target_user.username:
					flash("You can't de-admin yourself")
					return redirect(url_for('userlist'))
				else:
					target_user.is_admin = False
					db.session.commit()
					flash(target_user.username + " has been removed as Admin")
					return redirect(url_for('userlist'))
	return render_template('main/user_list.html', users=users)
