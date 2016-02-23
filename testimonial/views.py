from family_web import app, db
from flask import render_template, url_for, session, request, redirect, flash

@app.route('/')
@app.route('/index')
def index():
	if (session.get('username')):
		return redirect(url_for('changepass'))
	return render_template('testimonial/index.html')
