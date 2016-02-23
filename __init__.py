from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.migrate import Migrate
from flask.ext.markdown import Markdown

app = Flask(__name__)
app.config.from_object('settings')
db = SQLAlchemy(app)

migrate = Migrate(app, db)
Markdown(app)

from user import views
from testimonial import views