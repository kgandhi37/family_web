from family_web import app, db
from flask import render_template, url_for, session, request, redirect, flash
from user.decorators import require_login, require_user_admin, is_user_already_logged_in
from user.models import User
from main.models import Location, Event
from datetime import datetime
from main.form import LocationForm, EventForm, EventMediaForm
import string

@app.route('/')
@app.route('/index')
def index():
	if (session.get('username')):
		return redirect(url_for('home'))
	return render_template('main/index.html')

@app.route('/home')
@require_login
def home():
	next_event = Event.query.order_by(Event.id.desc()).first()
	current_date = datetime.utcnow()
	return render_template('main/home.html', next_event=next_event)

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
				elif target_user.username == "kishen":
					flash("Sorry you can't de-admin Kishen, he runs things around here")
					return redirect(url_for('userlist'))
				else:	
					target_user.is_admin = False
					db.session.commit()
					flash(target_user.username + " has been removed as Admin")
					return redirect(url_for('userlist'))
	return render_template('main/user_list.html', users=users)

@app.route('/location', methods=('GET', 'POST'))
@require_login
@require_user_admin
def location():
	form = LocationForm()
	locations = Location.query
	if request.args.get('id'):
		del_id = request.args.get('id')
		Location.query.filter_by(id=del_id).delete()
		db.session.commit()
		flash("Location Deleted")
		return redirect(url_for('location'))
	if form.validate_on_submit():
		location = Location(form.location.data, form.address.data)
		db.session.add(location)
		db.session.commit()
		flash("Location added")
		return redirect(url_for('location'))
	return render_template('main/locations.html', form=form, locations=locations)

@app.route('/event', methods=('GET', 'POST'))
@require_login
@require_user_admin
def event():
	form = EventForm()
	events=Event.query
	if request.args.get('id'):
		del_id = request.args.get('id')
		Event.query.filter_by(id=del_id).delete()
		db.session.commit()
		flash("Event Deleted")
		return redirect(url_for('event'))
	if form.validate_on_submit():
		location = str(form.location.data)
		starters = str(form.starters.data)
		drinks = str(form.drinks.data)
		dessert = str(form.dessert.data)
		disposables = str(form.disposables.data)
		if form.add_info.data:
			add_info = form.add_info.data
		else:
			add_info = "No Additional Information"
		event = Event(
			location,
			form.the_round.data,
			form.date.data,
			form.theme.data,
			starters,
			drinks,
			dessert,
			disposables,
			str(form.idol.data),
			add_info
			)
		db.session.add(event)
		db.session.commit()
		flash("Event Added")
		return redirect(url_for('event'))
	return render_template('main/event.html', form=form, events=events)

@app.route('/eventmedia/<int:event_id>', methods=('GET', 'POST'))
@require_login
@require_user_admin
def eventmedia(event_id):
	form = EventMediaForm()
	event = Event.query.filter_by(id=event_id).first_or_404()
	if form.validate_on_submit():
			event.media_link = form.media_link.data
			db.session.commit()
			flash("Media Link Added")
			return redirect(url_for('event'))
	return render_template('main/eventmediaform.html', form=form, event=event)
