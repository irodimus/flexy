import json
import os
import requests
import urllib.parse

from plexapi.server import PlexServer

import settings

plex = PlexServer(settings.PLEX_URL, settings.PLEX_TOKEN)


def generate_url(params):
    url = params['base_url']
    for key, value in params.items():
        if key != 'base_url':
            url += f'{key}={value}&'

    return url[:-1]


def clean_title(title):
    return title.replace('🏆 ', '').replace('🥈 ', '')
