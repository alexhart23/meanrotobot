__author__ = 'Alex Hart'

from twython import TwythonStreamer, Twython, TwythonError
from src import main, secrets


def post_response(reply,tweet_id):
    twitter = Twython(secrets.APP_KEY,
                      secrets.APP_SECRET,
                      secrets.OAUTH_TOKEN,
                      secrets.OAUTH_TOKEN_SECRET)
    try:
        twitter.update_status(status=reply,
                              in_reply_to_status_id=tweet_id)
        print("success")
    except TwythonError as e:
        print("failed: %s" % e)


class MyStreamer(TwythonStreamer):
    def on_success(self, data):
        if ('text' in data) and (data['in_reply_to_status_id'] is None):
            print(data)
            tweet_text = data['text']
            user = '@' + data['user']['screen_name']
            tweet_id = data['id_str']
            response = main.respond(tweet_text, user, tweet_id)
            if response is not None:
                reply = user + " " + response
                post_response(reply,tweet_id)

    def on_error(self, status_code, data):
        print(status_code)

        # Want to stop trying to get data because of the error?
        # Uncomment the next line!
        # self.disconnect()

def sample_tweet():
    tweet = """pick 3: OBJ Charles Johnson, megatron, l murray foster. .5 ppr return yards""" #good
    '''
    tweet = """Manning, Manning or bradford""" #did not work
    tweet = """Cody Parkey, Stephen Gostowski or Kai Forbath or Tucker""" #didn't find gostowski - spelled wrong
    tweet = """Cosy Parkey, stephen gostkowski or kai forbath""" # worked
    tweet = """I need lineup help: Calvin Johnson or Eddy Lacy?""" #worked
    tweet = """pick 2: Latavius Murray, Gronkowski, or Shady""" #worked
    tweet = """Who should I start Aaron Rodgers or Tom Brady?""" # worked #32.12 second to finish. 6.09 after. MONEY
    tweet = """Who should I start Aaron Rodgers or Luck?""" # worked
    tweet = """Who should I start Aaron Rodgers or luck?""" #did not work. didn't id luck as a noun
    tweet = """Pick 2: AD, Gronk, CJ2K,Megatron"""  # 8.37 seconds to finish. 5.83 after
    tweet = """Peyton or Eli?""" # doesn't work. can't match just first names
    tweet = """Tucker or Forbath"""
    tweet = """pick 2 AD, Bell, or Lacy,Megatron,Antonio Brown"""
    tweet = """Golden Tate or Amari Cooper"""
    tweet = """CJ2K or David Johnson"""
    tweet = """Should I start Golden Tate or Tavon Austin?"""'''

    return tweet
