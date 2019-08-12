from plexapi.server import PlexServer
import requests
import xml.etree.ElementTree as ET

import settings
from utils import utils


def get_all_show_collections():
    section_id = utils.get_type_id(type='show')
    url = utils.generate_url(params={
        'base_url': f'{settings.PLEX_URL}/library/sections/{section_id}/all?',
        'type': utils.get_type_id(type='collection'),
        'X-Plex-Token': settings.PLEX_TOKEN
    })
    r = requests.get(url)

    collections = {}
    root = ET.fromstring(r.text)
    for child in root:
        for element in child.getiterator('Directory'):
            collections[element.attrib['ratingKey']] = element.attrib['title']
    return collections


def execute():
    """
    Deletes all collections from movie and tv shows.
    """
    plex = PlexServer(settings.PLEX_URL, settings.PLEX_TOKEN)

    sections = plex.library.sections()

    for section in sections:

        if section.type == 'movie':
            all_movie_collections = section.collection()

            if all_movie_collections:

                for collection in all_movie_collections:
                    print(f'Removing collection: {collection.title}')
                    collection.delete()

        if section.type == 'show':
            all_show_collections = get_all_show_collections()

            for collection_id, collection_title in all_show_collections.items():
                print(f'Removing collection: {collection_title}')
                url = utils.generate_url(params={
                    'base_url': f'{settings.PLEX_URL}/library/metadata/{collection_id}?',
                    'X-Plex-Token': settings.PLEX_TOKEN
                })
                requests.delete(url)


if __name__ == '__main__':
    execute()
