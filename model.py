from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Search(db.Model):
    """A set of searches between a given pair of words, either BF or DF

       The assumption here is that only word pairs which are connected by
       a path get recorded.
    """

    __tablename__ = "searches"

    search_id = db.Column(db.Integer, primary_key=True)
    search_type = db.Column(db.String(3), nullable=False) #"DFS" or "BFS"
    start_word = db.Column(db.String(32), nullable=False)
    end_word = db.Column(db.String(32), nullable=False)
    num_letters = db.Column(db.Integer, nullable=False)
    avg_path_length = db.Column(db.Float, nullable=False)
    avg_search_time = db.Column(db.Float, nullable=False) #in ms


    def __repr__(self):
        """Provide helpful representation when printed"""

        repr_str = "<Search start={s_word} end={e_word} type={s_type}>"
        return repr_str.format(s_word=self.start_word,
                               e_word=self.end_word,
                               s_type=self.search_type)




##############################################################################
# Helper functions

def connect_to_db(app):
    """Connect the database to our Flask app."""

    # Configure to use our SQLite database
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///wordladder'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.app = app
    db.init_app(app)


if __name__ == "__main__":
    # As a convenience, if we run this module interactively, it will leave
    # you in a state of being able to work with the database directly.

    from server import app
    connect_to_db(app)
    print "Connected to DB."
