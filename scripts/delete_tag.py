import argparse
import requests

from plexapi.server import PlexServer

import settings
from utils import utils


def execute(genre):
    """
    Remove specific tag from all movies.
    """
    plex = PlexServer(settings.PLEX_URL, settings.PLEX_TOKEN)

    plex_sections = plex.library.sections()

    for plex_section in plex_sections:

        if plex_section.type == "movie":
            section = plex.library.section(plex_section.title)

            for video in section.all():
                video.reload()
                video_genres = [genre.tag.lower() for genre in video.genres]

                if genre.lower() in video_genres:
                    print("Removing {genre} from {title}.".format(genre=genre, title=video.title))
                    url = utils.generate_url(params={
                        "base_url": "{base_url}/library/sections/{id}/all?".format(base_url=settings.PLEX_URL,
                                                                                   id=video.librarySectionID),
                        "type": 1,
                        "id": video.ratingKey,
                        "includeExternalMedia": 1,
                        "genre%5B%5D.tag.tag-": genre,
                        "X-Plex-Token": settings.PLEX_TOKEN
                    })
                    requests.put(url)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Remove genre from Plex video.",
                                     formatter_class=argparse.RawTextHelpFormatter)

    parser.add_argument('--genre', required=True, help='Enter the genre to remove.')
    opts = parser.parse_args()

    execute(opts.genre)
