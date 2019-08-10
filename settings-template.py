from datetime import date
import os

# Generic ##############################################################################################################
TODAY = date.today().strftime('%Y-%m-%d')
ROOT = os.path.dirname(os.path.realpath(__file__))

# Newsletter ###########################################################################################################
NEWSLETTER_DIR = os.path.join(ROOT, 'newsletter')
NEWSLETTER_CONFIG_FILE = f'{TODAY}_newsletter.yaml'

# Synology #############################################################################################################
MOVIES_DIR = os.path.join(ROOT, 'test_dir')

# Plex #################################################################################################################
REMOVE_SINGLE_VIDEO_COLLECTIONS = True

# Trakt ################################################################################################################
TRAKT_BASE_URL = 'https://api.trakt.tv'
TRAKT_DEFAULT_USER_ID = 'not_implemented'
TRAKT_CLIENT_ID = 'not_implemented'
TRAKT_CLIENT_SECRET = 'not_implemented'
TRAKT_REDIRECT_URI = 'http://localhost:8080/'

TRAKT_TAGS = {
    'COLLECTION': {'group': 'collections'},
    'HOLIDAY': {'group': 'collections'},
    'WINNERS': {'group': 'winners'},
    'NOMINEES': {'group': 'nominees'},
    'TAG': {'group': 'tag'},
    'PEOPLE': {'group': 'people'}
}

COLLECTIONS = ['collections']
PEOPLE = ['people']
TROPHIES = ['oscar_winners', 'oscar_nominees']
TAGS = ['tags']
