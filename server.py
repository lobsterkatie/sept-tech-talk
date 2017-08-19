"""I control everything."""

from jinja2 import StrictUndefined
from flask import Flask, render_template, request, jsonify
from datetime import datetime, timedelta
from model import (db, connect_to_db)
from game import *
from utilities import *

app = Flask(__name__)

# app.secret_key = "shhhhhhhhhhh!!! don't tell!" FIXME

#keep jinja from failing silently because of undefined variables
app.jinja_env.undefined = StrictUndefined

# app.jinja_env.auto_reload = True FIXME










if __name__ == "__main__":
    """If we run this file from the command line, do this stuff"""

    app.debug = True

    connect_to_db(app)

    app.run()
