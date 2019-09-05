from datetime import date, datetime
import requests

from plexapi.server import PlexServer

import settings
from utils import utils


def update_collection_mode(collection):
    rating_key = collection.ratingKey
    count = int(collection.childCount)

    modes = {
        -1: "Library default",
        1: "Hide items in this collection",
        2: "Show this collection and its items",
        0: "Hide collection"
    }

    # hide items in collection
    if (count <= settings.HIDE_VIDEOS_MAX_COLLECTION_LENGTH) or (collection.title in settings.IGNORE_COLLECTION_LENGTH):
        expected_mode = 1
        print("Changing collection mode for '{title}' to '{mode}'".format(title=collection.title,
                                                                          mode=modes[expected_mode]))
        update_settings = utils.generate_url(params={
            "base_url": "{base_url}/library/metadata/{id}/prefs?".format(base_url=settings.PLEX_URL, id=rating_key),
            "collectionMode": expected_mode,
            "X-Plex-Token": settings.PLEX_TOKEN
        })
        requests.put(update_settings)

    # show items in collection
    if (collection.title in settings.ALWAYS_SHOW_VIDEOS_IN_COLLECTION) \
            or (count > settings.HIDE_VIDEOS_MAX_COLLECTION_LENGTH) and (
            collection.title not in settings.IGNORE_COLLECTION_LENGTH):
        expected_mode = 2
        print("Changing collection mode for '{title}' to '{mode}'".format(title=collection.title,
                                                                          mode=modes[expected_mode]))
        update_settings = utils.generate_url(params={
            "base_url": "{base_url}/library/metadata/{id}/prefs?".format(base_url=settings.PLEX_URL, id=rating_key),
            "collectionMode": expected_mode,
            "X-Plex-Token": settings.PLEX_TOKEN
        })
        requests.put(update_settings)

    # hide collection as a whole
    if collection.title in settings.ALWAYS_HIDE_COLLECTION:
        expected_mode = 0
        print("Changing collection mode for '{title}' to '{mode}'".format(title=collection.title,
                                                                          mode=modes[expected_mode]))
        update_settings = utils.generate_url(params={
            "base_url": "{base_url}/library/metadata/{id}/prefs?".format(base_url=settings.PLEX_URL, id=rating_key),
            "collectionMode": expected_mode,
            "X-Plex-Token": settings.PLEX_TOKEN
        })
        requests.put(update_settings)

    # hide inactive holiday collections
    if collection.title in settings.HOLIDAY_COLLECTIONS:
        date_ranges = settings.HOLIDAY_COLLECTIONS[collection.title]

        expected_mode = 0
        current_date = datetime.now().date()

        start_date = datetime.strptime(str(current_date.year) + '-' + date_ranges[0], '%Y-%m-%d').date()
        end_date = datetime.strptime(str(current_date.year) + '-' + date_ranges[1], '%Y-%m-%d').date()

        if not start_date <= current_date <= end_date:
            print("Changing collection mode for '{title}' to '{mode}'".format(title=collection.title,
                                                                              mode=modes[expected_mode]))
            update_settings = utils.generate_url(params={
                "base_url": "{base_url}/library/metadata/{id}/prefs?".format(base_url=settings.PLEX_URL, id=rating_key),
                "collectionMode": expected_mode,
                "X-Plex-Token": settings.PLEX_TOKEN
            })
            requests.put(update_settings)


def update_collection_order(collection):
    rating_key = collection.ratingKey
    count = int(collection.childCount)

    modes = {
        0: "Release date",
        1: "Alphabetical"
    }

    # by release date
    if (count <= settings.SORT_VIDEOS_BY_RELEASE_MAX_COLLECTION_LENGTH) \
            or (collection.title in settings.ALWAYS_SORT_BY_RELEASE_DATE):
        print("Changing collection order for '{title}' to '{mode}'".format(title=collection.title, mode=modes[0]))
        update_settings = utils.generate_url(params={
            "base_url": f"{settings.PLEX_URL}/library/metadata/{rating_key}/prefs?",
            "collectionSort": 0,
            "X-Plex-Token": settings.PLEX_TOKEN
        })
        requests.put(update_settings)

    # alphabetically
    if (count > settings.SORT_VIDEOS_BY_RELEASE_MAX_COLLECTION_LENGTH) \
            or (collection.title in settings.ALWAYS_SORT_ALPHABETICALLY):
        print("Changing collection order for '{title}' to '{mode}'".format(title=collection.title, mode=modes[1]))
        update_settings = utils.generate_url(params={
            "base_url": f"{settings.PLEX_URL}/library/metadata/{rating_key}/prefs?",
            "collectionSort": 1,
            "X-Plex-Token": settings.PLEX_TOKEN
        })
        requests.put(update_settings)


def execute():
    plex = PlexServer(settings.PLEX_URL, settings.PLEX_TOKEN)

    plex_sections = plex.library.sections()

    for plex_section in plex_sections:

        for collection in plex_section.collection():
            update_collection_mode(collection=collection)
            # update_collection_order(collection=collection)


if __name__ == "__main__":
    execute()
