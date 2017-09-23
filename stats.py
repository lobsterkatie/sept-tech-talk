from model import db, Search
from collections import defaultdict


def average(nums):
    """Return the mean of the given list of values

    >>> average([1, 6, 10, 4, 3])
    4.8

    >>> average([2, 5, 8, 1])
    4.0

    """

    return sum(nums) / float(len(nums))



def median(nums):
    """Return the median value from the given list

    >>> median([3, 5, 1, 4, 2])
    3

    >>> median([3, 2, 4, 1])
    2.5

    """

    sorted_nums = sorted(nums)
    num_count = len(nums)
    if num_count % 2 == 0:
        num1 = sorted_nums[num_count / 2 - 1]
        num2 = sorted_nums[num_count / 2]
        return (num1 + num2) / 2.0
    else:
        return sorted_nums[num_count / 2]


def compute_graph_stats():
    """Compute various stats for graphing purposes.

       Returns a dictionary of the form {
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

    #create a dictionary to hold the stats
    #note that it's set up as a defaultdict of defaultdicts, so as not to have
    #to create the structure ahead of time (the "pretty" is so it can be
    #pretty-printed for debugging purposes)
    stats = PrettyDefaultDict(lambda: PrettyDefaultDict(list))

    #compute the stats and add them to the dictionary
    for search_type in ["BFS", "DFS"]:
        for word_length in range(2, 11):

            #get all the relevant searches out of the database
            searches = (
                Search.query.filter(Search.search_type == search_type,
                                    Search.word_length == word_length)
                            .all())

            #compute and store medians for path length, search time,
            #efficiency, and words explored
            med_path_length = median([search.med_path_length
                                      for search in searches])
            stats["pathLength"][search_type].append(
                int(round(med_path_length)))


            med_search_time = median([search.med_search_time
                                      for search in searches])
            stats["searchTime"][search_type].append(
                round(med_search_time, 1))


            med_efficiency = median([search.med_efficiency
                                     for search in searches])
            stats["efficiency"][search_type].append(
                round(100 * med_efficiency, 1))


            med_words_explored = median([search.med_words_explored
                                         for search in searches])
            stats["wordsExplored"][search_type].append(
                int(round(med_words_explored)))


    #add metadata to the dictionary for graphing purposes
    stats["wordLengths"] = range(2, 11)
    stats["pathLength"]["yAxisLabel"] = "num words in path"
    stats["searchTime"]["yAxisLabel"] = "search time (ms)"
    stats["wordsExplored"]["yAxisLabel"] = "num words explored"
    stats["efficiency"]["yAxisLabel"] = "% of explored words used"

    # pprint(stats)

    return stats


class PrettyDefaultDict(defaultdict):
    """A hack to make defaultdicts pretty-printable"""
    __repr__ = dict.__repr__



if __name__ == "__main__":

    #create a fake flask app, so that we can talk to the database by running
    #this file directly
    from flask import Flask
    from model import connect_to_db
    app = Flask(__name__)
    connect_to_db(app)
    print "Connected to DB."
