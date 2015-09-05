__author__ = 'Alex Hart'

import nltk
from nltk.tree import Tree
import name_tools
import csv


# TO DO: make sure the input is all lower case
def tokenize_input(input):
    tokens = nltk.word_tokenize(input)
    tagged = nltk.pos_tag(tokens)
    entities = nltk.chunk.ne_chunk(tagged, binary=False)
    return entities


# figure out what is being asked
def identify_question(input):
    # is this a "who do I start?" question?
    keywords = ['start', 'choose', 'pick', 'or']
    if any(key in input for key in keywords):
        return "who_start"
    else:
        return None


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
def identify_players(input):
    # TODO: Really, probably should be searching for individual nouns and go from there
    players = []
    tokens = tokenize_input(input)
    for subtree in tokens:
        if type(subtree) == Tree:  # If subtree is a noun chunk, i.e. NE != "O"
            ne_label = subtree.label()
            ne_string = " ".join([token for token, pos in subtree.leaves()])
            players.append((ne_string, ne_label))
    players = [i[0] for i in players]
    return players


def identify_player_nickname(player, nicknames):
    print("Seeing if provided name is a known nickname...")
    nicknames = csv.DictReader(open(nicknames))
    for row in nicknames:
        stored_nickname = row['nickname']
        match_score = name_tools.match(player, stored_nickname)
        if match_score >= 0.95:
            identified_player = row['playername']
            print("Found a match: " + player + "="+ stored_nickname,
                  row['playername'], match_score)
            return identified_player
            break
    else:
        return player


def get_player_info(player, rankings, nicknames):
    rankings = csv.DictReader(open(rankings))

    # first, see if a nickname was used. if so, convert it to a full name
    provided_name = identify_player_nickname(player, nicknames)

    # it takes a bunch of time to run the name_match against EVERY line,
    # so we're only going to check the lines that have at least one
    # of the names from a players full name

    matches = []
    for row in rankings:
        split_name = provided_name.split(" ")
        stored_name = row['playername']
        if any(s in stored_name for s in split_name):
            match_score = name_tools.match(provided_name, stored_name)
            pos = str(row['playerposition'])
            team = str(row['playerteam'])
            ovr_rank = int(row['overallRank'])
            pos_rank = int(row['positionRank'])
            # if we get a perfect match, automatically return that
            if match_score == 1.0:
                return (
                match_score, stored_name, pos, team, ovr_rank, pos_rank)
            elif match_score > 0.60:
                matches.append(
                    (match_score, stored_name, pos, team, ovr_rank, pos_rank))
    sorted_matches = sorted(matches, key=lambda tup: tup[0], reverse=True)
    best_match = sorted_matches[0]
    return best_match


def return_selection(players, selections):
    # 'players' format:
    # (match score, name, position, team, overall rank, position rank)
    # TODO - if all the players are of the same position, use pos rank
    found_players = sorted(players, key=lambda tup: tup[4])
    selected_players = found_players[:int(selections)]
    return selected_players


# identify scoring notes like ppr, return yards, etc
def is_ppr(input):
    if "ppr" in input:
        return True


def is_return_yards(input):
    if ("return" or "kr") in input:
        return True
