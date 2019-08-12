import json
import os
import requests
import urllib.parse

from plexapi.server import PlexServer

import settings
from utils import utils

# TODO ignore unrelease movies


def write_json(data):
    file_path = os.path.join(settings.ROOT, 'data', 'missing.json')
    with open(file_path, 'w') as outfile:
        print(f'Writing to file: {file_path}')
        json.dump(data, outfile)


def execute():
    """
    Compare Trakt list with Plex collections to find missing videos.
    """
    missing = {}

    plex = PlexServer(settings.PLEX_URL, settings.PLEX_TOKEN)

    sections_by_type = utils.get_sections_by_type(plex=plex)

    for section_title in sections_by_type['movies']:
        section_config = utils.open_trakt_json('movies')
        section = plex.library.section(section_title)

        trakt_videos = section_config.keys()

        for trakt_video in trakt_videos:
            all_collections = section_config[trakt_video].get('collections', None)
            if all_collections:
                collections = [collection for collection in all_collections if collection not in settings.IGNORE_MISSING_VIDEOS]

                if collections:
                    if not any(x for x in section.all() if x.title == trakt_video):
                        for collection in collections:
                            print(f'Missing "{trakt_video}" for collection "{collection}"')
                            try:
                                missing[collection].append(trakt_video)
                            except KeyError:
                                missing[collection] = [trakt_video]

    write_json(data=missing)


if __name__ == '__main__':
    execute()
