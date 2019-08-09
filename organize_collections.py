import settings
import requests
import json
import os

import logging
import sys

root = logging.getLogger()
root.setLevel(logging.DEBUG)

handler = logging.StreamHandler(sys.stdout)
handler.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
root.addHandler(handler)

base_url = settings.TRAKT_BASE_URL

client_id = settings.TRAKT_CLIENT_ID
client_secret = settings.TRAKT_CLIENT_SECRET
redirect_uri = settings.TRAKT_REDIRECT_URI

user_id = settings.TRAKT_DEFAULT_USER_ID

headers = {
    'Content-Type': 'application/json',
    'trakt-api-key': client_id,
    'trakt-api-version': '2'
}


def get_response(url):
    r = requests.get(url, headers=headers)
    return r.json()


def get_user_lists():
    logging.info(f'Getting lists for user: {user_id}')
    return get_response(url=f'{base_url}/users/{user_id}/lists/')


def get_list(list_id):
    logging.info(f"Getting list with list_id: {list_id}")
    return get_response(url=f'{base_url}/users/{user_id}/lists/{list_id}/items/')


def generate_grouped_lists():
    lists = get_user_lists()

    groups = {
        'videos': {},
        'people': {},
    }

    for l in lists:
        list_name = l['name']
        list_id = l['ids']['trakt']

        logging.info(f'Found list: "{list_name}"')
        if list_name.startswith('COLLECTION'):
            logging.info(f'Adding list "{list_name}" to group "videos"')
            groups['videos'][list_id] = list_name

        elif list_name.startswith('HOLIDAY'):
            logging.info(f'Adding list "{list_name}" to group "videos"')
            groups['videos'][list_id] = list_name

        elif list_name.startswith('WINNERS'):
            logging.info(f'Adding list "{list_name}" to group "videos"')
            groups['videos'][list_id] = list_name

        elif list_name.startswith('NOMINEES'):
            logging.info(f'Adding list "{list_name}" to group "videos"')
            groups['videos'][list_id] = list_name

        elif list_name.startswith('TAG'):
            logging.info(f'Adding list "{list_name}" to group "videos"')
            groups['videos'][list_id] = list_name

        elif list_name.startswith('PEOPLE'):
            logging.info(f'Adding list "{list_name}" to group "people"')
            groups['people'][list_id] = list_name

        else:
            logging.info(f'Ignoring list "{list_name}"')


    return groups


def _add_to_collection_dict(video, title, list_name, group):
    video_exists = video.get(title)
    if not video_exists:
        video[title] = {f'{group}': []}

    group_exists = video[title].get(group)
    if not group_exists:
        video[title][group] = []

    video[title][group].append(list_name)
    return video[title]


def update_collections_group(list_data):
    movies = {}

    shows = {}

    for list_id, list_name in list_data.items():
        list_details = get_list(list_id=list_id)

        for video in list_details:
            video_type = video['type']
            title = video[video_type]["title"]

            if video_type == 'movie':
                movies = _add_to_collection_dict(
                    video=movies,
                    title=title,
                    list_name=list_name
                )
            elif video_type == 'show':
                shows = _add_to_collection_dict(
                    video=shows,
                    title=title,
                    list_name=list_name
                )

            logging.info(f'Adding "{title}" to collection group "{video_type}"')

    write_json(group='movies', data=movies)
    write_json(group='shows', data=shows)


def write_json(group, data):
    file_path = os.path.join(settings.ROOT, 'data', f'{group}.json')
    with open(file_path, 'w') as outfile:
        logging.info(f'Writing to file: {file_path}')
        json.dump(data, outfile)


def groups_by_video(groups):
    for group, list_data in groups.items():

        if group in settings.COLLECTIONS:
            logging.info(f'Working on group: {group}')
            update_collections_group(list_data=list_data)


if __name__ == '__main__':
    movies = {}
    shows = {}

    groups = generate_grouped_lists()

    video_lists = groups['videos']

    for list_id, list_name in video_lists.items():
        list_details = get_list(list_id=list_id)

        for video in list_details:
            video_type = video['type']
            title = video[video_type]["title"]

            for trakt_tag, tag_config in settings.TRAKT_TAGS.items():
                if trakt_tag != 'PEOPLE':
                    if list_name.startswith(trakt_tag):
                        short_list_name = list_name.replace(f'{trakt_tag} - ', ''),
                        if video_type == 'movie':
                            movies[title] = _add_to_collection_dict(
                                video=movies,
                                title=title,
                                list_name=short_list_name,
                                group=tag_config['group']
                            )
                        elif video_type == 'show':
                            shows[title] = _add_to_collection_dict(
                                video=shows,
                                title=title,
                                list_name=short_list_name,
                                group=tag_config['group']
                            )

    write_json(group='movies', data=movies)
    write_json(group='shows', data=shows)
