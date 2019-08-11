
def get_type_id(type):
    """
    Used for Plex API calls. As far as I know, movies are type 1 and tv shows are type 2.
    """
    return {
        'movie': 1,
        'show': 2
    }.get(type, None)


def generate_url(params):
    """
    Concatenates parameters for Plex API call
    """
    url = params['base_url']
    for key, value in params.items():
        if key != 'base_url':
            url += f'{key}={value}&'

    return url[:-1]


def clean_title(title):
    """
    Removes added icons from titles so they can continue to be matched to Trakt lists.
    """
    icons = ['🏆', '🥈']
    for icon in icons:
        title = title.replace(f'{icon} ', '')
    return title
