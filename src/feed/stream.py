# sampled_stream.py
## Uses MQTT to stream to Solace

import json
from twitter_stream import SampledStream

class Stream(SampledStream):
    user_fields = ['name', 'location', 'public_metrics']
    expansions = ['author_id']
    tweet_fields = ['created_at']

stream = Stream()
for tweet in stream.connect():
    print(json.dumps(tweet, indent=4))