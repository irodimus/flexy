from plexapi.server import PlexServer

import settings


def execute():
    plex = PlexServer(settings.PLEX_URL, settings.PLEX_TOKEN)

    plex_sections = plex.library.sections()

    for plex_section in plex_sections:
        for collection in plex_section.collection():
            if collection.childCount <= 1 and collection.title not in settings.IGNORE_SINGLE_VIDEO_COLLECTIONS:
                print(f'Removing collection: {collection.title}')
                collection.delete()


if __name__ == '__main__':
    if settings.REMOVE_SINGLE_VIDEO_COLLECTIONS:
        execute()
