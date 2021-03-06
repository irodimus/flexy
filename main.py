from scripts import update_video_settings
from scripts import update_collection_settings
from scripts import delete_single_video_collections
from scripts import check_for_missing_collection_videos
from scripts import update_posters
from utils import create_trakt_groups

import settings

if __name__ == '__main__':
    # Setup
    create_trakt_groups

    # Update Video Settings: add videos to collections, add trophies for Oscar winners and nominees, update genre tags
    update_video_settings.execute()

    # Update Collection Settings: set collection image, collection mode, and collection ordering
    update_collection_settings.execute()

    # Delete Single Video Collections
    delete_single_video_collections.execute()

    # Upload Posters: for individual movies and collections
    update_posters.execute()

    # Other
    if settings.FIND_MISSING_VIDEOS:
        check_for_missing_collection_videos.execute()  # Be warned: this can be a long running script.
