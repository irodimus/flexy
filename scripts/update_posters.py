from datetime import datetime, timedelta

import dropbox
from plexapi.server import PlexServer
import re
import requests
import urllib.parse
import xml.etree.ElementTree as ET

import settings
from utils import utils


# TODO upload background

def upload_poster_via_dropbox(media, poster_type):
    """
    The Plex API call needs a link to an image so instead of storing them locally, I store them in Dropbox and use the
    display link generated for each image. To use this, you must have a Dropbox token and have your images
    stored in the correct folders. The image name must match the collection name, however, non-alphanumeric characters
    are ignored for matching purposes.
    """
    dbx = dropbox.Dropbox(settings.DROPBOX_TOKEN)
    contents = dbx.files_list_folder(path=f'/{poster_type.lower()}').entries

    media_id = media.ratingKey
    clean_media_title = utils.clean_title(media.title).replace(':', settings.SEMICOLON_REPLACEMENT).lower()

    poster_file = None
    for file in contents:
        if poster_type != 'collections':
            if f'{clean_media_title} ({media.year})' in file.name.lower():
                print(f'{clean_media_title} ({str(media.year)}) in {file.name.lower()}')
                poster_file = file
        else:
            # collections don't have years
            if clean_media_title in file.name.lower():
                poster_file = file

    image_file_path = None
    if poster_file:
        image_file_path = poster_file.path_display

    if image_file_path:
        print(f'Uploading image for "{media.title}"')
        image_link = dbx.files_get_temporary_link(path=image_file_path).link

        # need to upload the photo to Plex's database
        upload_poster_url = utils.generate_url(params={
            'base_url': f'{settings.PLEX_URL}/library/metadata/{media_id}/posters?',
            'url': urllib.parse.quote(image_link),
            'X-Plex-Token': settings.PLEX_TOKEN
        })
        requests.post(upload_poster_url)

        # once the photo is in the database, we need to get the url
        get_poster_url = utils.generate_url(params={
            'base_url': f'{settings.PLEX_URL}/library/metadata/{media_id}/posters?',
            'X-Plex-Token': settings.PLEX_TOKEN
        })

        r = requests.get(get_poster_url)
        root = ET.fromstring(r.text)

        for child in root:
            rating_key = child.attrib['ratingKey']
            if rating_key.startswith('upload'):
                upload_url = rating_key

        # once we have that url, we can set it as the poster
        update_poster = utils.generate_url(params={
            'base_url': f'{settings.PLEX_URL}/library/metadata/{media_id}/poster?',
            'url': upload_url,
            'X-Plex-Token': settings.PLEX_TOKEN
        })
        requests.put(update_poster)
        return True

    else:
        print(f'No image for "{media.title}"')
        return False


def upload_new_posters(poster_type):
    """
    Loops through Dropbox folders for new files and uploads them if the video or collection exists.
    """
    dbx = dropbox.Dropbox(settings.DROPBOX_TOKEN)
    contents = dbx.files_list_folder(path=f'/{poster_type}').entries

    plex = PlexServer(settings.PLEX_URL, settings.PLEX_TOKEN)

    for file in contents:
        file_modified_at = file.client_modified

        if file_modified_at >= (datetime.now() - timedelta(days=1)):
            regex_split = re.findall(r"^(.*?)(?<=\()(?:\d{4}\|?)+(?=\))", file.name)
            file_title = regex_split[0].replace(' (', '')

            for section in plex.library.sections():
                results = plex.library.section(section.title).search(f'{file_title}')

                # there's a chance this won't return the correct video if there's more than one returned in the search
                if results:
                    video = results[0]
                    poster_exists = upload_poster_via_dropbox(
                        media=video,
                        poster_type=section.title
                    )


def add_posters_for_new_videos(video_type, missing_posters):
    """
    Loops through Plex for newly added videos and uploads posters if they exist.
    """
    plex = PlexServer(settings.PLEX_URL, settings.PLEX_TOKEN)

    sections_by_type = utils.get_sections_by_type(plex=plex)

    for section_title in sections_by_type[video_type]:
        section = plex.library.section(section_title)

        for plex_video in section.all():

    #         title = utils.clean_title(plex_video.title)
    #
    #         added_at = plex_video.addedAt
    #
    #         if added_at >= (datetime.now() - timedelta(days=1)):
    #             poster_exists = upload_poster_via_dropbox(
    #                 media=plex_video,
    #                 poster_type=video_type
    #             )
    #
    #             if not poster_exists:
    #                 missing_posters['posters'].append(title)
    #
    # return missing_posters


# TODO is there a way to check addedAt for collections?
def add_posters_for_collections(missing_posters):
    """
    Loop through all collections and upload correct poster.

    Note: This script does not take into account whether or not a collection is "new", it just updates all of them.
    """
    plex = PlexServer(settings.PLEX_URL, settings.PLEX_TOKEN)

    plex_sections = plex.library.sections()

    for plex_section in plex_sections:

        for collection in plex_section.collection():
            poster_exists = upload_poster_via_dropbox(
                media=collection,
                poster_type='collections'
            )

            if not poster_exists:
                missing_posters['posters'].append(collection.title)

    return missing_posters

# TODO add_posters_for_new_posters
# if a poster was recently added to dropbox, upload it
# helpful if someone wants to change out a poster for a video older than one day


def execute():
    missing_posters = {
        'posters': [],
        'collections': []
    }

    missing_posters = add_posters_for_new_videos(video_type='movies', missing_posters=missing_posters)


    # missing_posters = add_posters_for_collections(missing_posters=missing_posters)

    # upload_new_posters(poster_type='movies')

    # TODO write missing posters to files
    # print(missing_posters)


if __name__ == '__main__':
    execute()
