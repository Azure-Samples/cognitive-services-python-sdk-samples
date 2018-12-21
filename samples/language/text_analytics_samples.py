# -*- coding: utf-8 -*-

import os

from azure.cognitiveservices.language.textanalytics import TextAnalyticsClient
from msrest.authentication import CognitiveServicesCredentials

SUBSCRIPTION_KEY_ENV_NAME = "TEXTANALYTICS_SUBSCRIPTION_KEY"
TEXTANALYTICS_LOCATION = os.environ.get("TEXTANALYTICS_LOCATION", "westcentralus")


def language_extraction(subscription_key):
    """Language extraction.

    This will detect the language of a few strings.
    """
    endpoint = "https://{}.api.cognitive.microsoft.com".format(TEXTANALYTICS_LOCATION)
    client = TextAnalyticsClient(endpoint=endpoint, credentials=CognitiveServicesCredentials(subscription_key))

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
    endpoint = "https://{}.api.cognitive.microsoft.com".format(TEXTANALYTICS_LOCATION)
    client = TextAnalyticsClient(endpoint=endpoint, credentials=CognitiveServicesCredentials(subscription_key))

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
    endpoint = "https://{}.api.cognitive.microsoft.com".format(TEXTANALYTICS_LOCATION)
    client = TextAnalyticsClient(endpoint=endpoint, credentials=CognitiveServicesCredentials(subscription_key))

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


def entity_extraction(subscription_key):
    """EntityExtraction.

    Extracts the entities from sentences and prints out their properties
    """
    endpoint = "https://{}.api.cognitive.microsoft.com".format(TEXTANALYTICS_LOCATION)
    client = TextAnalyticsClient(endpoint=endpoint, credentials=CognitiveServicesCredentials(subscription_key))

    try:
        documents = [{
            'language': 'en',
            'id': 0,
            'text': "Microsoft released win10. Microsoft also released Hololens"
        }, {
            'language': 'en',
            'id': 1,
            'text': "Microsoft is an IT company."
        }, {
            'language': 'es',
            'id': 2,
            'text': "Microsoft lanzó win10. Microsoft también lanzó Hololens"
        }, {
            'language': 'es',
            'id': 3,
            'text': "Microsoft es una empresa de TI."
        }]
        for document in documents:
            print("Extracting entities from '{}' (id: {})".format(document['text'], document['id']))

        response = client.entities(
            documents=documents
        )

        for document in response.documents:
            print("Document ID: {}".format(document['Id']))
            print("\t Entities:")
            for entity in document['Entities']:
                print("\t\tEntity Name: {}".format(entity.name))
                print("\t\tWikipedia Language: {}".format(entity.wikipedia_language))
                print("\t\tWikipedia Url: {}".format(entity.wikipedia_url))
                print("\t\tNumber of times appeared on the text: {}".format(len(entity.matches)))
                print("\t\tEntity Type: {}".format(entity.type))
                print("\t\tEntity SubType: {}".format(entity.sub_type))
                print("\n")

    except Exception as err:
        print("Encountered exception. {}".format(err))


if __name__ == "__main__":
    import sys, os.path

    sys.path.append(os.path.abspath(os.path.join(__file__, "..", "..")))
    from tools import execute_samples

    execute_samples(globals(), SUBSCRIPTION_KEY_ENV_NAME)
