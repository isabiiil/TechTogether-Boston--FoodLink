import mongoengine as mg
from os import environ

mg.connect("pantry", host=environ["atlasurl"])


class User(mg.Document):
	username = mg.StringField()
	password = mg.StringField()
	salt = mg.StringField()
	organization = mg.StringField()
	location = mg.StringField()
	utype = mg.StringField()
	posts = mg.ListField(mg.ReferenceField("Post"))


class Post(mg.Document):
	ptype = mg.StringField()
	timestamp = mg.DateField()
	owner = mg.StringField()
	title = mg.StringField()
	content = mg.StringField()
