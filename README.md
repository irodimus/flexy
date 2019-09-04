## Set Up

Before running any scripts, you will need to update your PYTHONPATH to include flexy.

If you receive the following error, then it's because you need to export the python path.
``````
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