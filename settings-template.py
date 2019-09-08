from datetime import date
import os

# DROPBOX ##############################################################################################################
DROPBOX_TOKEN = "not_implemented"

# GENERAL ##############################################################################################################
TODAY = date.today().strftime("%Y-%m-%d")
ROOT = os.path.dirname(os.path.realpath(__file__))

SEMICOLON_REPLACEMENT = ""

# PLEX #################################################################################################################
PLEX_URL = "not_implemented"
PLEX_TOKEN = "not_implemented"

# Update Video Settings ------------------------------------------------------------------------------------------------

ADD_WINNERS_TROPHY = True
ADD_NOMINEES_MEDAL = True
ADD_OSCAR_TAG = True

# for adding a 4K/8K tag to the end of movies like "Movie Name (4K)" or for adding a 4K tag to the movie
# if you want both, set both to True
ADD_QUALITY_SUFFIX = True
ADD_QUALITY_TAG = True

# Update Collection Settings -------------------------------------------------------------------------------------------

# quantity of videos allowed in collection before you stop hiding them, works under the assumption that collections with
# more videos probably aren't related so it would be beneficial to see them individually
HIDE_VIDEOS_MAX_COLLECTION_LENGTH = 10

# collections to hide videos regardless of how many videos are in it because I don't need to see all 14 Star Trek movies
IGNORE_COLLECTION_LENGTH = []

# collections where you always want the videos to show, useful for collections like holidays or genre-specific ones
ALWAYS_SHOW_VIDEOS_IN_COLLECTION = []

ALWAYS_HIDE_COLLECTION = []

# works under the assumption that with more videos in a collection, it's easier to browse alphabetically
SORT_VIDEOS_BY_RELEASE_MAX_COLLECTION_LENGTH = 10
ALWAYS_SORT_BY_RELEASE_DATE = []
ALWAYS_SORT_ALPHABETICALLY = []

# if you'd like to completely remove the out of season collection, set to True
# if you'd like to just hide the collection from the main view, set to False
DELETE_OUT_OF_SEASON_COLLECTIONS = True

# Collection Name: (Starting month-year, Ending month-year)
# Note: can't cross over years, Christmas can't go from "12-01" to "01-01"
HOLIDAY_COLLECTIONS = {
}

# Delete Single Video Collections --------------------------------------------------------------------------------------

REMOVE_SINGLE_VIDEO_COLLECTIONS = True

# When trying to group tv shows and movies together, some get removed because there's usually two items: one movie and
# one tv show, but since it's by section, it's only sees "one movie" or "one tv show"
IGNORE_SINGLE_VIDEO_COLLECTIONS = []

# Check For Missing Videos In Collections ------------------------------------------------------------------------------
IGNORE_MISSING_VIDEOS = []

# POSTERS ##############################################################################################################

DAYS_TO_CHECK = 1

# TMDB #################################################################################################################

TMDB_REQUEST_COUNT = 0
TMDB_URL = "https://api.themoviedb.org/3"

TMDB_API_KEY = "not_implemented"

# TRAKT ################################################################################################################
TRAKT_BASE_URL = "https://api.trakt.tv"
TRAKT_DEFAULT_USER_ID = "proftensions"  # update with your own id

FIND_MISSING_VIDEOS = False

# don't change unless you know what you're doing -----------------------------------------------------------------------
TRAKT_TAGS = {
    "COLLECTION": {"group": "collections"},
    "HOLIDAY": {"group": "collections"},
    "WINNERS": {"group": "winners"},
    "NOMINEES": {"group": "nominees"},
    "TAG": {"group": "tag"},
    "PEOPLE": {"group": "people"}
}

COLLECTIONS = ["collections"]
PEOPLE = ["people"]
TROPHIES = ["oscar_winners", "oscar_nominees"]
TAGS = ["tags"]
