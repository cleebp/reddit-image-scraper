# Reddit Image Scraper

Python script to crawl over given subreddit or multireddit links and download all top images and gifs locally.

## How to Run

Install chromedriver:
- `brew tap homebrew/cask`
- `brew cask install chromedriver`

Install requirements:
- `python3 -m venv venv`
- `source venv/bin/activate`
- `pip install -r requirements.txt`

Setup your config file:
- `cp src/config_default.py src/config.py`
- Add subreddit or multireddit links

Run the scraper:
- `python src/run.py`
- ...
- _profit?_