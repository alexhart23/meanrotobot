__author__ = 'Alex Hart'

import src.parse_input as parse_input
import src.configs as configs
import os


def test_tokenize_input():
    assert parse_input.tokenize_input(
        "@meanrotobot who should I start? Jeffery or Hopkins") == [('@', 'IN'),
                                                                   (
                                                                       'meanrotobot',
                                                                       'NN'), (
                                                                       'who',
                                                                       'WP'), (
                                                                       'should',
                                                                       'MD'), (
                                                                       'I',
                                                                       'PRP'),
                                                                   ('start',
                                                                    'VB'),
                                                                   ('?', '.'),
                                                                   ('Jeffery',
                                                                    'NNP'), (
                                                                       'or',
                                                                       'CC'),
                                                                   ('Hopkins',
                                                                    'NNP')]


def test_identify_question():
    assert parse_input.identify_question(
        "@meanrotobot who should I start? Jeffery or Hopkins") == "who_start"
    assert parse_input.identify_question(
        "@meanrotobot blah blah blah you suck") == "unknown"


def test_identify_total_selections():
    assert parse_input.identify_total_selections(
        "@meanrotobot pick 2: Lacy, Peterson, Murray") == 2
    assert parse_input.identify_total_selections(
        "@meanrotobot pick two: Lacy, Peterson, Murray") == 2
    assert parse_input.identify_total_selections(
        "@meanrotobot pick 3: Lacy, Peterson, Murray") == 3
    assert parse_input.identify_total_selections(
        "@meanrotobot pick three: Lacy, Peterson, Murray") == 3
    assert parse_input.identify_total_selections(
        "@meanrotobot pick 4: Lacy, Peterson, Murray") == 4
    assert parse_input.identify_total_selections(
        "@meanrotobot pick four: Lacy, Peterson, Murray") == 4
    assert parse_input.identify_total_selections(
        "@meanrotobot pick 5: Lacy, Peterson, Murray") == 5
    assert parse_input.identify_total_selections(
        "@meanrotobot pick five: Lacy, Peterson, Murray") == 5
    assert parse_input.identify_total_selections(
        "@meanrotobot who should I start? Lacy, Peterson, Murray") == 1


def test_identify_possible_players():
    assert parse_input.identify_possible_players(
        "@meanrotobot who should I start? Lacy, Peterson, Murray") == [
               'meanrotobot', 'who', 'should', 'I', '?', 'Lacy', ',',
               'Peterson', ',', 'Murray']


def test_check_player_by_nickname():
    scriptpath = os.path.dirname(__file__)
    nicknames = os.path.join(scriptpath, configs.test_nicknames)
    assert parse_input.check_player_by_nickname("Megatron",
                                                nicknames) == "Calvin Johnson"
    assert parse_input.check_player_by_nickname("FakeName", nicknames) is None


def test_check_player_against_rankings():
    scriptpath = os.path.dirname(__file__)
    rankings = os.path.join(scriptpath, configs.test_rankings)
    assert parse_input.check_player_against_rankings("Calvin Johnson",
                                                     rankings) == "Calvin Johnson"
    assert parse_input.check_player_against_rankings("Johnson",
                                                     rankings) == "Chris Johnson"
    assert parse_input.check_player_against_rankings("Lavatvis Murray",
                                                     rankings) == "Latavius Murray"
    assert parse_input.check_player_against_rankings("Fake Player",
                                                     rankings) is None


def test_is_ppr():
    assert parse_input.is_ppr("@meanrotobot A or b? ppr league") is True
    assert parse_input.is_ppr("@meanrotobot A or b?") is None


def test_is_return_yards():
    assert parse_input.is_return_yards(
        "@meanrotobot A or b? return yard league") is True
    assert parse_input.is_return_yards(
        "@meanrotobot A or b? kr league") is True
    assert parse_input.is_return_yards("@meanrotobot A or b?") is None
