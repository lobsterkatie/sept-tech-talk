from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from json import dumps

db = SQLAlchemy()

##############################################################################
# ToDict mixin


class ToDictMixin(object):
    """Provides a method to return a dictionary version of a model class."""

    def to_dict(self):
        """Returns a dictionary representing the object"""

        dict_of_obj = {}

        #iterate through the table's columns, adding the value in each
        #to the dictionary
        for column_name in self.__mapper__.column_attrs.keys():
            value = getattr(self, column_name, None)
            dict_of_obj[column_name] = value

        #return the completed dictionary
        return dict_of_obj


##############################################################################
# JSON mixin


class JSONMixin(object):
    """Provides a method to return a JSON version of a model class."""

    def json(self):
        """Return a JSON string representing the object"""

        dict_of_obj = {}

        #iterate through the table's columns, adding the value in each
        #to the dictionary
        for column_name in self.__mapper__.column_attrs.keys():
            value = getattr(self, column_name, None)
            dict_of_obj[column_name] = value

        #jsonify the completed dictionary and return the resulting string
        return dumps(dict_of_obj)


##############################################################################
# Model definitions


class Search(ToDictMixin, db.Model):
    """A set of searches between a given pair of words, either BF or DF

       The assumption here is that only word pairs which are connected by
       a path get recorded.
    """

    __tablename__ = "searches"

    search_id = db.Column(db.Integer, primary_key=True)
    search_type = db.Column(db.String(3), nullable=False) #"DFS" or "BFS"
    start_word = db.Column(db.String(32), nullable=False)
    end_word = db.Column(db.String(32), nullable=False)
    word_length = db.Column(db.Integer, nullable=False)
    num_trials = db.Column(db.Integer, nullable=False)
    avg_path_length = db.Column(db.Float, nullable=False)
    avg_search_time = db.Column(db.Float, nullable=False) #in ms
    avg_efficiency = db.Column(db.Float, nullable=False)
    med_path_length = db.Column(db.Float, nullable=False)
    med_search_time = db.Column(db.Float, nullable=False) #in ms
    med_efficiency = db.Column(db.Float, nullable=False)
    sample_path = db.Column(db.ARRAY(db.String(16)), nullable=False)

    def __repr__(self):
        """Provide helpful representation when printed"""

        repr_str = "<Search start={s_word} end={e_word} type={s_type}>"
        return repr_str.format(s_word=self.start_word,
                               e_word=self.end_word,
                               s_type=self.search_type)


class Word(db.Model):
    """A legal word, along with its degree"""

    __tablename__ = "words"

    word_id = db.Column(db.Integer, primary_key=True)
    word = db.Column(db.String(32), nullable=False)
    degree = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        """Provide helpful representation when printed"""

        repr_str = "<Word {word}>"
        return repr_str.format(word=self.word)


##############################################################################
# Helper functions

def connect_to_db(app):
    """Connect the database to our Flask app."""

    # Configure to use our SQLite database
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///doublets'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.app = app
    db.init_app(app)


if __name__ == "__main__":

    #create a fake flask app, so that we can talk to the database by running
    #this file directly
    app = Flask(__name__)
    connect_to_db(app)
    print "Connected to DB."
