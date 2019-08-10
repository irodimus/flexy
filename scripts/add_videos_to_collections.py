import json
import os

from plexapi.server import PlexServer

import settings

plex = PlexServer(settings.PLEX_URL, settings.PLEX_TOKEN)


def get_sections_by_type():
    sections_by_type = {
        'movies': [],
        'shows': []
    }
    sections = plex.library.sections()
    for section in sections:
        if section.type == 'movie':
            sections_by_type['movies'].append(section.title)
        elif section.type == 'show':
            sections_by_type['shows'].append(section.title)
    return sections_by_type


def open_json(group):
    file_path = os.path.join(settings.ROOT, 'data', f'{group}.json')
    with open(file_path, 'r') as f:
        config = json.load(f)
    return config



sections_by_type = get_sections_by_type()

for section_title in sections_by_type['movies']:
    section_config = open_json('movies')
    section = plex.library.section(section_title)

    for plex_video in section.all():
        plex_video_config = section_config.get(plex_video.title, None)

        if plex_video_config:

            if plex_video_config.get('collections', None):
                print(f'{plex_video.title} has collections.')
                # TODO add movie to collection

            if plex_video_config.get('winners', None):
                print(f'{plex_video.title} is a winner.')
                # TODO add winner trophy to title

            if plex_video_config.get('nominees', None):
                print(f'{plex_video.title} is a nominee.')
                # TODO add nominee medal to title

            if plex_video_config.get('tags', None):
                print(f'{plex_video.title} has tags.')
                # TODO add tags to video


