"""I control everything."""

from jinja2 import StrictUndefined
from flask import Flask, render_template, request, jsonify
from model import db, connect_to_db, Search
from game import *
# from utilities import *

app = Flask(__name__)

#FIXME take this out if there's no session
# app.secret_key = "shhhhhhhhhhh!!! don't tell!"

#keep jinja from failing silently because of undefined variables
app.jinja_env.undefined = StrictUndefined

# FIXME take this out if the bug is fixed
# app.jinja_env.auto_reload = True


@app.route("/")
def show_homepage():
    """Show the landing page"""

    return render_template("home.html")


@app.route("/do-search.json", methods=["POST"])
def do_search():
    """Run BFS and DFS searches, both recording the results in the DB and
       returning them to the front end as JSON."
    """

    #get form values
    start_word = request.form.get("start_word")
    end_word = request.form.get("end_word")

    #check if this pair has been run before - if so, just return the previous
    #results
    prev_results = (Search.query.filter(Search.start_word == start_word,
                                        Search.end_word == end_word)
                                .order_by(Search.search_type)
                                .all())
    if prev_results:
        #because of the order_by, BFS will be before DFS
        return jsonify({"BFS": prev_results[0].to_dict(),
                        "DFS": prev_results[1].to_dict()})

    #otherwise, if this is a new word pair, run searches
    results = do_searches(start_word, end_word, 1000)

    #if a path was found, record data in the DB
    if results:
        dfs_result = Search(**results["DFS"])
        bfs_result = Search(**results["BFS"])
        db.session.add_all([dfs_result, bfs_result])
        db.session.commit()

    #return the results to the front end
    return jsonify(results)






if __name__ == "__main__":
    """If we run this file from the command line, do this stuff"""

    app.debug = True

    connect_to_db(app)

    app.run()
