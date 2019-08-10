import os

from datetime import date
import settings
from scripts.newsletter import Newsletter

today = date.today().strftime('%Y-%m-%d')

root = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))


def check_for_missing_posters():
    section_title = 'Movies Missing Posters'
    posters = ['poster.jpg', 'poster.png']

    titles = {section_title: []}
    for subdir, dirs, files in os.walk(settings.MOVIES_DIR):
        poster_exists = [file for file in posters if file.lower() in files]

        if not poster_exists and subdir != settings.MOVIES_DIR:
            titles[section_title].append(os.path.basename(subdir))

    return titles


if __name__ == '__main__':
    n = Newsletter()

    missing_posters = check_for_missing_posters()
    n.write_config(params=missing_posters)
