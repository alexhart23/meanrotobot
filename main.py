__author__ = 'Alex Hart'

from src import configs, get_input, parse_input

tweet_unmod = get_input.get_tweet()
tweet = tweet_unmod.lower()

question = parse_input.identify_question(tweet)
ppr = parse_input.is_ppr(tweet)
return_yards = parse_input.is_return_yards(tweet)

if question == "who_start":
    picks = parse_input.identify_total_selections(tweet)

print("Tweet: \"%s\"" % tweet)
print("Raw data from tweet:")
print("Question type: %s" % question)
print("Number of players to return: %s" % picks)
print("Is it ppr? %s" % ppr)
print("Is it return yards? %s" % return_yards)

confirmed_players = parse_input.verify_possible_players(tweet_unmod,
                                                        configs.nicknames,
                                                        configs.rankings)
print("\nPlayers confirmed: %s" % confirmed_players)

players_with_info = parse_input.populate_player_info(confirmed_players,configs.rankings)

selections = parse_input.return_selection(players_with_info, picks)
print("\nSelection(s) are: %s" % selections)

