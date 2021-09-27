---
page_type: sample
languages:
- python
products:
- azure
description: "These samples will show you how to get up and running using the Python SDKs for various Cognitive Services services."
urlFragment: cognitive-services-python-sdk-samples
---

# Cognitive Services Python SDK Samples

These samples will show you how to get up and running using the Python SDKs for various Cognitive Services services. They'll cover a few rudimentary use cases and hopefully express best practices for interacting with the data from these APIs.

## Features

This project framework provides examples for the following services:

| Area | Service | SDK |
|------|---------|-----|
| Knowledge | [QnA API](https://azure.microsoft.com/en-us/services/cognitive-services/qna-maker/) | [azure-cognitiveservices-knowledge-qnamaker](http://pypi.python.org/pypi/azure-cognitiveservices-knowledge-qnamaker) |
| Language | [LUIS API](https://azure.microsoft.com/services/cognitive-services/language-understanding-intelligent-service/) | [azure-cognitiveservices-language-luis](http://pypi.python.org/pypi/azure-cognitiveservices-language-luis) |
| Language | [Bing Spell Check API](https://azure.microsoft.com/services/cognitive-services/spell-check/) | [azure-cognitiveservices-language-spellcheck](http://pypi.python.org/pypi/azure-cognitiveservices-language-spellcheck) |
| Language | [Text Analytics API](https://azure.microsoft.com/services/cognitive-services/text-analytics/) | [azure-cognitiveservices-language-textanalytics](http://pypi.python.org/pypi/azure-cognitiveservices-language-textanalytics) |
| Search | [Bing Autosuggest API](https://azure.microsoft.com/services/cognitive-services/autosuggest/) | [azure-cognitiveservices-search-autosuggest](http://pypi.python.org/pypi/azure-cognitiveservices-search-autosuggest) |
| Search | [Bing Custom Search API](https://azure.microsoft.com/services/cognitive-services/bing-custom-search/) | [azure-cognitiveservices-search-customsearch](http://pypi.python.org/pypi/azure-cognitiveservices-search-customsearch) |
| Search | [Bing Custom Image Search API](https://azure.microsoft.com/services/cognitive-services/bing-custom-search/) | [azure-cognitiveservices-search-customimagesearch](http://pypi.python.org/pypi/azure-cognitiveservices-search-customimagesearch) |
| Search | [Bing Entity Search API](https://azure.microsoft.com/services/cognitive-services/bing-entity-search-api/) | [azure-cognitiveservices-search-entitysearch](http://pypi.python.org/pypi/azure-cognitiveservices-search-entitysearch) |
| Search | [Bing Image Search API](https://azure.microsoft.com/services/cognitive-services/bing-image-search-api/) | [azure-cognitiveservices-search-imagesearch](http://pypi.python.org/pypi/azure-cognitiveservices-search-imagesearch) |
| Search | [Bing News Search API](https://azure.microsoft.com/services/cognitive-services/bing-news-search-api/) | [azure-cognitiveservices-search-newssearch](http://pypi.python.org/pypi/azure-cognitiveservices-search-newssearch) |
| Search | [Bing Video Search API](https://azure.microsoft.com/services/cognitive-services/bing-video-search-api/) | [azure-cognitiveservices-search-videosearch](http://pypi.python.org/pypi/azure-cognitiveservices-search-videosearch) |
| Search | [Bing Visual Search API](https://azure.microsoft.com/services/cognitive-services/bing-visual-search-api/) | [azure-cognitiveservices-search-visualsearch](http://pypi.python.org/pypi/azure-cognitiveservices-search-visualsearch) |
| Search | [Bing Web Search API](https://azure.microsoft.com/services/cognitive-services/bing-web-search-api/) | [azure-cognitiveservices-search-websearch](http://pypi.python.org/pypi/azure-cognitiveservices-search-websearch) |
| Vision | [Face API](https://azure.microsoft.com/services/cognitive-services/face/) | [azure-cognitiveservices-vision-face](http://pypi.python.org/pypi/azure-cognitiveservices-vision-face) |
| Vision | [Computer Vision API](https://azure.microsoft.com/services/cognitive-services/computer-vision/) |  [azure-cognitiveservices-vision-computervision](http://pypi.python.org/pypi/azure-cognitiveservices-vision-computervision) |
| Vision | [Content Moderator API](https://azure.microsoft.com/services/cognitive-services/content-moderator/) | [azure-cognitiveservices-vision-contentmoderator](http://pypi.python.org/pypi/azure-cognitiveservices-vision-contentmoderator) |
| Vision | [Custom Vision API](https://azure.microsoft.com/services/cognitive-services/custom-vision-service/) | [azure-cognitiveservices-vision-customvision](http://pypi.python.org/pypi/azure-cognitiveservices-vision-customvision) |
| Vision | [Ink Recognizer API](https://azure.microsoft.com/services/cognitive-services/ink-recognizer/) | [azure-cognitiveservices-inkrecognizer](https://pypi.org/project/azure-cognitiveservices-inkrecognizer/) |

We provide several meta-packages to help you install several packages at a time. Please note that meta-packages are only recommended for development purpose. It's recommended in production to always pin specific version of individual packages.

## Getting Started

### Prerequisites

1. A cognitive services API key with which to authenticate the SDK's calls. [Create a new Azure account, and try Cognitive Services for free.](https://azure.microsoft.com/free/cognitive-services/)

> Subscription keys are usually per service. For example, the subscription key for Spell Check will not be the same than Custom Search. Read the previous *sign up* link or the Azure portal for details on subscription keys.

### Installation

1. If you don't already have it, [install Python](https://www.python.org/downloads/).

    This sample (and the SDK) is compatible with Python 2.7, 3.3, 3.4, 3.5 and 3.6.

2. General recommendation for Python development is to use a Virtual Environment.
    For more information, see <https://docs.python.org/3/tutorial/venv.html>

    Install and initialize the virtual environment with the "venv" module on Python 3 (you must install [virtualenv](https://pypi.python.org/pypi/virtualenv) for Python 2.7):

    ```bash
    python -m venv mytestenv # Might be "python3" or "py -3.6" depending on your Python installation
    cd mytestenv
    source bin/activate      # Linux shell (Bash, ZSH, etc.) only
    ./scripts/activate       # PowerShell only
    ./scripts/activate.bat   # Windows CMD only
    ```

### Quickstart

1. Clone the repository.

    ```bash
    git clone https://github.com/Azure-Samples/cognitive-services-python-sdk-samples.git
    ```

2. Install the dependencies using pip.

    ```bash
    cd cognitive-services-python-sdk-samples
    pip install -r requirements.txt
    ```

3. Set up the environment variables with corresponding keys to execute samples of interest

| Environment variable | Service | Notes |
|----------------------|---------|-------|
| `LUIS_SUBSCRIPTION_KEY` |  LUIS | |
| `SPELLCHECK_SUBSCRIPTION_KEY` |  SpellCheck | |
| `TEXTANALYTICS_SUBSCRIPTION_KEY` |  TextAnalytics | You might override too `TEXTANALYTICS_LOCATION` (westcentralus by default). |
| `AUTOSUGGEST_SUBSCRIPTION_KEY` |  Autosuggest | |
| `CUSTOMSEARCH_SUBSCRIPTION_KEY` |  CustomSearch | |
| `CUSTOMIMAGESEARCH_SUBSCRIPTION_KEY` |  CustomImageSearch | |
| `ENTITYSEARCH_SUBSCRIPTION_KEY` |  EntitySearch | |
| `IMAGESEARCH_SUBSCRIPTION_KEY` |  ImageSearch | |
| `NEWSSEARCH_SUBSCRIPTION_KEY` |  NewsSearch | |
| `VIDEOSEARCH_SUBSCRIPTION_KEY` |  VideoSearch | |
| `VISUALSEARCH_SUBSCRIPTION_KEY` |  VideoSearch | |
| `WEBSEARCH_SUBSCRIPTION_KEY` |  WebSearch | |
| `COMPUTERVISION_SUBSCRIPTION_KEY` |  Computer Vision | You might override too `COMPUTERVISION_LOCATION` (westcentralus by default). |
| `CONTENTMODERATOR_SUBSCRIPTION_KEY` |  Content Moderator | You might override too `CONTENTMODERATOR_LOCATION` (westcentralus by default). |
| `CUSTOMVISION_TRAINING_KEY`,  `CUSTOMVISION_TRAINING_ID` |  CustomVision Training | |
| `CUSTOMVISION_PREDICTION_KEY`,  `CUSTOMVISION_PREDICTION_ID` |  CustomVision Prediction | |

## Demo

A demo app is included to show how to use the project.

To run the complete demo, execute `python example.py`

To run each individual demo, point directly to the file. For example (i.e. not complete list):

1. `python samples/language/spellcheck_samples.py`
2. `python samples/search/entity_search_samples.py`
3. `python samples/search/video_search_samples.py`
4. `python samples/vision/inkrecognizer_sample.py`

To see the code of each example, simply look at the examples in the Samples folder. They are written to be isolated in scope so that you can see only what you're interested in.

## Resources

- <https://docs.microsoft.com/python/api/overview/azure/cognitive-services>
- <https://github.com/Azure/azure-sdk-for-python>
