import requests

from plexapi.server import PlexServer

import settings
from utils import utils

"""
Remove all trophies and medals from all movies.
"""

plex = PlexServer(settings.PLEX_URL, settings.PLEX_TOKEN)

plex_sections = plex.library.sections()

for plex_section in plex_sections:

    if plex_section.type == 'movie':
        section = plex.library.section(plex_section.title)

        for video in section.all():
            title = video.title

            trophies = ['🏆', '🥈']
            if any(trophy in title for trophy in trophies):

                print(f'Removing trophy from "{title}"')
                url = utils.generate_url(params={
                    'base_url': f'{settings.PLEX_URL}/library/sections/{video.librarySectionID}/all?',
                    'type': 1,
                    'id': video.ratingKey,
                    'includeExternalMedia': 1,
                    'title.value': utils.clean_title(title),
                    'title.locked': 1,
                    'titleSort.locked': 1,
                    'X-Plex-Token': settings.PLEX_TOKEN
                })
                requests.put(url)
