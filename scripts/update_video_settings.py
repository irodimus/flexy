import requests
import urllib.parse

from plexapi.server import PlexServer

import settings
from utils import utils


def add_collections(video, collections):
    title = utils.clean_title(video.title)

    for collection in collections:

        print(f'Adding "{title}" to "{collection}"')
        video.addCollection(collection)


def add_tags(video, tags):
    title = utils.clean_title(video.title)

    for tag in tags:

        print(f'Adding "{tag}" tag to "{title}"')
        url = utils.generate_url(params={
            'base_url': f'{settings.PLEX_URL}/library/sections/{video.librarySectionID}/all?',
            'type': utils.get_type_id(type=video.type),
            'id': video.ratingKey,
            'includeExternalMedia': 1,
            'genre%5B0%5D.tag.tag': tag,
            'genre.locked': 1,
            'X-Plex-Token': settings.PLEX_TOKEN
        })
        requests.put(url)


def rename_video(video, collections):
    if collections == 'winners':
        trophy = '🏆'
    elif collections == 'nominees':
        trophy = '🥈'

    title = video.title
    if '🏆' not in title and '🥈' not in title:
        title = f'{trophy} {urllib.parse.quote(video.title)}'

        print(f'Adding "{trophy}" to "{video.title}"')
        url = utils.generate_url(params={
            'base_url': f'{settings.PLEX_URL}/library/sections/{video.librarySectionID}/all?',
            'type': utils.get_type_id(type=video.type),
            'id': video.ratingKey,
            'includeExternalMedia': 1,
            'title.value': title,
            'title.locked': 1,
            'titleSort.locked': 1,
            'X-Plex-Token': settings.PLEX_TOKEN
        })
        requests.put(url)


def execute():
    plex = PlexServer(settings.PLEX_URL, settings.PLEX_TOKEN)

    sections_by_type = utils.get_sections_by_type(plex=plex)

    for section_title in sections_by_type['movies']:
        section_config = utils.open_trakt_json('movies')
        section = plex.library.section(section_title)

        for plex_video in section.all():
            title = utils.clean_title(plex_video.title)
            plex_video_config = section_config.get(title, None)

            if plex_video_config:

                collections = plex_video_config.get('collections', None)
                if collections:
                    add_collections(video=plex_video, collections=collections)

                if settings.ADD_WINNERS_TROPHY:
                    winners = plex_video_config.get('winners', None)
                    if winners:
                        rename_video(video=plex_video, collections='winners')

                        if settings.ADD_OSCAR_TAG:
                            add_tags(video=plex_video, tags=['Oscar Best Picture Winners'])

                if settings.ADD_NOMINEES_MEDAL:
                    nominees = plex_video_config.get('nominees', None)
                    if nominees:
                        rename_video(video=plex_video, collections='nominees')

                tags = plex_video_config.get('tags', None)
                if tags:
                    add_tags(video=plex_video, tags=tags)

    # TODO add Show processing


if __name__ == '__main__':
    execute()
