import paho.mqtt.client as mqtt
import os
import json

def on_connect(client, data, flags, rc):
    assert (rc == 0), "Error Connecting. Return code: " + str(rc)
    print("Connected to Tamimi's Broker!")

    for t in topics:
        print("Subscribing to: " + t)
        client.subscribe(t)

def on_message(client, data, msg):
    print("Received message on: %s\n %s" % (msg.topic, msg.payload))
    payload_json = {"tweetBody": msg.payload}
    res = sentiment_analyzer(payload_json,"")
    # msg_decode = msg.payload.decode("utf-8")
    # print("Received message on: %s\n %s" % (msg.topic, msg_json_pretty))

def sentiment_analyzer(self, event, context):
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
# Broker Info
url = os.environ.get('SOLACE_HOST')
username = os.environ.get('SOLACE_VPN')
password = os.environ.get('SOLACE_USERNAME')
PORT=8883


topics = [
    "sentiment/v1/hastag"
    "sentiment/v1/user"
]

client = mqtt.Client()
client.username_pw_set(username=username, password=password)
# Note: Make sure you have this installed in the same dir
client.tls_set(ca_certs="./DigiCert_Global_Root_CA.pem")

client.on_connect = on_connect
client.on_message = on_message


print("Attempting to connect...")
client.connect(url, port=PORT)
client.loop_forever()