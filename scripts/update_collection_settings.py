import requests
import urllib.parse
import xml.etree.ElementTree as ET
import datetime

import dropbox
from plexapi.server import PlexServer

import settings
from utils import utils

# TODO upload background
# TODO update description


def upload_poster(collection):
    dbx = dropbox.Dropbox(settings.DROPBOX_TOKEN)
    contents = dbx.files_list_folder(path='/Collections').entries

    poster_file = [file for file in contents if collection.title.lower() in file.name.lower()]

    image_file_path = None
    if poster_file and len(poster_file) == 1:
        image_file_path = poster_file[0].path_display

    elif len(poster_file) > 0:
        server_modified_date = datetime.datetime(1900, 1, 1)

        for file in poster_file:
            try:
                if file.server_modified > server_modified_date:
                    image_file_path = file.path_display
                    server_modified_date = file.server_modified

            except AttributeError:
                # this is probably a folder in the Dropbox folder
                pass

    if image_file_path:
        collection_id = collection.ratingKey
        print(f'Uploading image for "{collection.title}"')

        image_link = dbx.files_get_temporary_link(path=image_file_path).link

        upload_poster_url = utils.generate_url(params={
            'base_url': f'{settings.PLEX_URL}/library/metadata/{collection_id}/posters?',
            'url': urllib.parse.quote(image_link),
            'X-Plex-Token': settings.PLEX_TOKEN
        })
        requests.post(upload_poster_url)

        get_poster_url = utils.generate_url(params={
            'base_url': f'{settings.PLEX_URL}/library/metadata/{collection_id}/posters?',
            'X-Plex-Token': settings.PLEX_TOKEN
        })

        r = requests.get(get_poster_url)
        root = ET.fromstring(r.text)

        for child in root:
            rating_key = child.attrib['ratingKey']
            if rating_key.startswith('upload'):
                upload_url = rating_key

        update_poster = utils.generate_url(params={
            'base_url': f'{settings.PLEX_URL}/library/metadata/{collection_id}/poster?',
            'url': upload_url,
            'X-Plex-Token': settings.PLEX_TOKEN
        })
        requests.put(update_poster)


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

    # hide collection
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

    if (count <= settings.SORT_VIDEOS_BY_RELEASE_MAX_COLLECTION_LENGTH) \
            or (settings.SORT_VIDEOS_DEFAULT.lower() == 'release date') \
            or (collection.title in settings.ALWAYS_SORT_BY_RELEASE_DATE):
        print(f'Changing collection order for "{collection.title}" to "{modes[0]}"')
        update_settings = utils.generate_url(params={
            'base_url': f'{settings.PLEX_URL}/library/metadata/{rating_key}/prefs?',
            'collectionSort': 0,
            'X-Plex-Token': settings.PLEX_TOKEN
        })
        requests.put(update_settings)

    if (count > settings.SORT_VIDEOS_BY_RELEASE_MAX_COLLECTION_LENGTH) \
            or (collection.title in settings.ALWAYS_SORT_ALPHABETICALLY):
        print(f'Changing collection order for "{collection.title}" to "{modes[1]}"')
        update_settings = utils.generate_url(params={
            'base_url': f'{settings.PLEX_URL}/library/metadata/{rating_key}/prefs?',
            'collectionSort': 1,
            'X-Plex-Token': settings.PLEX_TOKEN
        })
        requests.put(update_settings)


if __name__ == '__main__':
    plex = PlexServer(settings.PLEX_URL, settings.PLEX_TOKEN)

    plex_sections = plex.library.sections()

    for plex_section in plex_sections:

        for collection in plex_section.collection():
            upload_poster(collection=collection)
            update_collection_mode(collection=collection)
            update_collection_order(collection=collection)
