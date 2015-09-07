__author__ = 'Alex Hart'


def get_tweet():
    tweet = """pick : OBJ Charles Johnson, megatron, l murray foster. .5 ppr return yards""" #good
    tweet = """Manning, Manning or bradford""" #did not work
    tweet = """Cody Parkey, Stephen Gostowski or Kai Forbath or Tucker""" #didn't find gostowski - spelled wrong
    tweet = """Cosy Parkey, stephen gostkowski or kai forbath""" # worked
    tweet = """I need lineup help: Calvin Johnson or Eddy Lacy?""" #worked
    tweet = """pick 2: Latavius Murray, Gronkowski, or Shady""" #worked
    tweet = """Who should I start Aaron Rodgers or Tom Brady?""" # worked #32.12 second to finish. 6.09 after. MONEY
    tweet = """Who should I start Aaron Rodgers or Luck?""" # worked
    tweet = """Who should I start Aaron Rodgers or luck?""" #did not work. didn't id luck as a noun

    tweet = """Pick 2: AD, Gronk, CJ2K,Megatron"""  # 8.37 seconds to finish. 5.83 after
    #tweet = """Peyton or Eli?""" # doesn't work. can't match just first names
    return tweet
