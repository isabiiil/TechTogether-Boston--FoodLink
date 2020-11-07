from flask import *
import json
import importlib
import requests
import mongoengine as mg
from os import environ

mg.connect("pantry", host=environ["atlasurl"])
class User(mg.Document):
	username = mg.StringField()
	password = mg.StringField()
	organization = mg.StringField()
	location = mg.StringField()
	type = mg.StringField()
	posts = mg.ListField(mg.ReferenceField("Post"))


class Post(mg.Document):
	type = mg.StringField()
	timestamp = mg.DateField()
	content = mg.StringField()



app = Flask(__name__)

@app.route("/")
def home():
	print(environ["atlasurl"])
	return "home"

@app.route("/login", methods=["POST"])
def login():
	m = request.get_json()
	return json.dumps(m)

@app.route("/debug", methods=["GET"])
def debug():
	z = requests.post("http://localhost:5000/login", json={"HELLO":"DIE"})
	User(username="mood").save()
	return json.dumps(z.json())




if __name__ == "__main__":
	app.run(debug=True)
