from flask import *
import json
import importlib
import requests
from os import environ, urandom
from .util.dbctrl import *
from .util.decorators import *
import hashlib

app = Flask(__name__)
app.secret_key = "HELLO"


def hashcalc(password, salt):
	return hashlib.sha512(
            (password + salt).encode("utf-8")).digest().hex()


@app.route("/", methods=["GET"])
@login_required
def home():
	if "user" in session:
		m = User.objects(username=session["user"])
		return render_template("home.html", user = m[0].username)
	return redirect(url_for("login"))

@app.route("/logout", methods=["get"])
def logout():
	if "user" in session:
		session.pop("user")
	return redirect(url_for("login"))
	pass

@app.route("/login", methods=["POST", "GET"])
def login():
	if request.method == "POST":
		m = User.objects(username=request.form["username"])
		if m and m[0].password == hashcalc(request.form["password"], m[0].salt):
			session["user"] = m[0].username
			return redirect(url_for("home"))
		else:
			flash("wrong credentials")
			pass
	m = request.get_json()
	return render_template("login.html")


@app.route("/register", methods=["GET", "POST"])
def register():
	if "user" in session:
		return redirect(url_for("home"))
	else:
		if request.method == "POST":
			if request.form["password0"] == request.form["password1"]:
				uname = request.form["username"]
				if User.objects(username=uname):
					flash("username already exists")
					return redirect(url_for("register"))
				
				else:
					salt = urandom(64).hex()
					User(username=uname, salt=salt, password=hashcalc(request.form["password0"], salt)).save()
					session["user"] = uname
					return redirect(url_for("home"))
					pass
				pass
			else:
				flash("passwords dont match")
				return redirect(url_for("home"))
			pass
		return render_template("register.html")
	pass

@app.route("/debug", methods=["GET"])
def debug():
	z = requests.post("http://localhost:5000/login", json={"HELLO":"DIE"})
	User(username="mood").save()
	return json.dumps(z.json())


if __name__ == "__main__":
	app.run(debug=True)
