from model import db, Search, Word
from collections import defaultdict


class PrettyDefaultDict(defaultdict):
    __repr__ = dict.__repr__


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


def compute_stats():
    """Compute various stats"""

    #group the searches by search type and word length
    search_stats = PrettyDefaultDict(dict)
    stats_for_graphs = PrettyDefaultDict(lambda: PrettyDefaultDict(list))
    for search_type in ["BFS", "DFS"]:
        for word_length in range(2, 11):
            #create a dictionary to hold the stats
            stats = {}

            #get all the relevant searches out of the database
            searches = (
                Search.query.filter(Search.search_type == search_type,
                                    Search.word_length == word_length)
                            .all())

            #compute and store medians for path length, search time,
            #efficiency, and words explored
            med_path_length = median([search.med_path_length
                                      for search in searches])

            med_search_time = median([search.med_search_time
                                      for search in searches])

            med_efficiency = median([search.med_efficiency
                                     for search in searches])

            med_words_explored = median([search.med_words_explored
                                         for search in searches])

            stats["med_path_length"] = int(round(med_path_length))
            stats["med_search_time"] = round(med_search_time, 1)
            stats["med_efficiency"] = round(100 * med_efficiency, 1)
            # stats["med_words_explored1"] = int(100 * med_path_length / med_efficiency)
            stats["med_words_explored"] = int(round(med_words_explored))

            #put the stats into the larger dictionary
            search_stats[search_type][word_length] = stats

            stats_for_graphs["pathLength"][search_type].append(
                 stats["med_path_length"])
            stats_for_graphs["searchTime"][search_type].append(
                 stats["med_search_time"])
            stats_for_graphs["efficiency"][search_type].append(
                 stats["med_efficiency"])
            stats_for_graphs["wordsExplored"][search_type].append(
                 stats["med_words_explored"])

    #add metadata to the dictionary for graphing purposes
    stats_for_graphs["wordLengths"] = range(2, 11)
    stats_for_graphs["pathLength"]["yAxisLabel"] = "num words in path"
    stats_for_graphs["searchTime"]["yAxisLabel"] = "search time (ms)"
    stats_for_graphs["wordsExplored"]["yAxisLabel"] = "num words explored"
    stats_for_graphs["efficiency"]["yAxisLabel"] = "% of explored words used"


    # from pprint import pprint
    # pprint(search_stats)
    # # pprint(search_stats["DFS"])
    # print
    # print
    # # pprint(search_stats["BFS"])
    # pprint(stats_for_graphs)

    return stats_for_graphs

    # stats = defaultdict(lamda: defaultdict())

    # path_length_stats = defaultdict(dict)
    # for search_type in ["BFS", "DFS"]:
    #     for word_length in range(2, 7):
    #         path_length_stats[search_type][word_length]["med_path_length"] = (
    #             median([search.path_length for search in ]))

# def compute_stats2():
#     """Compute stats, grouped by stat and search type. Each collection of stats
#        is a list of 5 values, corresponding to words of lengths 2 through 6."""







if __name__ == "__main__":

    #create a fake flask app, so that we can talk to the database by running
    #this file directly
    from flask import Flask
    from model import connect_to_db
    app = Flask(__name__)
    connect_to_db(app)
    print "Connected to DB."
