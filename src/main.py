__author__ = 'Alex Hart'

from src import configs, parse_input, compose_reponse
import sys

def respond(tweet_text,user,tweet_id):
    tweet = tweet_text.lower()
    question = parse_input.identify_question(tweet)
    # TODO use different rankings based on ppr and return yards
    ppr = parse_input.is_ppr(tweet)
    return_yards = parse_input.is_return_yards(tweet)

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
                                                            configs.rankings)
        print("\nPlayers confirmed: %s" % confirmed_players)
        players_with_info = parse_input.populate_player_info(confirmed_players,configs.rankings)
        selections,player_options = parse_input.return_selection(players_with_info, picks)
        print("\nSelection(s) are: %s" % selections)
        category = compose_reponse.determine_response_category(player_options)
        print("Category is: %s" % category)
        response, response_len = compose_reponse.compose_tweet(selections,category,user)
        print("Response is: %s" % response)
        # TODO submit raw tweet, user, identified question, confirmed players,selected players, and response to a google form for tracking
        return response
    elif question == "unknown":
        print("question unknown")
        sys.exit(1)


