import json
import os

import settings


def clean_title(title):
    """
    Removes added icons from titles so they can continue to be matched to Trakt lists.
    """
    icons = ['🏆', '🥈']
    for icon in icons:
        title = title.replace(f'{icon} ', '')
    return title


def generate_url(params):
    """
    Concatenates parameters for Plex API call
    """
    url = params['base_url']
    for key, value in params.items():
        if key != 'base_url':
            url += f'{key}={value}&'

    return url[:-1]


def get_sections_by_type(plex):
    """
    Movies and TV Shows have slightly different attributes so they need to be processed differently.
    """
    sections_by_type = {
        'movies': [],
        'shows': []
    }

    plex_sections = plex.library.sections()

    for plex_section in plex_sections:

        if plex_section.type == 'movie':
            sections_by_type['movies'].append(plex_section.title)

        elif plex_section.type == 'show':
            sections_by_type['shows'].append(plex_section.title)

    return sections_by_type


def get_type_id(type):
    """
    Used for Plex API calls. As far as I know, movies are type 1 and tv shows are type 2.
    """
    return {
        'movie': 1,
        'show': 2,
        'season': 3,
        'episode': 4,
        'collection': 18  # tv shows
    }.get(type, None)


def open_trakt_json(group):
    """
    Read Trakt jsons for updates.
    """
    file_path = os.path.join(settings.ROOT, 'data', f'{group}.json')
    with open(file_path, 'r') as f:
        config = json.load(f)
    return config
