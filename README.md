# LastfmSnap

LastfmSnap is a project designed to give last.fm users fine access to their data by helping them access snapshots of their listening history. The project is built using Python, and though there is a basic CLI, it isn't fully functional yet. A fully functional CLI is definetly a goal, and some other goals include a GUI, more time options, graphs, export to CSV/TXT, & perhaps even a webpage.

## Usage

While you *could* just run `cli.py`, it isn't fully functional, and so it is highly reccomended to import `scrape.py` and make queries using a scrape object, as seen in `test.py`. Try it! Go run `test.py`!

```
import scrape
sc = scrape.scrape("10", "2022-01-01", "TODAY", "vishwarrior")
print(sc.artistInfo())
```

This would print the user `vishwarrior`'s top 10 most scrobbled artists from the start of 2022 to the current date. Like most, if not all, methods in scape.py, `artistInfo()` returns an list, meaning that you could do whatever with that data, eg. sort alphabetically, slice it, etc. LastfmSnap aims to give you a snapshot of your last.fm listening history in an easily parasable way so that you can do whatever with it!

### Modules:
LastfmSnap uses some Python modules that you would have to install (`BeautifulSoup`, `requests`, `pandas`, `unidecode`). You need to `pip install` these if you haven't already installed them.

## Questions/Bugs/Feature Requests

The documentation of each method hopefully should clear any doubts regarding their functionality, but if you have any questions or note any bugs, please create an issue. I'd greatly appreciate any 'auditing' of my code, especially with regards to performance. Also, if there is any added functionality you'd like to see, feel free to submit a pull request or make a feature request!
