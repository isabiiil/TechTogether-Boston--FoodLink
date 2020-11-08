from flask import *
import json
import importlib
import requests
from os import environ, urandom
from .util.dbctrl import *
from .util.decorators import *
import datetime
import hashlib

app = Flask(__name__)
app.secret_key = "HELLO"


def hashcalc(password, salt):
	return hashlib.sha512(
            (password + salt).encode("utf-8")).digest().hex()

@app.route("/", methods=["GET"])
@login_required
def home():
	print(session)
	if "user" in session:
		m = User.objects(username=session["user"])
		pdata = Post.objects()
		return render_template("home.html", user=m[0], pdata=pdata, posts=Post.objects())
	return redirect(url_for("login"))

@app.route("/logout", methods=["get"])
def logout():
	if "user" in session:
		session.pop("user")
		session.pop("type")
	flash("logged out")
	return redirect(url_for("login"))
	pass

@app.route("/login", methods=["POST", "GET"])
def login():
	if request.method == "POST":
		m = User.objects(username=request.form["username"])
		if m and m[0].password == hashcalc(request.form["password"], m[0].salt):
			session["user"] = m[0].username
			session["type"] = m[0].utype
			return redirect(url_for("home"))
		else:
			flash("wrong credentials")
			pass
	m = request.get_json()
	if "user" in session:
		return redirect(url_for("home"))
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
					User(username=uname, salt=salt, password=hashcalc(request.form["password0"], salt), utype = request.form["type"]).save()
					session["user"] = uname
					session["type"] = request.form["type"]
					return redirect(url_for("home"))
					pass
				pass
			else:
				flash("passwords dont match")
				return redirect(url_for("home"))
			pass
		return render_template("register.html")
	pass

@app.route("/post", methods=["GET", "POST"])
def newpost():
	if request.method == "POST":
		print(request.form)
		time = datetime.datetime.now().strftime("%m/%d/%Y, %H:%M:%S")
		if session["type"] == "orgo":
			message = request.form["message"]
			type = request.form["post-type"]
			announcement = request.form["announcement"]
			acknowledge = request.form["acknowledge"]
			category = request.form["category"]

			if type == "Announcement":
				post = Post(ptype="orgo", title="Announcement", content=message, timestamp = time, owner=session["user"]).save()
				u = User.objects(username=session["user"])[0]
				u.posts.append(post)
				u.save()
			else:
				post = Post(ptype="orgo", title=announcement+" " + acknowledge, content = message, timestamp = time, owner=session["user"]).save()
				User.objects(username=session["user"])[0]
				u = User.objects(username=session["user"])[0]
				print(u.posts)
				u.posts.append(post)
				u.save()
			return redirect(url_for("home"))
		
		else:
			message = request.form["message"]
			type = request.form["post-type"]
			subject = request.form["appreciation"]
			title = "Appreciation: " + subject
			post = Post(ptype="user", content = message, title = title, timestamp = time, owner=session["user"]).save()
			return redirect(url_for("home"))
	udata = User.objects()
	user = [x for x in udata if x.username==session["user"]]
	return render_template("post.html", udata = udata, user=user[0], posts=Post.objects(owner=session["user"]))

@app.route("/debug", methods=["GET"])
def debug():
	z = requests.post("http://localhost:5000/login", json={"HELLO":"DIE"})
	User(username="mood").save()
	return json.dumps(z.json())


if __name__ == "__main__":
	app.run(debug=True)
