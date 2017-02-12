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

    return render_template("view_connections.html")


@app.route("/add-connection")
def add_connections():
    """lets user fill out form to add a connection"""

    return render_template("add_connection.html")


@app.route("/added", methods=["POST"])
def add_single_connection():
    """adds a new connection to the database"""

    print "********* start added route"

    # info = request.form

    # print "!!info from server", info

    # helper.add_connection(info)

    # for data in info:
    first_name = request.form.get("first_name")

    print first_name

    last_name = request.form.get("last_name")
    email = request.form.get("email")
    met_where = request.form.get("met_where")
    introduced_by = request.form.get("introduced_by")
    city = request.form.get("city")
    state = request.form.get("state")
    notes = request.form.get("notes")
    interests = request.form.get("interests")
    connection_added_at = datetime.now()

    print "datetime item",  connection_added_at

    print "--------"
    print "hello stop"

    connection = Connection(first_name=first_name, last_name=last_name, email=email,)
                            # met_where=met_where, introduced_by=introduced_by,
                            # city=city, state=state, notes=notes, interests=interests,
                            # connection_added_at=connection_added_at)

    print "connection instance", connection

    db.session.add(connection)

    db.session.commit()

    # flash("You added {} {} as a connection".format(info.get("first_name"), info.get("last_name")))
    flash("You added {} {} as a connection".format(first_name, last_name))

    return redirect("/")


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
        session["user_name"] = current_user.name

        return redirect("/")

    except NoResultFound:
        flash("email and password didn't match any of our records")
        return redirect("/login")



if __name__ == "__main__":
    # We have to set debug=True here, since it has to be True at the
    # point that we invoke the DebugToolbarExtension
    app.debug = False

    connect_to_db(app, "postgresql:///connect")

    # Use the DebugToolbar
    DebugToolbarExtension(app)

    app.run(host="0.0.0.0")
