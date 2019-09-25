# <imports>
# -*- coding: utf-8 -*-

import os
from azure.cognitiveservices.language.textanalytics import TextAnalyticsClient
from msrest.authentication import CognitiveServicesCredentials
# </imports>

# <initialVars>
key_var_name = 'TEXT_ANALYTICS_SUBSCRIPTION_KEY'
if not key_var_name in os.environ:
    raise Exception('Please set/export the environment variable: {}'.format(key_var_name))
subscription_key = os.environ[key_var_name]

endpoint_var_name = 'TEXT_ANALYTICS_ENDPOINT'
if not endpoint_var_name in os.environ:
    raise Exception('Please set/export the environment variable: {}'.format(endpoint_var_name))
endpoint = os.environ[endpoint_var_name]
# <initialVars>

"""Language detection.

    This example detects the language of several strings. 
    """
# <languageDetection>
def language_detection():
    
    credentials = CognitiveServicesCredentials(subscription_key)
    text_analytics = TextAnalyticsClient(
        endpoint=endpoint, credentials=credentials)

    try:
        documents = [
            {'id': '1', 'text': 'This is a document written in English.'},
            {'id': '2', 'text': 'Este es un document escrito en Español.'},
            {'id': '3', 'text': '这是一个用中文写的文件'}
        ]
        response = text_analytics.detect_language(documents=documents)

        for document in response.documents:
            print("Document Id: ", document.id, ", Language: ",
                  document.detected_languages[0].name)

    except Exception as err:
        print("Encountered exception. {}".format(err))
language_detection()
# </languageDetection>


"""Key-phrases.

Returns the key talking points in several text examples.
"""
# <keyPhrases>
def key_phrases():
    
    credentials = CognitiveServicesCredentials(subscription_key)
    text_analytics = TextAnalyticsClient(
        endpoint=endpoint, credentials=credentials)

    try:
        documents = [
            {"id": "1", "language": "ja", "text": "猫は幸せ"},
            {"id": "2", "language": "de",
                "text": "Fahrt nach Stuttgart und dann zum Hotel zu Fu."},
            {"id": "3", "language": "en",
                "text": "My cat might need to see a veterinarian."},
            {"id": "4", "language": "es", "text": "A mi me encanta el fútbol!"}
        ]

        for document in documents:
            print(
                "Asking key-phrases on '{}' (id: {})".format(document['text'], document['id']))

        response = text_analytics.key_phrases(documents=documents)

        for document in response.documents:
            print("Document Id: ", document.id)
            print("\tKey Phrases:")
            for phrase in document.key_phrases:
                print("\t\t", phrase)

    except Exception as err:
        print("Encountered exception. {}".format(err))
key_phrases()
# </keyPhrases>

"""Sentiment.

Scores close to 1 indicate positive sentiment, while scores close to 0 indicate negative sentiment.
"""

# <sentimentAnalysis>
def sentiment():
    
    credentials = CognitiveServicesCredentials(subscription_key)
    text_analytics = TextAnalyticsClient(
        endpoint=endpoint, credentials=credentials)

    try:
        documents = [
            {"id": "1", "language": "en", "text": "I had the best day of my life."},
            {"id": "2", "language": "en",
                "text": "This was a waste of my time. The speaker put me to sleep."},
            {"id": "3", "language": "es", "text": "No tengo dinero ni nada que dar..."},
            {"id": "4", "language": "it",
                "text": "L'hotel veneziano era meraviglioso. È un bellissimo pezzo di architettura."}
        ]

        response = text_analytics.sentiment(documents=documents)
        for document in response.documents:
            print("Document Id: ", document.id, ", Sentiment Score: ",
                  "{:.2f}".format(document.score))

    except Exception as err:
        print("Encountered exception. {}".format(err))
sentiment()
# </sentimentAnalysis> 

"""EntityRecognition.
Extracts the entities from sentences and prints out their properties.
"""

# <entityRecognition>
def entity_recognition():
    
    credentials = CognitiveServicesCredentials(subscription_key)
    text_analytics = TextAnalyticsClient(
        endpoint=endpoint, credentials=credentials)

    try:
        documents = [
            {"id": "1", "language": "en", "text": "Microsoft was founded by Bill Gates and Paul Allen on April 4, 1975, to develop and sell BASIC interpreters for the Altair 8800."},
            {"id": "2", "language": "es",
                "text": "La sede principal de Microsoft se encuentra en la ciudad de Redmond, a 21 kilómetros de Seattle."}
        ]
        response = text_analytics.entities(documents=documents)

        for document in response.documents:
            print("Document Id: ", document.id)
            print("\tKey Entities:")
            for entity in document.entities:
                print("\t\t", "NAME: ", entity.name, "\tType: ",
                      entity.type, "\tSub-type: ", entity.sub_type)
                for match in entity.matches:
                    print("\t\t\tOffset: ", match.offset, "\tLength: ", match.length, "\tScore: ",
                          "{:.2f}".format(match.entity_type_score))

    except Exception as err:
        print("Encountered exception. {}".format(err))
entity_recognition()
# </entityExtraction>

if __name__ == "__main__":
    import sys
    import os.path

    sys.path.append(os.path.abspath(os.path.join(__file__, "..", "..")))
    from tools import execute_samples

    execute_samples(globals(), SUBSCRIPTION_KEY_ENV_NAME)
