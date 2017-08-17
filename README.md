# DGCharacterGenerator

This generates random character stats and skills for Arc Dream's game [Delta Green](http://www.delta-green.com/), and prints the character stats to stdout. 

Currently, only the generic professions are available, i.e. the ones on pages 20-24. Specific agency builds will be added in a future release.

## To Run

You must have Python 2.6 or higher installed. 

Run the command ``python DGCharacterGenerator.py`` on your favorite command line. 

## Options

You can view a full list of options by running the ``--help`` command. 

### Generating Multiple Characters

The ``-m`` or ``--make`` flag, together with a number, allows you to specify how many characters you want. For example, this is how to generate 4 federal agents, with stats optimized for the profession:

```bash
DGCharacterGenerator.py -p 'federal agent' -o -m 4
```

### Specifying Background and Profession:

The flags ``-p`` and ``-b`` (``--profession`` and ``--background``) allow you to specify which profession or background you would like your character to have. Currently, only the generic professions are avialable, so you can be a Federal Agent but not an Navy/ONI operator. 

You don't have to copy the profession or background name exactly- you can look in ``DGCharacterGenerator.py`` to see which words the generator will recognize. Be sure to use single or double quotations marks if there is more that one word in the profession: ``"federal agent"``, not ``federal agent``.

### Optimization

The flag ``-o`` (``--optimize``) attempts to make the best character possible with a given inupt. If a profession is not selected, the generator randomly create stats, then  look through the recommended stats for each profession, and select a profession that which best matches the stats.

If profession is selected, the generator will create a certain number of random stats, then select the stats which are highest in the stats associated with that profession. The default number of random stat sets generated is 3, but you can change that using the ``-g`` flag.

This command will generate a pretty good cop:

```bash
python DGCharacterGenerator.py -p cop -o
```

This will create a supercop:

```bash
python DGCharacterGenerator.py -p cop -o -g 15
```
