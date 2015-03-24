# SLMPD scraper

## Getting started

* Step 0: Have virtualenv and virtualenvwrapper installed.

```
sudo pip install virtualenv virtualenvwrapper
```

* Step 1: Make a virtualenv and install requirements.

```
git clone git@github.com:jeremyjbowers/slmpd.git && cd slmpd
mkvirtualenv slmpd
pip install -r requirements.txt
```

* Step 2: Run the scraper.
```
./scraper.py
```

This shouldn't download any new files until they add them.
