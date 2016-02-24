from flask_wtf import Form
from wtforms import validators, StringField, PasswordField, DateTimeField, IntegerField, TextAreaField
from wtforms.fields.html5 import EmailField
from wtforms.ext.sqlalchemy.fields import QuerySelectField
from main.models import Location
from user.models import User

class LocationForm(Form):
	location = StringField('Location', [validators.Required()])
	address = StringField('Address', [validators.Required()])

def locations():
	return Location.query

def idols():
	return User.query

class EventForm(Form):
	location = QuerySelectField('Location', query_factory=locations, allow_blank=False)
	the_round = IntegerField('Round', [validators.Required()])
	date = StringField('Date', [validators.Required()])
	theme = StringField('Theme', [validators.Required()])
	starters = QuerySelectField('Starters', query_factory=locations, allow_blank=False)
	drinks = QuerySelectField('Drinks', query_factory=locations, allow_blank=False)
	dessert = QuerySelectField('Dessert', query_factory=locations, allow_blank=False)
	disposables = QuerySelectField('Disposables', query_factory=locations, allow_blank=False)
	idol = QuerySelectField('Idol', query_factory=idols, allow_blank=False)
	add_info = TextAreaField('Additional Info')

class EventMediaForm(Form):
	media_link = StringField('Media', [validators.Required()])