__author__ = 'Alex Hart'

from src import get_input, secrets

stream =get_input.MyStreamer(secrets.APP_KEY,
                    secrets.APP_SECRET,
                    secrets.OAUTH_TOKEN,
                    secrets.OAUTH_TOKEN_SECRET)
stream.user()