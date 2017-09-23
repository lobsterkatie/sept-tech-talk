"""I control everything."""

from jinja2 import StrictUndefined
from flask import Flask, render_template, request, jsonify
from flask_migrate import Migrate
from model import db, connect_to_db, Search
from game import *
from stats import compute_graph_stats

app = Flask(__name__)

#FIXME take this out if there's no session
# app.secret_key = "shhhhhhhhhhh!!! don't tell!"

#keep jinja from failing silently because of undefined variables
app.jinja_env.undefined = StrictUndefined

# FIXME take this out if the bug is fixed
app.jinja_env.auto_reload = True

#make the database and migrations work
connect_to_db(app)
migrate = Migrate(app, db)


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
    results = do_searches(start_word, end_word, 1)

    #if a path was found, record data in the DB
    if results:
        dfs_result = Search(**results["DFS"])
        bfs_result = Search(**results["BFS"])
        db.session.add_all([dfs_result, bfs_result])
        db.session.commit()

    #return the results to the front end
    return jsonify(results)


@app.route("/chart-data.json")
def get_chart_data():
    """Calculate stats for charts and return them to the front end.

       Data is a dictionary of the form: {
            "wordLengths": <x-axis labels for chart; range(2, 11)>,
            "pathLength": {
                "yAxisLabel": <string>,
                "BFS": [list of median path lengths, ordered by num_letters],
                "DFS": [list of median path lengths, ordered by num_letters]
            },
            "searchTime": {dict similar to pathLength dict},
            "wordsExplored": {dict similar to pathLength dict},
            "efficiency": {dict similar to pathLength dict}
       }

    """

    #note that for the moment, the actual calculations are being done on
    #server start-up, to dramatically increase pageload performance
    return jsonify(chart_data)


if __name__ == "__main__":
    """If we run this file from the command line, do this stuff"""

    #assuming that the stats for the charts won't change very often or very
    #much, for the moment get the stats on server start-up, to make pageload
    #way faster
    chart_data = compute_graph_stats()

    app.debug = True
    app.run()
