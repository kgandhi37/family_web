import os

SECRET_KEY = '\xd8\x94QH\xbej\xca9\x9a\xec\xab+\xec\xf6_\x86\xb6\x93\x9c_\xe1\x89z\xac'
DEBUG = True 
DB_USERNAME = 'root'
DB_PASSWORD = 'test'
BLOG_DATABASE_NAME = 'family_web'
DB_HOST = 'mysql:3306'
DB_URI = "mysql+pymysql://%s:%s@%s/%s" % (DB_USERNAME, DB_PASSWORD, DB_HOST, BLOG_DATABASE_NAME)
SQLALCHEMY_DATABASE_URI = DB_URI
SQLALCHEMY_TRACK_MODIFICATIONS = True