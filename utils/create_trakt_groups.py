import settings
import requests
import json
import os


class TraktGroups:

    def __init__(self):
        self.base_url = settings.TRAKT_BASE_URL

        self.client_id = settings.TRAKT_CLIENT_ID
        self.client_secret = settings.TRAKT_CLIENT_SECRET
        self.redirect_uri = settings.TRAKT_REDIRECT_URI

        self.user_id = settings.TRAKT_DEFAULT_USER_ID

        self.headers = {
            "Content-Type": "application/json",
            "trakt-api-key": self.client_id,
            "trakt-api-version": "2"
        }

        self.execute()

    def _add_to_collection_dict(self, video, title, list_name, group):
        video_exists = video.get(title)
        if not video_exists:
            video[title] = {}

        group_exists = video[title].get(group)
        if not group_exists:
            video[title][group] = []

        video[title][group].append(list_name)
        return video[title]

    def get_response(self, url):
        r = requests.get(url, headers=self.headers)
        return r.json()

    def get_user_lists(self):
        print("Getting lists for user: {user_id}".format(user_id=self.user_id))
        return self.get_response(
            url="{base_url}/users/{user_id}/lists/".format(base_url=self.base_url, user_id=self.user_id))

    def get_list(self, list_id):
        print(f'Getting list with list_id: {list_id}'.format(list_id=list_id))
        return self.get_response(
            url="{base_url}/users/{user_id}/lists/{list_id}/items/".format(base_url=self.base_url,
                                                                                     user_id=self.user_id,
                                                                                     list_id=list_id))

    def generate_grouped_lists(self, lists):
        """
        People-based collections need to be updated differently so they get separated out.
        """

        groups = {
            "videos": {},
            "people": {},
        }

        for l in lists:
            list_name = l["name"]
            list_id = l["ids"]["trakt"]

            print("Found list: '{list_name}'".format(list_name=list_name))
            if list_name.startswith("COLLECTION"):
                print("Adding list '{list_name}' to group 'videos'".format(list_name=list_name))
                groups["videos"][list_id] = list_name

            elif list_name.startswith("HOLIDAY"):
                print("Adding list '{list_name}' to group 'videos'".format(list_name=list_name))
                groups["videos"][list_id] = list_name

            elif list_name.startswith("WINNERS"):
                print("Adding list '{list_name}' to group 'videos'".format(list_name=list_name))
                groups["videos"][list_id] = list_name

            elif list_name.startswith("NOMINEES"):
                print("Adding list '{list_name}' to group 'videos'".format(list_name=list_name))
                groups["videos"][list_id] = list_name

            elif list_name.startswith("TAG"):
                print("Adding list '{list_name}' to group 'videos'".format(list_name=list_name))
                groups["videos"][list_id] = list_name

            elif list_name.startswith("PEOPLE"):
                print("Adding list '{list_name}' to group 'people'".format(list_name=list_name))
                groups["people"][list_id] = list_name

            else:
                print("Ignoring list '{list_name}'".format(list_name=list_name))

        return groups

    def write_json(self, group, data):
        root_data = os.path.join(settings.ROOT, "data")

        if not os.path.exists(root_data):
            print("Creating root 'data' file path: {root_data}".format(root_data=root_data))
            os.makedirs(root_data)

        file_path = os.path.join(root_data, "{group}.json".format(group=group))
        with open(file_path, "w") as outfile:
            print("Writing to file: {file_path}".format(file_path=file_path))
            json.dump(data, outfile)

    def execute(self):
        """
        Loops through Trakt lists and adds each video to a json file with each collection, holiday, oscar status and
        tag appropriate for the video. This makes it easier to match Plex videos for updates.

        Example:
            {
              {
                "The Lord of the Rings: The Fellowship of the Ring": {
                  "collections": ["Middle Earth"],
                  "nominees": ["Oscars Best Picture"]
              }, ...
            }
        """
        movies = {}
        shows = {}

        lists = self.get_user_lists()
        groups = self.generate_grouped_lists(lists=lists)

        video_lists = groups["videos"]

        for list_id, list_name in video_lists.items():
            list_details = self.get_list(list_id=list_id)

            for video in list_details:
                video_type = video["type"]
                title = "{title} ({year})".format(title=video[video_type]['title'], year=video[video_type]['year'])

                for trakt_tag, tag_config in settings.TRAKT_TAGS.items():

                    if trakt_tag != "PEOPLE":

                        if list_name.startswith(trakt_tag):
                            short_list_name = list_name.replace("{trakt_tag} - ".format(trakt_tag=trakt_tag), "")

                            if video_type == "movie":
                                movies[title] = self._add_to_collection_dict(
                                    video=movies,
                                    title=title,
                                    list_name=short_list_name,
                                    group=tag_config["group"]
                                )

                            elif video_type == "show":
                                shows[title] = self._add_to_collection_dict(
                                    video=shows,
                                    title=title,
                                    list_name=short_list_name,
                                    group=tag_config["group"]
                                )

                    # TODO add people process

        self.write_json(group="movies", data=movies)
        self.write_json(group="shows", data=shows)


if __name__ == "__main__":
    TraktGroups().execute()
