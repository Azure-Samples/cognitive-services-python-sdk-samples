# -*- coding: utf-8 -*-

import os

from azure.cognitiveservices.language.textanalytics import TextAnalyticsAPI
from msrest.authentication import CognitiveServicesCredentials

SUBSCRIPTION_KEY_ENV_NAME = "TEXTANALYTICS_SUBSCRIPTION_KEY"
TEXTANALYTICS_LOCATION = os.environ.get("TEXTANALYTICS_LOCATION", "westcentralus")

def language_extraction(subscription_key):
    """Language extraction.

    This will detect the language of a few strings.
    """
    client = TextAnalyticsAPI(TEXTANALYTICS_LOCATION, CognitiveServicesCredentials(subscription_key))

    try:
        documents = [{
            'id': 1,
            'text': 'This is a document written in English.'
        }, {
            'id': 2,
            'text': 'Este es un document escrito en Español.'
        }, {
            'id': 3,
            'text': '这是一个用中文写的文件'
        }]
        for document in documents:
            print("Asking language detection on '{}' (id: {})".format(document['text'], document['id']))
        response = client.detect_language(
            documents=documents
        )

        for document in response.documents:
            print("Found out that {} is {}".format(document.id, document.detected_languages[0].name))

    except Exception as err:
        print("Encountered exception. {}".format(err))

def key_phrases(subscription_key):
    """Key-phrases.

    The API returns a list of strings denoting the key talking points in the input text.
    """
    client = TextAnalyticsAPI(TEXTANALYTICS_LOCATION, CognitiveServicesCredentials(subscription_key))

    try:
        documents = [{
            'language': 'ja',
            'id': 1,
            'text': "猫は幸せ"
        }, {
            'language': 'de',
            'id': 2,
            'text': "Fahrt nach Stuttgart und dann zum Hotel zu Fu."
        }, {
            'language': 'en',
            'id': 3,
            'text': "My cat is stiff as a rock."
        }, {
            'language': 'es',
            'id': 4,
            'text': "A mi me encanta el fútbol!"
        }]

        for document in documents:
            print("Asking key-phrases on '{}' (id: {})".format(document['text'], document['id']))

        response = client.key_phrases(
            documents=documents
        )

        for document in response.documents:
            print("Found out that in document {}, key-phrases are:".format(document.id))
            for phrase in document.key_phrases:
                print("- {}".format(phrase))

    except Exception as err:
        print("Encountered exception. {}".format(err))


def sentiment(subscription_key):
    """Sentiment.

    Scores close to 1 indicate positive sentiment, while scores close to 0 indicate negative sentiment.
    """
    client = TextAnalyticsAPI(TEXTANALYTICS_LOCATION, CognitiveServicesCredentials(subscription_key))

    try:
        documents = [{
            'language': 'en',
            'id': 0,
            'text': "I had the best day of my life."
        }, {
            'language': 'en',
            'id': 1,
            'text': "This was a waste of my time. The speaker put me to sleep."
        }, {
            'language': 'es',
            'id': 2,
            'text': "No tengo dinero ni nada que dar..."
        }, {
            'language': 'it',
            'id': 3,
            'text': "L'hotel veneziano era meraviglioso. È un bellissimo pezzo di architettura."
        }]

        for document in documents:
            print("Asking sentiment on '{}' (id: {})".format(document['text'], document['id']))

        response = client.sentiment(
            documents=documents
        )

        for document in response.documents:
            print("Found out that in document {}, sentimet score is {}:".format(document.id, document.score))

    except Exception as err:
        print("Encountered exception. {}".format(err))


if __name__ == "__main__":
    # import sys, os.path
    # sys.path.append(os.path.abspath(os.path.join(__file__, "..", "..")))
    # from tools import execute_samples
    #execute_samples(globals(), SUBSCRIPTION_KEY_ENV_NAME)
    language_extraction("027b004824b34b009f533ab4274f2dbb")
