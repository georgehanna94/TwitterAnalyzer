import json
import requests


sentences = [
    'The food we had yesterday was delicious',
    'My time in Italy was very enjoyable',
    'I found the meal to be tasty',
    'The internet was slow.',
    'Our experience was suboptimal'
]


def lambda_handler(event, context):


    url = "http://localhost:8000/dep"
    message_text = "They ate the pizza with anchovies"
    headers = {'content-type': 'application/json'}
    d = {'text': message_text, 'model': 'en'}

    response = requests.post(url, data=json.dumps(d), headers=headers)
    r = response.json()

    for sentence in sentences:
        doc = nlp(sentence)
        for token in doc:
            print(token.text, token.dep_, token.head.text, token.head.pos_,
                  token.pos_, [child for child in token.children])

    aspects = []
    for sentence in sentences:
        doc = nlp(sentence)
        descriptive_term = ''
        target = ''
        for token in doc:
            if token.dep_ == 'nsubj' and token.pos_ == 'NOUN':
                target = token.text
            if token.pos_ == 'ADJ':
                prepend = ''
                for child in token.children:
                    if child.pos_ != 'ADV':
                        continue
                    prepend += child.text + ' '
                descriptive_term = prepend + token.text
        aspects.append({'aspect': target,
                        'description': descriptive_term})
    print(aspects)

    return {
        'statusCode': 200,
        'body': 'mama 5alast'
    }

if __name__ == '__main__':
    lambda_handler({},"")