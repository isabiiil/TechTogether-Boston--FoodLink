import mongoengine as mg
from os import environ

mg.connect("pantry")

class User(mg.Document):
	username = mg.StringField()
	password = mg.StringField()
	organization = mg.StringField()
	location = mg.StringField()
	type = mg.StringField()
	posts = mg.ListField(mg.ReferenceField("Post"))

class Post(mg.Document):
	type = mg.StringField()
	timestramp = mg.DateField()
	content = mg.StringField()
