# DGCharacterGenerator

This generates random character stats and skills for Arc Dream's game [Delta Green](http://www.delta-green.com/). Right now there is limited functionality. Right now, it prints the character stats to stdout. By default, the generator selects professions that suit the statistics of the character it generated. You can turn this off and have professions be totally random, but you have to alter the script to do it. Command line args will be added in the next release, to let you disable this and also to specify professions and backgrounds.

Currently, only the generic professions are available, i.e. the ones on pages 20-24. Specific agency builds will be added in a future release.

## To Run

You must have Python 2.6 or higher installed. 

Make sure all files are in the same directory and run the command ``python gen_random.py``. 

To turn off smart, open ``gen_random.py`` and changed line 107 to:

```python
make_random_character(False)
```
