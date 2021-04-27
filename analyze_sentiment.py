import json
from textblob import TextBlob


def lambda_handler(event, context):
    tweet_body = event.get('tweetBody')

    if not tweet_body:
        return {
            'statusCode': 400,
            'body': 'Invalid tweet input submitted for sentiment analysis'
        }

    testimonial = TextBlob(tweet_body)
    sentiment_polarity = testimonial.sentiment.polarity
    sentiment_subjectivity = testimonial.sentiment.subjectivity

    response = {'sentiment_polarity': sentiment_polarity,
                'sentiment_subjectivity': sentiment_subjectivity,
                'stripped_input': testimonial.stripped}
    return {
        'statusCode': 200,
        'body': json.dumps(response)
    }


# if __name__ == '__main__':
#     event = {'tweetBody': 'Tamimi is the best developer in the world'}
#     resp = lambda_handler(event,"")
#
#     print(resp)