from flask import *
import json
import importlib
import requests
from os import environ
from .util import dbctrl


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
