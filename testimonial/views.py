from family_web import app, db
from flask import render_template, url_for, session, request, redirect, flash
from user.decorators import require_login
from testimonial.models import Idol, Testimonial
from user.models import User
from main.models import Event
from testimonial.form import TestimonialForm

POSTS_PER_PAGE = 5

@app.route('/testimonial', methods=('GET', 'POST'))
@app.route('/testimonial/<int:page>', methods=('GET', 'POST'))
@require_login
def testimonial(page=1):
	current_user_id = User.query.filter_by(username=session.get('username')).first()
	next_event = Event.query.order_by(Event.id.desc()).first()
	if not next_event:
		flash("No events yet, please create the first event")
		return redirect(url_for('event'))
	idol = Idol.query.filter_by(event_id=next_event.id).first()
	idol_id = idol.id
	testimonials = Testimonial.query.filter_by(user_id=current_user_id.id, live=True).order_by(Testimonial.id.desc()).paginate(page, POSTS_PER_PAGE, False)
	if request.args.get('id'):
		del_id = request.args.get('id')
		tst_to_del = Testimonial.query.filter_by(id=del_id).first()
		if tst_to_del.user_id != current_user_id.id:
			flash("This is not your post to delete!")
			return redirect(url_for('testimonial'))
		else:
			tst_to_del.live = False
			db.session.commit()
			flash("Testimonial deleted!")
			return redirect(url_for('testimonial'))
	return render_template('testimonial/testimonial.html', testimonials=testimonials, idol_id=idol_id)


# adding testimonials - only allow for most recent event

@app.route('/add_testimonial/<int:idol_id>', methods=('GET', 'POST'))
@require_login
def add_testimonial(idol_id):
	form = TestimonialForm()
	idol = Idol.query.filter_by(id=idol_id, live=True).first_or_404()
	next_event = Event.query.order_by(Event.id.desc()).first()
	if idol.event_id != next_event.id:
		flash("That isn't the most recent event, you cannot add any more testimonials. You can only add testimonials for the idol of the most recent event!")
		return redirect(url_for('testimonial'))
	if form.validate_on_submit():
		user = User.query.filter_by(username=session.get('username')).first()
		event = Event.query.filter_by(id=idol.event_id).first()
		testimonial = Testimonial(user, idol, event, form.testimonial.data)
		db.session.add(testimonial)
		db.session.commit()
		flash("Added testimonial!")
		return redirect(url_for('testimonial'))
	return render_template('testimonial/add_testimonial.html', form=form, idol_id=idol_id, action='new') # action to allow editing (see html file)

@app.route('/edit_testimonial/<int:testimonial_id>', methods=('GET', 'POST'))
@require_login
def edit_testimonial(testimonial_id):
	user = User.query.filter_by(username=session.get('username')).first()
	testimonial = Testimonial.query.filter_by(id=testimonial_id).first_or_404()
	if user.id != testimonial.user_id:
		flash("You didn't write this testimonial")
		return redirect(url_for('testimonial'))
	form = TestimonialForm(obj=testimonial) # pre-fill the form to edit
	if form.validate_on_submit():
		form.populate_obj(testimonial) # replaces testimonial data with form data
		db.session.commit()
		flash("Edited Testimonial")
		return redirect(url_for('testimonial'))
	return render_template('testimonial/add_testimonial.html', form=form, idol_id=testimonial.idol_id, testimonial=testimonial, action=edit_testimonial)



@app.route('/idol')
@require_login
def idol():
	idols = Idol.query.filter_by(live=True)
	return render_template('testimonial/idoladmin.html', idols=idols)


@app.route('/idol_testimonials/<int:idol_id>')
@app.route('/idol_testimonials/<int:idol_id>/<int:page>')
@require_login
def idol_testimonials(idol_id, page=1):
	testimonials = Testimonial.query.filter_by(idol_id=idol_id, live=True).order_by(Testimonial.id.desc()).paginate(page, POSTS_PER_PAGE, False)
	idol = Idol.query.filter_by(id=idol_id).first()
	if request.args.get('id'):
		del_id = request.args.get('id')
		tst_to_del = Testimonial.query.filter_by(id=del_id).first()
		if session.get('is_admin') == False:
			flash("You need to be an admin to do this!")
			return redirect(url_for('idol_testimonials', idol_id=idol.id))
		else:
			tst_to_del.live = False
			db.session.commit()
			flash("Testimonial deleted!")
			return redirect(url_for('idol_testimonials', idol_id=idol.id))
	return render_template('testimonial/idol_testimonials.html', testimonials=testimonials, idol=idol)