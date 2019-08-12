import requests

from plexapi.server import PlexServer

import settings
from utils import utils

# TODO update description (sourced from Trakt?)


def update_collection_mode(collection):
    rating_key = collection.ratingKey
    count = int(collection.childCount)

    modes = {
        -1: 'Library default',
        1: 'Hide items in this collection',
        2: 'Show this collection and its items',
        0: 'Hide collection'
    }

    # hide items in collection
    if (count <= settings.HIDE_VIDEOS_MAX_COLLECTION_LENGTH) or (collection.title in settings.IGNORE_COLLECTION_LENGTH):
        print(f'Changing collection mode for "{collection.title}" to "{modes[1]}"')
        update_settings = utils.generate_url(params={
            'base_url': f'{settings.PLEX_URL}/library/metadata/{rating_key}/prefs?',
            'collectionMode': 1,
            'X-Plex-Token': settings.PLEX_TOKEN
        })
        requests.put(update_settings)

    # show items in collection
    if (collection.title in settings.ALWAYS_SHOW_VIDEOS_IN_COLLECTION) \
            or (count > settings.HIDE_VIDEOS_MAX_COLLECTION_LENGTH):
        print(f'Changing collection mode for "{collection.title}" to "{modes[2]}"')
        update_settings = utils.generate_url(params={
            'base_url': f'{settings.PLEX_URL}/library/metadata/{rating_key}/prefs?',
            'collectionMode': 2,
            'X-Plex-Token': settings.PLEX_TOKEN
        })
        requests.put(update_settings)

    # hide collection as a whole
    if collection.title in settings.ALWAYS_HIDE_COLLECTION:
        print(f'Changing collection mode for "{collection.title}" to "{modes[0]}"')
        update_settings = utils.generate_url(params={
            'base_url': f'{settings.PLEX_URL}/library/metadata/{rating_key}/prefs?',
            'collectionMode': 0,
            'X-Plex-Token': settings.PLEX_TOKEN
        })
        requests.put(update_settings)


def update_collection_order(collection):
    rating_key = collection.ratingKey
    count = int(collection.childCount)

    modes = {
        0: 'Release date',
        1: 'Alphabetical'
    }

    # by release date
    if (count <= settings.SORT_VIDEOS_BY_RELEASE_MAX_COLLECTION_LENGTH) \
            or (collection.title in settings.ALWAYS_SORT_BY_RELEASE_DATE):
        print(f'Changing collection order for "{collection.title}" to "{modes[0]}"')
        update_settings = utils.generate_url(params={
            'base_url': f'{settings.PLEX_URL}/library/metadata/{rating_key}/prefs?',
            'collectionSort': 0,
            'X-Plex-Token': settings.PLEX_TOKEN
        })
        requests.put(update_settings)

    # alphabetically
    if (count > settings.SORT_VIDEOS_BY_RELEASE_MAX_COLLECTION_LENGTH) \
            or (collection.title in settings.ALWAYS_SORT_ALPHABETICALLY):
        print(f'Changing collection order for "{collection.title}" to "{modes[1]}"')
        update_settings = utils.generate_url(params={
            'base_url': f'{settings.PLEX_URL}/library/metadata/{rating_key}/prefs?',
            'collectionSort': 1,
            'X-Plex-Token': settings.PLEX_TOKEN
        })
        requests.put(update_settings)

# TODO add holiday-specific collections limitations

# TODO add a way to change collection sort order?
# maybe you want genre and holiday-specific collections to show up first


def execute():
    plex = PlexServer(settings.PLEX_URL, settings.PLEX_TOKEN)

    plex_sections = plex.library.sections()

    for plex_section in plex_sections:

        for collection in plex_section.collection():
            upload_poster_via_dropbox(collection=collection)
            update_collection_mode(collection=collection)
            update_collection_order(collection=collection)

    # TODO add Show processing


if __name__ == '__main__':
    execute()
