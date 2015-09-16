__author__ = 'Alex Hart'

from src import configs, parse_input, compose_reponse, secrets
import requests
import sys


# submit the results to a google form for tracking purposes AKA logging
def submit_results(form_id, user, raw_tweet,
                   tagged_tweet,
                   question,
                   confirmed_players,
                   selections,
                   category,
                   response,
                   response_len,
                   tweet_id):
    url = "https://docs.google.com/forms/d/%s/formResponse" % form_id
    submission = {"entry.2105335826": user,
                  "entry.1575116797": raw_tweet,
                  "entry.845787665": tagged_tweet,
                  "entry.1488885322": question,
                  "entry.2116497517": confirmed_players,
                  "entry.1779266700": selections,
                  "entry.1211763545": category,
                  "entry.468172303": response,
                  "entry.1997131024": response_len,
                  "entry.1793373159": tweet_id,
                  }

    requests.post(url, submission)

def determine_rankings(ppr, t=False):
    # use appropriate rankings based on notes
    if t is True:
        rankings = configs.test_rankings
    elif ppr is True:
        rankings = configs.ppr_rankings
    else:
        rankings = configs.rankings
    return rankings


def respond(tweet_text, user, tweet_id, t=False):
    tweet = tweet_text.lower()
    tokens = parse_input.tokenize_input(tweet_text)
    question = parse_input.identify_question(tweet)
    # TODO use different rankings based on ppr and return yards
    ppr = parse_input.is_ppr(tweet)
    return_yards = parse_input.is_return_yards(tweet)

    rankings = determine_rankings(ppr)

    print("Tweet: \"%s\"" % tweet)

    if question == "who_start":
        picks = parse_input.identify_total_selections(tweet)

        print("PARSED INFO:")
        print("Question type: %s" % question)
        print("Number of players to return: %s" % picks)
        print("Is it ppr? %s" % ppr)
        print("Is it return yards? %s" % return_yards)

        confirmed_players = parse_input.verify_possible_players(tweet_text,
                                                                configs.nicknames,
                                                                rankings)
        print("\nPlayers confirmed: %s" % confirmed_players)
        players_with_info = parse_input.populate_player_info(confirmed_players,
                                                             rankings)
        selections, player_options = parse_input.return_selection(
            players_with_info, picks)
        if selections != []:
            print("\nSelection(s) are: %s" % selections)
            category = compose_reponse.determine_response_category(
                player_options)
            print("Category is: %s" % category)
            response, response_len = compose_reponse.compose_tweet(selections,
                                                                   category,
                                                                   user)
            print("Response is: %s" % response)

            submit_results(form_id=secrets.FORM_ID,
                           user=user,
                           raw_tweet=tweet_text,
                           tagged_tweet=tokens,
                           question=question,
                           confirmed_players=confirmed_players,
                           selections=selections,
                           category=category,
                           response=response,
                           response_len=response_len,
                           tweet_id=tweet_id)
            return response
        else:
            print("Could not identify any players")
            return None
    elif question == "unknown":
        print("question unknown")
