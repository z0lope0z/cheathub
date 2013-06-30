#CheatHub
-----------------------

This script automatically pushes code taken from the interwebs

## General Requirements

* [Python 2.7 or higher](http://www.python.org/download/releases/2.7/)
* [Beautiful Soup 4](http://www.crummy.com/software/BeautifulSoup/)

```
  pip install beautifulsoup4
```

## Configuration
You will need to modify setup.cfg

* github repo - the github repository wherein you want to place your files
* urls - a list of urls where the python code is taken
* last_date - modified by the script so it knows when was the last time it was run


### Example
```
[github]
github_repo = git@github.com:z0lope0z/cheathub-files.git

[links]
urls = http://code.google.com/p/aima-python/, http://www.google.com/

[config]
last_date = Jun 30 2013 10:30AM
```
