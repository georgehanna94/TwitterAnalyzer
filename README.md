# TwitterAnalyzer

A home-made hackathon brought to you by your favourite egyptian and jordan fools

## Prerequisites

1. Install python
   1. Recommended: use vitrual environments `python3 -m venv venv`
   1. Activate virtual environment `source venv/bin/activate`
1. Update pip `pip install --upgrade pip`
1. Install dependencies
   1. `pip install -r requiremnets/txt`

## Dirs

### Feed

Contains the code to query the feed given a hashtag input. Store the twitter credential at `~/.twitter-keys.yaml`

```
keys:
    consumer_key: CONSUMER_KEY
    consumer_secret: CONSUMER_SECRET
    access_token: ACCESS_TOKEN
    access_token_secret: ACCESS_TOKEN_SECRET
    bearer_token: BEARER_TOKEN

```

### Sentiment

1. `SOLACE_HOST=<broker_url> SOLACE_VPN=<solace_VPN> SOLACE_USERNAME=<username> SOLACE_PASSWORD=<password> python analyzer_sentiment.py`
