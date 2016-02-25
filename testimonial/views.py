from family_web import app, db
from flask import render_template, url_for, session, request, redirect, flash
from user.decorators import require_login, require_user_admin, is_user_already_logged_in
from testimonial.models import Idol, Testimonial
from user.models import User
from main.models import Event
from testimonial.form import TestimonialForm

POSTS_PER_PAGE = 5

@app.route('/testimonial')
@app.route('/testimonial/<int:page>')
@require_login
def testimonial(page=1):
	current_user_id = User.query.filter_by(username=session.get('username')).first()
	next_event = Event.query.order_by(Event.id.desc()).first()
	idol = Idol.query.filter_by(event_id=next_event.id).first()
	idol_id = idol.id
	testimonials = Testimonial.query.filter_by(user_id=current_user_id.id).order_by(Testimonial.id.desc()).paginate(page, POSTS_PER_PAGE, False)
	return render_template('testimonial/testimonial.html', testimonials=testimonials, idol_id=idol_id)


# adding testimonials - currently links with home as can only add testimonial for the idol of the next event. 
# future work, logged in users will be able to see all the previous events. link to there after. 

@app.route('/add_testimonial/<int:idol_id>', methods=('GET', 'POST'))
@require_login
def add_testimonial(idol_id):
	form = TestimonialForm()
	idol = Idol.query.filter_by(id=idol_id, live=True).first()
	next_event = Event.query.order_by(Event.id.desc()).first()
	if idol.event_id != next_event.id:
		flash("That isn't the most recent event, you cannot add any more testimonials. You can only add testimonials for the idol of the most recent event!")
		return redirect(url_for('testimonial'))
	if idol:
		if form.validate_on_submit():
			user = User.query.filter_by(username=session.get('username')).first()
			event = Event.query.filter_by(id=idol.event_id).first()
			testimonial = Testimonial(user, idol, event, form.testimonial.data)
			db.session.add(testimonial)
			db.session.commit()
			flash("Added testimonial!")
			return redirect(url_for('testimonial'))
	else:
		flash("No such Idol!")
		return redirect(url_for('home'))
	return render_template('testimonial/add_testimonial.html', form=form, idol_id=idol_id)


@app.route('/idol')
@require_login
def idol():
	idols = Idol.query.filter_by(live=True)
	return render_template('testimonial/idoladmin.html', idols=idols)
