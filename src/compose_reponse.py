__author__ = 'Alex Hart'

import csv
import random
import numpy

# figure out what list to pull a response from
def determine_response_category(options):
    rankings = []
    for i in options:
        rankings.append(i[3])
    print(rankings)
    if any(obj for obj in options if obj[1]=="K"):
        response_category = "kickers"
    elif any(rank == 1 for rank in rankings):
        response_category = "number_one"
    elif all(rank < 20 for rank in rankings):
        response_category = "small_gap_very_high"
    elif all(rank > 150 for rank in rankings):
        response_category = "small_gap_low"
    elif any(numpy.diff(rankings) > 25):
        response_category = "large_gap"
    else:
        response_category = "small_gap"
    return response_category


def compose_tweet(selections,category,user,response_type="rand"):
    responses = csv.DictReader(open("responses/%s.csv"%category))
    data =[row['phrase'] for row in responses]
    rand_response = random.choice(data)
    p
    if "%s" in rand_response:
        if len(selections) == 1:
            selection = selections[0][0]
        elif len(selections) == 2:
            selection = "%s and %s" % (selections[0][0], selections[1][0])
        elif len(selections) == 3:
            selection = "%s, %s, and %s" % (selections[0][0], selections[1][0], selections[2][0])
        elif len(selections) == 4:
            selection = "%s, %s, %s, and %s" % (selections[0][0], selections[1][0], selections[2][0],selections[3][0])
        elif len(selections) == 5:
            selection = "%s, %s, %s, %s and %s" % (selections[0][0], selections[1][0], selections[2][0],selections[3][0],selections[4][0])
        response = (rand_response %(selection))
    else:
        response = rand_response
    response_len = len(response)
    if validate_tweet(user+" "+response) is True:
        return response, response_len
    else:
        print(response)
        print("response is too long. it's %s characters" %response_len)
        return None, response_len


# make sure the tweet is <= 140 chars
def validate_tweet(response):
    # using 120 so we have room for the twitter handle
    if len(response) <= 140:
        return True
    else:
        return False