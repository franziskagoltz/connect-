""" Server file for connect++ """

from jinja2 import StrictUndefined

from flask import Flask, jsonify, render_template, redirect, request, flash, session, g

from flask_debugtoolbar import DebugToolbarExtension

from model import connect_to_db, db


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
def view_connections():
    """lets user add a connection"""

    return render_template("add_connection.html")


if __name__ == "__main__":
    # We have to set debug=True here, since it has to be True at the
    # point that we invoke the DebugToolbarExtension
    app.debug = False

    connect_to_db(app, "postgresql:///")

    # Use the DebugToolbar
    DebugToolbarExtension(app)

    app.run(host="0.0.0.0")
