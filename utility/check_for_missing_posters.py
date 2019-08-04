import os
import yaml

root = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
movies_directory = os.path.join(root, 'data')
components_dir = os.path.join(root, 'newsletter', 'components')


def write_to_yaml(titles):
    file_path = os.path.join(components_dir, 'newsletter.yml')
    d = {'Movies Missing Poster': titles}

    with open(file_path, 'w') as yaml_file:
        yaml.dump(d, yaml_file, default_flow_style=False)


def check_for_missing_posters(directory):
    posters = ['poster.jpg', 'poster.png']

    titles = []
    for subdir, dirs, files in os.walk(directory):
        poster_exists = [file for file in posters if file.lower() in files]
        if not poster_exists and subdir != movies_directory:
            titles.append(os.path.basename(subdir))

    return titles


if __name__ == '__main__':
    titles = check_for_missing_posters(directory=movies_directory)
    write_to_yaml(titles=titles)
