from plexapi.server import PlexServer

import settings


"""
Remove all collection tags from all movies and then delete the collection itself.
You could probably just delete the collection, but I'm not taking any chances.
"""

plex = PlexServer(settings.PLEX_URL, settings.PLEX_TOKEN)

sections = plex.library.sections()

for section in sections:

    if section.type == 'movie':
        all_collections = section.collection()

        if all_collections:
            # remove tags from all movies
            for video in section.all():
                print(f'Removing collection tags from video: {video.title}')
                video.removeCollection([c.tag for c in video.collections])

            # then go through and delete all collections
            for collection in all_collections:
                print(f'Removing collection: {collection.title}')
                collection.delete()
