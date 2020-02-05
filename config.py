# ---------------------------------------------------------
# General configurations for the flask app
# ---------------------------------------------------------

import os

# Defining the base directory off the flask app
basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    # Creating a secreat key / access token from enviromental variable
    SLACK_BOT_TOKEN = os.environ.get("SLACK_BOT_TOKEN")

    # Allows for auto update on HTML file changes
    TEMPLATES_AUTO_RELOAD = True

    # NOTE: These configurations can be called by reference:
    #            api.config[<variable>]
    # NOTE: More configuration options here: 
    #            http://flask.pocoo.org/docs/1.0/config/
