## Uses solace Native Python API
import os
import platform
import time
import json
from textblob import TextBlob

# Import Solace Python  API modules from the solace package
from solace.messaging.messaging_service import MessagingService, ReconnectionListener, ReconnectionAttemptListener, ServiceInterruptionListener, RetryStrategy, ServiceEvent
from solace.messaging.resources.topic_subscription import TopicSubscription
from solace.messaging.receiver.message_receiver import MessageHandler, InboundMessage

if platform.uname().system == 'Windows': os.environ["PYTHONUNBUFFERED"] = "1" # Disable stdout buffer 

TOPIC_PREFIX = "sentiment/v1"

# Handle received messages
class MessageHandlerImpl(MessageHandler):
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

    def on_message(self, message: InboundMessage):
        topic = message.get_destination_name()
        payload_str = message.get_payload_as_string()
        print(f"Received message on: {topic} \nMessage Payload String: {payload_str} \n")
        payload_json = {"tweetBody": payload_str}
        res = self.sentiment_analyzer(payload_json,"")
        print(res)

# Inner classes for error handling
class ServiceEventHandler(ReconnectionListener, ReconnectionAttemptListener, ServiceInterruptionListener):
    def on_reconnected(self, e: ServiceEvent):
        print("\non_reconnected")
        print(f"Error cause: {e.get_cause()}")
        print(f"Message: {e.get_message()}")
    
    def on_reconnecting(self, e: "ServiceEvent"):
        print("\non_reconnecting")
        print(f"Error cause: {e.get_cause()}")
        print(f"Message: {e.get_message()}")

    def on_service_interrupted(self, e: "ServiceEvent"):
        print("\non_service_interrupted")
        print(f"Error cause: {e.get_cause()}")
        print(f"Message: {e.get_message()}")
    
# Broker Config
broker_props = {
    "solace.messaging.transport.host": os.environ.get('SOLACE_HOST') or "localhost",
    "solace.messaging.service.vpn-name": os.environ.get('SOLACE_VPN') or "default",
    "solace.messaging.authentication.scheme.basic.username": os.environ.get('SOLACE_USERNAME') or "default",
    "solace.messaging.authentication.scheme.basic.password": os.environ.get('SOLACE_PASSWORD') or "default"
    }

# Build A messaging service with a reconnection strategy of 20 retries over an interval of 3 seconds
# Note: The reconnections strategy could also be configured using the broker properties object
messaging_service = MessagingService.builder().from_properties(broker_props)\
                    .with_reconnection_retry_strategy(RetryStrategy.parametrized_retry(20,3))\
                    .build()

# Blocking connect thread
messaging_service.connect()
print(f'Messaging Service connected? {messaging_service.is_connected}')

# Error Handeling for the messaging service
service_handler = ServiceEventHandler()
messaging_service.add_reconnection_listener(service_handler)
messaging_service.add_reconnection_attempt_listener(service_handler)
messaging_service.add_service_interruption_listener(service_handler)

# Define a Topic subscriptions 
topics = [TOPIC_PREFIX + "/hashtag/>"]
topics_sub = []
for t in topics:
    topics_sub.append(TopicSubscription.of(t))

# Build a Receiver with the given topics and start it
direct_receiver = messaging_service.create_direct_message_receiver_builder()\
                        .with_subscriptions(topics_sub)\
                        .build()

direct_receiver.start()
print(f'Direct Subscriber is running? {direct_receiver.is_running()}')

try:
    print(f"Subscribing to: {topics}")
    # Callback for received messages
    direct_receiver.receive_async(MessageHandlerImpl())
    try: 
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print('\nDisconnecting Messaging Service')
finally:
    print('\nTerminating receiver')
    direct_receiver.terminate()
    print('\nDisconnecting Messaging Service')
    messaging_service.disconnect()