import json
import os

import settings


def clean_title(title):
    """
    Removes added icons from titles so they can continue to be matched to Trakt lists.
    """
    extras = ["🏆 ", "🥈 ", " (4K)", " (8K)"]
    for extra in extras:
        title = title.replace(f"{extra}", "")
    return title


def generate_url(params):
    """
    Concatenates parameters for Plex API call.
    """
    url = params["base_url"]
    for key, value in params.items():
        if key != "base_url":
            url += f"{key}={value}&".format(key=key, value=value)

    return url[:-1]


def get_sections_by_type(plex):
    """
    Movies and TV Shows have slightly different attributes so they need to be processed differently.
    """
    sections_by_type = {
        "movies": [],
        "shows": []
    }

    plex_sections = plex.library.sections()

    for plex_section in plex_sections:

        if plex_section.type == "movie":
            sections_by_type["movies"].append(plex_section.title)

        elif plex_section.type == "show":
            sections_by_type["shows"].append(plex_section.title)

    return sections_by_type


def get_type_id(type):
    """
    Used for Plex API calls.
    """
    return {
        "movie": 1,
        "show": 2,
        "season": 3,
        "episode": 4,
        "collection": 18
    }.get(type, None)


def open_trakt_json(group):
    """
    Read Trakt jsons for updates.
    """
    root_data = os.path.join(settings.ROOT, "data")
    file_path = os.path.join(root_data, f"{group}.json".format(group=group))

    try:
        with open(file_path, "r") as f:
            config = json.load(f)
        return config
    except FileNotFoundError as error:
        print(error)
        print("\nYou must run the create_trakt_groups.py file before using this method.")
        exit()


def write_json(group, data):
    root_data = os.path.join(settings.ROOT, "data")

    if not os.path.exists(root_data):
        print("Creating root 'data' file path: {root_data}".format(root_data=root_data))
        os.makedirs(root_data)

    file_path = os.path.join(root_data, "{group}.json".format(group=group))
    with open(file_path, "w") as outfile:
        print("Writing to file: {file_path}".format(file_path=file_path))
        json.dump(data, outfile)
