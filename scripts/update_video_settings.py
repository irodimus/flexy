from plexapi.server import PlexServer

import settings
from utils import utils


def add_collections_to_shows(video, collections):
    # receive AttributeError: 'Show' object has no attribute 'collections' when using plexapi function
    # also isn't going to check to see if the show is already added to a collection to try and avoid extra API calls
    title = utils.clean_title(video.title)

    for collection in collections:
        print("Adding '{title}' to '{collection}'".format(title=title, collection=collection))
        edits = {
            "collection[0].tag.tag": collection,
            "collection.locked": 1
        }
        video.edit(**edits)


def add_trophy_to_video(video, collections):
    if collections == 'winners':
        trophy = '🏆'
    elif collections == 'nominees':
        trophy = '🥈'

    if not video.title.startswith(trophy):
        print("Adding '{trophy}' to '{title}'".format(title=video.title, trophy=trophy))
        edits = {
            "title.value": "{trophy} {title}".format(trophy=trophy, title=video.title),
            "title.locked": 1,
            "titleSort.locked": 1
        }
        video.edit(**edits)


def add_quality(video):
    if not any([x in video.title for x in ["(4K)", "(8K)"]]):
        if video.media[0].height == 2160:
            quality = "4K"
        elif video.media[0].height == 4320:
            quality = "8K"
        else:
            return

    if settings.ADD_QUALITY_SUFFIX:
        print("Adding '{quality}' suffix to '{title}'".format(title=video.title, quality=quality))

        edits = {
            "title.value": "{title} ({quality})".format(title=video.title, quality=quality),
            "title.locked": 1,
            "titleSort.locked": 1
        }
        video.edit(**edits)

    if settings.ADD_QUALITY_TAG:
        print("Adding '{quality}' tag to '{title}'".format(quality=quality, title=video.title))
        video.addGenre("{quality} Videos".format(quality=quality))


def execute():
    plex = PlexServer(settings.PLEX_URL, settings.PLEX_TOKEN)

    sections_by_type = utils.get_sections_by_type(plex=plex)

    for section_title in sections_by_type["movies"]:
        section_config = utils.open_trakt_json("movies")
        section = plex.library.section(section_title)

        for plex_video in section.all():
            title = "{title} ({year})".format(title=utils.clean_title(plex_video.title), year=plex_video.year)
            plex_video_config = section_config.get(title, None)

            if plex_video_config:

                collections = plex_video_config.get("collections", None)
                if collections:
                    current_collections = [collection.tag for collection in plex_video.collections]
                    new_collections = list(set(collections) - set(current_collections))

                    print("Adding '{title}' to collection: {collections}".format(title=title,
                                                                                 collections=", ".join(collections)))
                    plex_video.addCollection(new_collections)

                if settings.ADD_WINNERS_TROPHY:
                    winners = plex_video_config.get("winners", None)
                    if winners:
                        add_trophy_to_video(video=plex_video, collections="winners")

                        if settings.ADD_OSCAR_TAG:
                            print("Adding 'Oscar Best Picture Winners' tag to {title}".format(title=plex_video.title))
                            plex_video.addGenre("Oscar Best Picture Winners")

                if settings.ADD_NOMINEES_MEDAL:
                    nominees = plex_video_config.get("nominees", None)
                    if nominees:
                        add_trophy_to_video(video=plex_video, collections="nominees")

                tags = plex_video_config.get("tags", None)
                if tags:
                    print("Adding {tags} tag to '{title}'".format(tags=", ".join(tags), title=plex_video.title))
                    plex_video.addGenre(tags)

            if settings.ADD_QUALITY_SUFFIX or settings.ADD_QUALITY_TAG:
                add_quality(video=plex_video)

    for section_title in sections_by_type["shows"]:
        section_config = utils.open_trakt_json("shows")
        section = plex.library.section(section_title)

        for plex_video in section.all():
            title = "{title} ({year})".format(title=utils.clean_title(plex_video.title), year=plex_video.year)
            plex_video_config = section_config.get(title, None)

            if plex_video_config:

                collections = plex_video_config.get("collections", None)
                if collections:
                    add_collections_to_shows(video=plex_video, collections=collections)

                tags = plex_video_config.get("tags", None)
                if tags:
                    print("Adding {tags} to '{title}'".format(tags=", ".join(tags), title=plex_video.title))
                    plex_video.addGenre(tags)


if __name__ == '__main__':
    execute()
