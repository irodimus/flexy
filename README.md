## Python Set Up

Before running any scripts, you will need to update your PYTHONPATH to include flexy.

If you receive the following error, then it's because you need to export the python path.
```
Traceback (most recent call last):
  File "update_video_settings.py", line 3, in <module>
    import settings
ModuleNotFoundError: No module named 'settings'
```

On a Mac, you can do this by adding the following line to your `.bash_profile`.
```
export PYTHONPATH=$PYTHONPATH:<path_to_flexy>y
```
After updating the file, run `source ~/.bash_profile` to update the settings.


## Flexy Set Up

Rename `settings-template.py` to `settings.py`.

### Trakt

Before running anything dealing with collections or videos, you must run: 
```
$ python utils/create_trakt_groups.py
```

This creates a json replica of your Trakt account to limit hits to the API.
Once it's ran, you won't need to run it again until you make changes to your Trakt lists.

For an example of how I set up my Trakt lists, you can check my [account](https://trakt.tv/users/proftensions/lists).

### Dropbox

Add your DropBox token to `DROPBOX_TOKEN` in settings.py to get access.
Add a folder for collections and one for movies, making sure the file names match their respective item.

Update `SEMICOLON_REPLACEMENT` with your value of choice so the code can find matches between titles and file names.

### Scripts

You can run individual functions by doing something like this:
```
python -c 'import scripts.update_video_settings as a; a.execute()'
```

Otherwise, I have grouped similar ones together and made heavy use of variables to decide which functions are called.
There is also a `main.py` that will run everything so if your settings are set up properly, you can run the main
file in a bash script on a nightly basis. If I already mentioned that somewhere in this, my apologies.

#### add videos to collections
```
$ python scripts/update_video_settings.py
```

Any list in your Trakt account that is prefixed with `COLLECTION` or `HOLIDAY` will be converted into a 
collection and all movies or tv shows in that Trakt list will be added to the collection.


#### add genres to videos
```
$ python scripts/update_video_settings.py
```
Any list in your Trakt account that is prefixed with `TAG` will be converted into a 
genre tag and applied to all movies or tv shows in that list.

If you don't want the tag `Oscar Best Picture Winner` applied, set `ADD_OSCAR_TAG` in
the `settings.py` file to `False`.

If you don't want the tags `4K Videos` or `8K Videos` applied, set `ADD_QUALITY_TAG`
in the the `settings.py` file to `False`.


#### add icons to titles
```
$ python scripts/update_video_settings.py
```

Any movie in the Trakt list `COLLECTION - Oscar Best Picture Winners` will have a little 
trophy (🏆) added to the title while any movie in `COLLECTION - Oscar Best Picture Nominees`
will have a little medal (🥈) added to the title.

If you don't want this feature, set `ADD_WINNERS_TROPHY` and `ADD_NOMINEES_MEDAL` in the 
`settings.py` file to `False`.


#### add quality suffixes to titles
```
$ python scripts/update_video_settings.py
```
Any movie in Plex that meets the requirements for 4K or 8K gets a suffix applied
to the title. 

If you don't want the suffixes `(4K)` or `(8K)` applied, set `ADD_QUALITY_SUFFIX`
in the the `settings.py` file to `False`.


#### upload poster for individual movies
```
$ python scripts/update_posters.py
```

Will search for a poster for any movies added to Plex within the last 24 hours and will
update any posters added to the `movies` DropBox folder within the last 24 hours.


#### upload poster for collections
```
$ python scripts/update_posters.py
```

Will search for a poster for any collections added to Plex within the last 24 hours and will
update any posters added to the `collections` DropBox folder within the last 24 hours.


#### write a JSON of movies and collections missing custom posters
```
$ python scripts/update_posters.py
```

Will write out a json file for any movies added within the last 24 hours that is missing a poster.

Note: if you'd like to extend the 24 hour window, then update the `DAYS_TO_CHECK` variable in
`settings.py`.


#### update collection mode and sort
```
$ python scripts/update_collection_settings.py
```

Plex has 4 modes for how a collection is displayed:
```
modes = {
    -1: "Library default",
    1: "Hide items in this collection",
    2: "Show this collection and its items",
    0: "Hide collection"
}
```

The default settings of flexy will set any collections with more than 10 videos to "Show this collection and its items"
while anything less is set to "Hide items in this collection". If you'd like to change the minimum
quantity of videos, update the `HIDE_VIDEOS_MAX_COLLECTION_LENGTH` in `settings.py`.

If there are collections where you'd like to ignore the max length, add the name to `IGNORE_COLLECTION_LENGTH` in `settings.py`.
A use-case would be for the Star Trek movies. You know pretty easily whether or not you want to watch a
Star Trek movie and you don't have to scroll through 14 videos to figure that out.

If there are collections where you'd always like to show the videos, add the name to `ALWAYS_SHOW_VIDEOS_IN_COLLECTION` in `settings.py`.
A use-case would be for the Marvel or DC cinematic universes. Not everyone knows which movies belong in those collections.

Other setting options: 

* `ALWAYS_HIDE_COLLECTION`: just add the collection name to the list
* `SORT_VIDEOS_BY_RELEASE_MAX_COLLECTION_LENGTH`: defaults to 10 and works under the assumption that with more videos in a collection, it's easier to browse alphabetically
* `ALWAYS_SORT_BY_RELEASE_DATE`: just add the collection name to the list
* `ALWAYS_SORT_ALPHABETICALLY`: just add the collection name to the list


#### show/hide holiday-specific collections from library
```
$ python scripts/update_collection_settings.py
```
To add collections you'd like available during certain windows of time (usually holiday-specifc),
update the `HOLIDAY_COLLECTIONS` variable in `settings.py`.

For example:
```
HOLIDAY_COLLECTIONS = {
    "Christmas Time": ("12-01", "12-31"),
    "Halloween Time": ("10-01", "11-01"),
}
```

You also have the option of remove out-of-season collections all together by setting the 
`DELETE_OUT_OF_SEASON_COLLECTIONS` variable to `True` in `settings.py`. Else, you can just hide the collection
from the main view (mode 0) by setting it to `False`. If you choose to delete the collection, it will still
be rebuilt and available when it is in season.


#### write a JSON of movies missing from Trakt lists
```
$ python scripts/check_for_missing_collection_videos.py
```

Compares your Trakt lists with your Plex library and creates a JSON of videos missing from Plex.
Useful for finding other items to focus on collecting.

Only run if you find this information valuable as it is a time-consuming script. The `FIND_MISSING_VIDEOS` variable
is defaulted to `False`, set to `True` if you would like it to run.

If there are collections where you're not concerned about getting all of the videos, add them to `IGNORE_MISSING_VIDEOS`
in `settings.py`. I use it for holiday-specific movies. I don't need all of the Christmas movies ever made.


#### remove single video collections
```
$ python scripts/delete_single_video_collections.py
```

Loops through collections and removes any with only one video. If you have collections that are for grouping 
a tv show with a movie (Firefly 🍃 , Twin Peaks, The X-Files, etc), add them to the `IGNORE_SINGLE_VIDEO_COLLECTIONS`
list in `settings.py`. 


### Clean Up

Mistakes happen.

#### delete_all_collections
```
$ python scripts/delete_all_collections.py
```

Pretty self-explanatory. Deletes all collections.

#### delete_all_trophies
```
$ python scripts/delete_all_trophies.py
```

Pretty self-explanatory. Removes trophies from titles.

#### delete_tag
```
$ python scripts/delete_tag.py --genre='Bad Genre'
```

Pretty self-explanatory. Removes a tag you don't want or have one you hate seeing for _some_ reason.

#### end

This has been my TED talk about how to spend more time on automating organizational processes than it would have taken you do to by hand.
