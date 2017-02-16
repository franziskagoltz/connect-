""" Server file for connect++ """

from jinja2 import StrictUndefined

from flask import Flask, jsonify, render_template, redirect, request, flash, session, g

from flask_debugtoolbar import DebugToolbarExtension
from sqlalchemy.orm.exc import NoResultFound
from model import connect_to_db, db, Connection
from datetime import datetime
import helper


app = Flask(__name__)

# Required to use Flask sessions and the debug toolbar
app.secret_key = "ABCDE"

# Normally, if you use an undefined variable in Jinja2, it fails
# silently. This is horrible. Fix this so that, instead, it raises an
# error.
app.jinja_env.undefined = StrictUndefined
app.jinja_env.auto_reload = True


@app.route("/")
def index():
    """landing page of connect ++"""

    return render_template("index.html")


@app.route("/view-connections")
def view_connections():
    """displays the user's connections"""

    connections = helper.get_connections()

    return render_template("view_connections.html", connections=connections)


# --------------- ADDING NEW CONNECTIONS --------------- #


@app.route("/add-connection")
def add_connections():
    """lets user fill out form to add a connection"""

    return render_template("add_connection.html")


@app.route("/added", methods=["POST"])
def add_single_connection():
    """adds a new connection to the database"""

    info = request.form
    user_id = session["user_id"]

    helper.add_connection(info, user_id)

    flash("You added {} {} as a connection".format(info.get("first_name"), info.get("last_name")))

    return redirect("/")


# --------------- LOGIN / LOGOUT --------------- #


@app.route("/login")
def user_login():
    """renders login form"""

    return render_template("login_form.html")


@app.route("/login", methods=["POST"])
def verify_login():
    """verifies a users login"""

    email = request.form.get("username")
    password = request.form.get("password")

    try:
        current_user = helper.get_current_user(email, password)
        flash("You are now logged in!")
        session["user_id"] = current_user.user_id
        session["user_name"] = current_user.first_name

        return redirect("/")

    except NoResultFound:
        flash("email and password didn't match any of our records")
        return redirect("/login")


@app.route("/logout")
def handle_logout():
    """handles user logout"""

    del session["user_id"]
    del session["user_name"]

    return redirect("/")


# --------------- PROFILE REGISTRATION --------------- #


@app.route("/sign-up")
def sign_up():
    """renders signup form"""

    return render_template("sign_up.html")


@app.route("/signed-up", methods=["POST"])
def processed_sign_up():
    """processes signup form, adds user to db"""

    info = request.form

    helper.add_user(info)

    return redirect("/")


if __name__ == "__main__":
    # We have to set debug=True here, since it has to be True at the
    # point that we invoke the DebugToolbarExtension
    app.debug = False

    connect_to_db(app, "postgresql:///connect")

    # Use the DebugToolbar
    DebugToolbarExtension(app)

    app.run(host="0.0.0.0")
