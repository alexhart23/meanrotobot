__author__ = 'Alex Hart'

import nltk
import name_tools
import csv


# TO DO: make sure the input is all lower case
def tokenize_input(input):
    tokens = nltk.word_tokenize(input)
    tagged = nltk.pos_tag(tokens)
    return tagged


# figure out what is being asked
def identify_question(input):
    # is this a "who do I start?" question?
    keywords = ['start', 'choose', 'pick', 'or']
    if any(key in input for key in keywords):
        return "who_start"
    else:
        return "unknown"


def identify_total_selections(input):
    if (" 2" or "two") in input:
        return 2
    elif (" 3" or "three") in input:
        return 3
    elif (" 4" or "four") in input:
        return 4
    elif (" 5" or "five") in input:
        return 5
    else:
        return 1


# identify the players that are involved in the question
def identify_possible_players(input):
    players = []
    tokens = tokenize_input(input)
    #players = [i[0] for i in tokens if i[1] == "NN" or i[1] == "NNP"]
    players = [i[0] for i in tokens]
    to_ignore = ['ppr','or','start','choose','pick','@','MeanRotobot']
    players = [el for el in players if el.lower() not in to_ignore]
    return players


def check_player_by_nickname(player, nicknames):
    #print("Seeing if \"%s\" is a known nickname..." % player)
    nicknames = csv.DictReader(open(nicknames))
    for row in nicknames:
        stored_nickname = row['nickname']
        match_score = name_tools.match(player, stored_nickname)
        if match_score >= 0.95:
            identified_player = row['playername']
            #print("Found a match: " + player + "=" + stored_nickname,identified_player, match_score)
            return identified_player
    else:
        #("Didn't find %s in nicknames list" % player)
        return None


def check_player_against_rankings(player, rankings):
    rankings = csv.DictReader(open(rankings))
    matches = []
    #print("checking for \"%s\" in rankings with initial search" % player)
    for row in rankings:
        split_name = player.lower().split(" ")
        stored_name = row['playername']
        # using this for the refinement search so we get better results
        stored_name_lower = row['playername'].lower()
        # remove any single character tuples as it will unnecessarily cause
        # it to search any row with that character in the name
        split_name = [el for el in split_name if len(el) > 1]
        if any(s in stored_name_lower for s in split_name):
            match_score = name_tools.match(player, stored_name)
            # if we get a perfect match, automatically return that
            if match_score == 1.0:
                return (stored_name)
            else:
                #print(match_score, stored_name)
                matches.append((match_score, stored_name))
    if matches == []:
        #print("could not find a match for \"%s\"" % player)
        return None
    elif len(matches) == 1:
        return matches[0]
    else:
        sorted_matches = sorted(matches, key=lambda tup: tup[0], reverse=True)
        best_match = sorted_matches[0]
        #print("best match for %s is %s" % (player, best_match))
        return best_match[1]

def populate_player_info(players,rankings):
    players_with_info = []
    for player in players:
        player_info = get_player_info(player,rankings)
        players_with_info.append(player_info)
    return players_with_info

def get_player_info(player, rankings):
    rankings = csv.DictReader(open(rankings))
    for row in rankings:
        stored_name = row['playername']
        if player in stored_name:
            pos = str(row['playerposition'])
            team = str(row['playerteam'])
            ovr_rank = int(row['overallRank'])
            pos_rank = int(row['positionRank'])
            return (player,pos,team,ovr_rank,pos_rank)


def verify_possible_players(input, nicknames, rankings):
    possible_players = identify_possible_players(input)
    print("Possible players: %s" % possible_players)
    confirmed_players = []
    # first, check and see if any of the possible players are a known nickname
    temp_possible_players = identify_possible_players(input)
    for player in temp_possible_players:
        nickname = check_player_by_nickname(player, nicknames)
        if nickname is not None:
            confirmed_players.append(nickname)
            possible_players.remove(player)

    #print("Possible players after nickname check: %s" % possible_players)
    #print("Confirmed players after nickname check: %s" % confirmed_players)

    # combine adjacent items in list to see if those names match anything
    possible_players = [x + " " + y for x, y in
                        zip(possible_players, possible_players[1:])]
    #print("new list is: %s" % possible_players)
    for player in possible_players:
        # check against rankings list
        against_list = check_player_against_rankings(player,
                                                     rankings)
        if against_list is not None:
            confirmed_players.append(against_list)
            possible_players.remove(player)

    #print("Possible players after check against list: %s" % possible_players)
    #print("Confirmed players after check against list: %s" % confirmed_players)

    # remove elements that were matched in the rolling window phase
    possible_players = [item for word in possible_players for item in
                        word.split(' ')]
    # remove single characters. we're not doing a single element search
    # on a single character
    possible_players = [el for el in possible_players if len(el) > 1]
    temp_possible_players = [item for word in possible_players for item in
                             word.split(' ')]
    #print(temp_possible_players)
    for p in temp_possible_players:
        for c in confirmed_players:
            if p.lower() in c.lower():
                #print("Removing \"%s\"" % p)
                possible_players.remove(p)
                break

    # finally, check the remaining words against the rankings for a match
    #print("Possible players after removing used items is: %s" % possible_players)
    for player in possible_players:
        # check against rankings list
        against_list = check_player_against_rankings(player,rankings)
        if against_list is not None:
            confirmed_players.append(against_list)
            possible_players.remove(player)

    print("Possible players after final check against list: %s"
          % possible_players)
    print("Confirmed players after final check against list: %s"
          % confirmed_players)
    return confirmed_players


def return_selection(players, to_select):
    # 'players' format:
    # (match score, name, position, team, overall rank, position rank)
    # TODO - if all the players are of the same position, use pos rank
    found_players = sorted(players, key=lambda tup: tup[4])
    selected_players = found_players[:int(to_select)]
    return selected_players, found_players


# identify scoring notes like ppr, return yards, etc
def is_ppr(input):
    if "ppr" in input:
        return True


def is_return_yards(input):
    if ("return" or "kr") in input:
        return True
