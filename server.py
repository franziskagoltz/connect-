""" Server file for connect++ """

from jinja2 import StrictUndefined

from flask import Flask, jsonify, render_template, redirect, request, flash, session, g

from flask_debugtoolbar import DebugToolbarExtension
from sqlalchemy.orm.exc import NoResultFound
from model import connect_to_db, db, Connection
from datetime import datetime
import helper
import os


app = Flask(__name__)

# Required to use Flask sessions and the debug toolbar
app.secret_key = "ABCDE"

# Normally, if you use an undefined variable in Jinja2, it fails
# silently. This is horrible. Fix this so that, instead, it raises an
# error.
app.jinja_env.undefined = StrictUndefined
app.jinja_env.auto_reload = True

fb_key = os.environ["FB_KEY"]


@app.route("/")
def index():
    """landing page of connect ++"""

    print fb_key

    return render_template("index.html")


@app.route("/view-connections")
def view_connections():
    """displays the user's connections"""

    if "user_id" in session:

        user_id = session["user_id"]

        connections = helper.get_connections(user_id)

        cities = helper.get_cities_of_connections(connections)

        return render_template("view_connections.html", connections=connections, cities=cities)

    else:
        flash("Please log in to view connections")
        return redirect("/login")


# --------------- ADDING NEW CONNECTIONS --------------- #


@app.route("/add-connection")
def add_connections():
    """lets user fill out form to add a connection"""

    if "user_id" in session:

        return render_template("add_connection.html")

    else:
        flash("Please log in to add a new connection")
        return redirect("/")


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

    return render_template("login_form.html", fb_key=fb_key)


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

    session.clear()

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


# --------------- FACEBOOK OAUTH --------------- #


@app.route("/fb-oauth", methods=["POST"])
def facebook_login():
    """handles facebook oauth"""

    info = request.form

    try:
        current_user = helper.get_current_user(info["email"], "passwordfromfb")
        session["user_id"] = current_user.user_id
        session["user_name"] = current_user.first_name
        flash("Welcome back! - You are now logged in!")

        return "success login"

    except NoResultFound:

        helper.add_user(info)
        current_user = helper.get_current_user(info["email"], "passwordfromfb")
        session["user_id"] = current_user.user_id
        session["user_name"] = current_user.first_name
        flash("Thanks for signing up")

        return "success sign up"


# --------------- JSON ROUTES --------------- #


@app.route("/cities.json", methods=["POST"])
def filter_by_cities():
    """received ajax call to get city for connections and return objects matching
       the city selection"""

    city = request.form.get("city")

    city_connection_pairs = helper.get_city_connection_pairs(city, session["user_id"])

    return jsonify(Connection.serialize_connections_object(city_connection_pairs))


if __name__ == "__main__":
    # We have to set debug=True here, since it has to be True at the
    # point that we invoke the DebugToolbarExtension
    app.debug = False

    connect_to_db(app, "postgresql:///connect")

    # Use the DebugToolbar
    DebugToolbarExtension(app)

    app.run(host="0.0.0.0")
