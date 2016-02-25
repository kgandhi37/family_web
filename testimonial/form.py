from flask_wtf import Form
from flask import session
from wtforms import validators, TextAreaField
from wtforms.ext.sqlalchemy.fields import QuerySelectField
from testimonial.models import Idol
from user.models import User


#  Form to add testimonials

class TestimonialForm(Form):
	testimonial = TextAreaField('Testimonial', [validators.Required()])