import requests

from plexapi.server import PlexServer

import settings
from utils import utils


def execute():
    """
    Remove all trophies and medals from all movies.
    """
    plex = PlexServer(settings.PLEX_URL, settings.PLEX_TOKEN)

    plex_sections = plex.library.sections()

    for plex_section in plex_sections:

        if plex_section.type == "movie":
            section = plex.library.section(plex_section.title)

            for video in section.all():
                title = video.title

                trophies = ["🏆", "🥈"]
                if any(trophy in title for trophy in trophies):
                    print("Removing trophy from '{title}'".format(title=title))
                    url = utils.generate_url(params={
                        "base_url": "{base_url}/library/sections/{id}/all?".format(base_url=settings.PLEX_URL,
                                                                                   id=video.librarySectionID),
                        "type": 1,
                        "id": video.ratingKey,
                        "includeExternalMedia": 1,
                        "title.value": utils.clean_title(title),
                        "title.locked": 1,
                        "titleSort.locked": 1,
                        "X-Plex-Token": settings.PLEX_TOKEN
                    })
                    requests.put(url)


if __name__ == "__main__":
    execute()
