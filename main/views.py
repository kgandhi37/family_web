from family_web import app, db
from flask import render_template, url_for, session, request, redirect, flash
from user.decorators import require_login, require_user_admin, is_user_already_logged_in
from user.models import User
from main.models import Location, Event
from datetime import datetime
from main.form import LocationForm, EventForm, EventMediaForm
from testimonial.models import Idol
import string

@app.route('/')
@app.route('/index')
@is_user_already_logged_in
def index():
	return render_template('main/index.html')

@app.route('/home')
@require_login
def home():
	next_event = Event.query.order_by(Event.id.desc()).first()
	if not next_event:
		flash("No events yet, please create the first event")
		return redirect(url_for('event'))
	idol = Idol.query.filter_by(event_id=next_event.id).first()
	idol_id = idol.id
	current_date = datetime.utcnow()
	return render_template('main/home.html', next_event=next_event, idol_id=idol_id)

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

@app.route('/view_events')
@require_login
def view_events():
	events=Event.query.filter_by(live=True)
	return render_template('main/view_events.html', events=events)

@app.route('/event', methods=('GET', 'POST'))
@require_login
@require_user_admin
def event():
	form = EventForm()
	events=Event.query.filter_by(live=True)
	check_if_loc = Location.query.first()
	if not check_if_loc:
		flash("To create your first event, please first add a location!")
		return redirect(url_for('location'))
	if request.args.get('id'):
		del_id = request.args.get('id')
		event_to_del = Event.query.filter_by(id=del_id, live=True).first()
		idol_to_del = Idol.query.filter_by(event_id=del_id, live=True).first()
		event_to_del.live = False
		idol_to_del.live = False
		db.session.commit()
		flash("Event Deleted")
		return redirect(url_for('event'))
	if form.validate_on_submit():
		location = str(form.location.data)
		starters = str(form.starters.data)
		drinks = str(form.drinks.data)
		dessert = str(form.dessert.data)
		disposables = str(form.disposables.data)
		idol = str(form.idol.data)
		user = User.query.filter_by(username=idol).first()
		idol_check=Idol.query.filter_by(user_id=user.id, live=True).first()
		if idol_check:
			flash("This person has already been the subject of an event, please choose someone else.")
			return redirect(url_for('event'))
		else:
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
				idol,
				add_info
				)
			db.session.add(event)
			db.session.flush()
			# creating idol
			if event.id:
				event_idol=Idol(user, event) # adding whole query - auto gets the Primary Key
				db.session.add(event_idol)
				db.session.flush()
			else:
				db.session.rollback()
				flash("Error creating Event")
			if event.id and event_idol.id:
				db.session.commit()
				flash("Event Added")
				return redirect(url_for('event'))
			else:
				db.session.rollback()
				flash("Error creating Event")

	return render_template('main/event.html', form=form, events=events, action='new')


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
