from flask import *
import json
import importlib
import requests
importlib.import_module("db")

app = Flask(__name__)

@app.route("/login", methods=["POST"])
def login():
	m = request.get_json()
	out = {}
	return json.dumps(out)

@app.route("/debug", methods=["GET"])
def debug():
	requests.post("http://localhost:5000/login", json={"hello":"bye"})
	return "h"



if __name__ == "__main__":
	app.run(debug=True)
