from family_web import db
from datetime import datetime

# Defining Testimonial DB structure

class Testimonial(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
	idol_id = db.Column(db.Integer, db.ForeignKey('idol.id')) 
	event_id = db.Column(db.Integer, db.ForeignKey('event.id'))
	testimonial = db.Column(db.Text)
	date = db.Column(db.DateTime)
	live = db.Column(db.Boolean)	

	def __init__(self, user, idol, event, testimonial, date=None, live=True):
		self.user_id = user.id
		self.idol_id = idol.id
		self.event_id = event.id
		self.testimonial = testimonial
		if date is None:
			self.date = datetime.utcnow()
		else:
			self.date = date
		self.live = live

	def __repr__(self):
		return "<Testimonial ID %r>" % self.id

# Creating Idols DB Structure

class Idol(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	user_id = db.Column(db.Integer, db.ForeignKey('user.id')) 
	event_id = db.Column(db.Integer, db.ForeignKey('event.id')) 
	live = db.Column(db.Boolean)

	testimonials = db.relationship('Testimonial', backref='idols', lazy='dynamic')

	def __init__(self, user, event, live=True):
		self.user_id = user.id
		self.event_id = event.id
		self.live = live

	def __repr__(self):
		return "<Idol ID %r>" % self.id

