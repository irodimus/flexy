from datetime import date
import os

today = date.today().strftime('%Y-%m-%d')
root = os.path.dirname(os.path.realpath(__file__))


# Newsletter ###########################################################################################################
NEWSLETTER_DIR = os.path.join(root, 'newsletter')
NEWSLETTER_CONFIG_FILE = f'{today}_newsletter.yaml'

# Plex #################################################################################################################
MOVIES_DIR = os.path.join(root, 'data')