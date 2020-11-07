from flask import *
from functools import wraps
import app.util.dbctrl as db


def login_required(route):
       @wraps(route)
       def wrapper(*args, **kwargs):
              if 'user' in session:
                     if len(db.User.objects(username=session["user"])) == 0:
                            session.pop("user")
                            return redirect(url_for("login"))
                     else:
                            return route(*args, **kwargs)
              else:
                     return redirect(url_for('login'))
              
       return wrapper
