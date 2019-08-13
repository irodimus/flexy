from plexapi.server import PlexServer

import settings
from utils import utils


def add_collections_to_shows(video, collections):
    # receive AttributeError: 'Show' object has no attribute 'collections' when using plexapi function
    title = utils.clean_title(video.title)

    for collection in collections:

        print(f'Adding "{title}" to "{collection}"')
        edits = {
            'collection[0].tag.tag': collection,
            'collection.locked': 1
        }
        video.edit(**edits)


def add_trophy_to_video(video, collections):
    if collections == 'winners':
        trophy = '🏆'
    elif collections == 'nominees':
        trophy = '🥈'

    if not video.title.startswith(trophy):
        print(f'Adding "{trophy}" to {video.title}')
        edits = {
            'title.value': f'{trophy} {video.title}',
            'title.locked': 1,
            'titleSort.locked': 1
        }
        video.edit(**edits)


def add_quality(video):
    if not any([x in video.title for x in ['(4K)', '(8K)']]):
        if video.media[0].height == 2160:
            quality = '4K'
        elif video.media[0].height == 4320:
            quality = '8K'
        else:
            return

    if settings.ADD_QUALITY_SUFFIX:
        print(f'Adding "{quality}" suffix to "{video.title}"')

        edits = {
            'title.value': f'{video.title} ({quality})',
            'title.locked': 1,
            'titleSort.locked': 1
        }
        video.edit(**edits)

    if settings.ADD_QUALITY_TAG:
        print(f'Adding "{quality}" tag to "{video.title}"')
        add_tags(video=video, tags=[quality])


def execute():
    plex = PlexServer(settings.PLEX_URL, settings.PLEX_TOKEN)

    sections_by_type = utils.get_sections_by_type(plex=plex)

    # for section_title in sections_by_type['movies']:
    #     section_config = utils.open_trakt_json('movies')
    #     section = plex.library.section(section_title)
    #
    #     for plex_video in section.all():
    #         title = utils.clean_title(plex_video.title)
    #         plex_video_config = section_config.get(title, None)
    #
    #         if plex_video_config:
    #
    #             collections = plex_video_config.get('collections', None)
    #             if collections:
    #                 print(f'Adding "{title}" to {collections}')
    #                 plex_video.addCollection(collections)
    #
    #             if settings.ADD_WINNERS_TROPHY:
    #                 winners = plex_video_config.get('winners', None)
    #                 if winners:
    #                     add_trophy_to_video(video=plex_video, collections='winners')
    #
    #                     if settings.ADD_OSCAR_TAG:
    #                         print(f"Adding ['Oscar Best Picture Winners'] to {plex_video.title}")
    #                         plex_video.addGenre('Oscar Best Picture Winners')
    #
    #             if settings.ADD_NOMINEES_MEDAL:
    #                 nominees = plex_video_config.get('nominees', None)
    #                 if nominees:
    #                     add_trophy_to_video(video=plex_video, collections='nominees')
    #
    #             tags = plex_video_config.get('tags', None)
    #             if tags:
    #                 print(f'Adding {tags} to {plex_video.title}')
    #                 plex_video.addGenre(tags)
    #
    #         if settings.ADD_QUALITY_SUFFIX or settings.ADD_QUALITY_TAG:
    #             add_quality(video=plex_video)

    for section_title in sections_by_type['shows']:
        section_config = utils.open_trakt_json('shows')
        section = plex.library.section(section_title)

        for plex_video in section.all():
            title = utils.clean_title(plex_video.title)
            plex_video_config = section_config.get(title, None)

            if plex_video_config:

                collections = plex_video_config.get('collections', None)
                if collections:
                    add_collections_to_shows(video=plex_video, collections=collections)

                tags = plex_video_config.get('tags', None)
                if tags:
                    print(f'Adding {tags} to {plex_video.title}')
                    plex_video.addGenre(tags)


if __name__ == '__main__':
    execute()
