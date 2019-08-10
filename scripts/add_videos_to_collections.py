import json
import os
import requests
import urllib.parse

from plexapi.server import PlexServer

import settings
from utils import utils

plex = PlexServer(settings.PLEX_URL, settings.PLEX_TOKEN)


def open_json(group):
    file_path = os.path.join(settings.ROOT, 'data', f'{group}.json')
    with open(file_path, 'r') as f:
        config = json.load(f)
    return config


def get_sections_by_type():
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


def add_collections(video, collections):
    for collection in collections:

        print(f'Adding "{video.title}" to "{collection}"')
        video.addCollection(collection)


def add_tags(video, tags):
    for tag in tags:

        print(f'Adding "{tag}" tag to "{video.title}"')
        url = utils.generate_url(params={
            'base_url': f'{settings.PLEX_URL}/library/sections/{video.librarySectionID}/all?',
            'type': 1,
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

    title = f'{trophy} {urllib.parse.quote(video.title)}'

    print(f'Adding "{trophy}" to "{video.title}"')
    url = utils.generate_url(params={
        'base_url': f'{settings.PLEX_URL}/library/sections/{video.librarySectionID}/all?',
        'type': 1,
        'id': video.ratingKey,
        'includeExternalMedia': 1,
        'title.value': title,
        'title.locked': 1,
        'titleSort.locked': 1,
        'X-Plex-Token': settings.PLEX_TOKEN
    })
    requests.put(url)


if __name__ == '__main__':
    sections_by_type = get_sections_by_type()

    for section_title in sections_by_type['movies']:
        section_config = open_json('movies')
        section = plex.library.section(section_title)

        for plex_video in section.all():
            plex_video_config = section_config.get(plex_video.title, None)

            if plex_video_config:

                collections = plex_video_config.get('collections', None)
                if collections:
                    add_collections(video=plex_video, collections=collections)

                winners = plex_video_config.get('winners', None)
                if winners:
                    rename_video(video=plex_video, collections='winners')
                    add_tags(video=plex_video, tags=['Oscar Best Picture Winners'])

                nominees = plex_video_config.get('nominees', None)
                if nominees:
                    rename_video(video=plex_video, collections='nominees')

                tags = plex_video_config.get('tags', None)
                if tags:
                    add_tags(video=plex_video, tags=tags)


