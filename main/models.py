from family_web import db

class Location(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	location = db.Column(db.String(80))
	address = db.Column(db.String(255))

	def __init__(self, location, address):
		self.location = location
		self.address = address

	def __repr__(self):
		return self.location

class Event(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	location = db.Column(db.String(80))
	the_round = db.Column(db.Integer)
	date = db.Column(db.String(80))
	theme = db.Column(db.String(80))
	starters = db.Column(db.String(80))
	drinks = db.Column(db.String(80))
	dessert = db.Column(db.String(80))
	disposables = db.Column(db.String(80))
	idol = db.Column(db.String(80))
	add_info = db.Column(db.Text)
	media_link = db.Column(db.String(255))
	live = db.Column(db.Boolean)

	idols = db.relationship('Idol', backref='events', lazy='dynamic') # when backreferencing in templates etc use events
	testimonials = db.relationship('Testimonial', backref='events', lazy='dynamic')

	def __init__(self, location, the_round, date, theme, starters, drinks, dessert, disposables, idol, add_info="None", media_link="#", live=True):
		self.location = location
		self.the_round = the_round
		self.date = date
		self.theme = theme
		self.starters = starters
		self.drinks = drinks
		self.dessert = dessert
		self.disposables = disposables
		self.idol = idol
		self.add_info = add_info
		self.media_link = media_link
		self.live = live

	def __repr__(self):
		return "<Event %r>" % self.id

