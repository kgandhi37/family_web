from family_web import app, db
from flask import render_template, url_for, session, request, redirect, flash, abort
from user.models import User
from user.form import LoginForm, RegisterForm, ChangePassForm, LostPasswordForm, ResetPasswordForm
from user.decorators import require_login, require_user_admin, is_user_already_logged_in
from global_functions import send_email
import string, random, bcrypt, socket

# random string function
def pass_generator(size=8, chars=string.ascii_uppercase + string.digits + string.ascii_lowercase):
	return ''.join(random.choice(chars) for _ in range(size))

@app.route('/initial', methods=('GET', 'POST'))
@is_user_already_logged_in
def initial():
	user = User.query.first()
	form = RegisterForm()
	if user:
		abort(403)
	else:
		if form.validate_on_submit():
			salt = bcrypt.gensalt()
			hashed_password = bcrypt.hashpw(form.password.data, salt)
			fullname = string.capwords(form.fullname.data)
			user = User(
				fullname,
				form.email.data,
				form.username.data.lower(),
				hashed_password,
				True
				)
			db.session.add(user)
			db.session.commit()
			flash("User Registered, app initialised.")
			return redirect(url_for('login'))
	return render_template('user/initial.html', form=form)

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
				user.req_lost_pass = False
				db.session.commit()
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

@app.route('/lostpass', methods=('GET','POST'))
@is_user_already_logged_in
def lostpass():
	form = LostPasswordForm()
	error = None
	if form.validate_on_submit():
		# check if email exists
		user = User.query.filter_by(email=form.email.data).first()
		if not user:
			error = "No such email registered"
		else:
			if user.req_lost_pass is True:
				error = "You've already requested a lost password for this user, please check your email or if this was sent by mistake please login"
			else:
				# get random string as unique code lost_pass_code
				unique_code = pass_generator()
				user.req_lost_pass = True
				user.lost_pass_code = unique_code
				db.session.commit()
				current_ip = socket.gethostbyname(socket.gethostname())
				email_subj = "Lost Password - GandhiWeb"
				email_body = "You've just requested to reset your password from IP " + current_ip + ". If this is not the case please login and this will expire. If you indeed have lost your password please go to the forgotten password page where you requested this from and follow the link on there to the reset password page and use the unique code: " + unique_code + " . Thanks, Kishen"
				send_email(user.email, email_subj, email_body)
				flash("New password requested")
				return redirect(url_for('lostpass'))

	return render_template('user/lostpass.html', form=form, error=error)

@app.route('/reset_pass', methods=('GET', 'POST'))
@is_user_already_logged_in
def reset_pass():
	form = ResetPasswordForm()
	error = None
	if form.validate_on_submit():
		user = User.query.filter_by(email=form.email.data).first()
		if not user:
			error = "No such email"
		else:
			if user.req_lost_pass is False:
				error = "This user hasn't requested a changed password"
			else:
				if form.unique_code.data != user.lost_pass_code:
					error = "Unique code doesn't match"
				else:
					salt = bcrypt.gensalt()
					new_hashed_password = bcrypt.hashpw(form.password.data, salt)
					user.password = new_hashed_password
					user.req_lost_pass = False
					db.session.commit()
					current_ip = socket.gethostbyname(socket.gethostname())
					email_subj = "Password Reset - GandhiWeb"
					email_body = "You just Reset your password on GandhiWeb, if this is not the case please contact Kishen. IP address used to reset password: " + current_ip
					send_email(user.email, email_subj, email_body)
					flash("Password reset succesfully, please login again with new password")
					return redirect(url_for('index'))
	return render_template('user/resetpass.html', form=form, error=error)






