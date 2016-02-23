from family_web import app, db
from flask import render_template, url_for, session, request, redirect, flash
from user.models import User
from user.form import LoginForm, RegisterForm, ChangePassForm
from user.decorators import require_login, require_user_admin, is_user_already_logged_in
from global_functions import send_email
import string
import bcrypt
import socket

@app.route('/login', methods=('GET','POST'))
@is_user_already_logged_in
def login():
	form = LoginForm()
	error = None
	# checking is user has been redirected to login to send back to correct page after logged in
	if request.method == 'GET' and request.args.get('next'):
		session['next'] = request.args.get('next', None)
    	
	# if form is correctly posted: login checks
	if form.validate_on_submit():
		user = User.query.filter_by(username=form.username.data).first()
		if user:
			if bcrypt.hashpw(form.password.data, user.password) == user.password:
				session['username'] = form.username.data.lower()
				session['fullname'] = user.fullname
				session['is_admin'] = user.is_admin
				flash("Logged in")
				if 'next' in session:
					next = session.get('next')
					session.pop('next')
					return redirect(next)
				else:	
					return redirect(url_for('index'))
			else:
				error = "Incorrect Username and/or Password"

		else:
			error = "Incorrect Username and/or Password"

	return render_template('user/login.html', form=form, error=error)


@app.route('/register', methods=('GET','POST'))
@require_login
@require_user_admin
def register():
	form = RegisterForm()
	if form.validate_on_submit():
		salt = bcrypt.gensalt()
		hashed_password = bcrypt.hashpw(form.password.data, salt)
		fullname = string.capwords(form.fullname.data)
		user = User(
			fullname,
			form.email.data,
			form.username.data.lower(),
			hashed_password,
			False
			)
		db.session.add(user)
		db.session.commit()
		flash("User Registered!")
		return redirect(url_for('register'))
	return render_template('user/register.html', form=form)

@app.route('/logout')
@require_login
def logout():
	session.pop('username')
	session.pop('fullname')
	session.pop('is_admin')
	flash("Logged out")
	return redirect(url_for('login'))

@app.route('/changepass', methods=('GET', 'POST'))
@require_login
def changepass():
	form = ChangePassForm()
	error = None
	if form.validate_on_submit():
		user = User.query.filter_by(username=session.get('username')).first()
		hashed_password = bcrypt.hashpw(form.old_password.data, user.password)
		if form.old_password.data == form.password.data:
			error = "New password can't be the same as the old one"
		else:
			if hashed_password == user.password:
				salt = bcrypt.gensalt()
				new_hashed_password = bcrypt.hashpw(form.password.data, salt)
				user.password = new_hashed_password
				db.session.commit()
				current_ip = socket.gethostbyname(socket.gethostname())
				email_subj = "Password change - GandhiWeb"
				email_body = "You just changed your password on GandhiWeb, if this is not the case please contact Kishen. IP address used to change password: " + current_ip
				send_email(user.email, email_subj, email_body)
				flash("Password changed succesfully, please login again with new password")
				session.pop('username')
				session.pop('fullname')
				session.pop('is_admin')
				return redirect(url_for('index'))

			else:
				error = "Incorrect old password"
	return render_template('user/changepass.html', form=form, error=error)




