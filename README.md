# Cognitive Services Python SDK Samples

These samples will show you how to get up and running using the Python SDKs for various Cognitive Services services. They'll cover a few rudimentary use cases and hopefully express best practices for interacting with the data from these APIs.

## Features

This project framework provides examples for the following services:

### Language

* Using the **Bing Spell Check SDK** [azure-cognititiveservices-language-spellcheck](http://pypi.python.org/pypi/azure-cognititiveservices-language-spellcheck) for the [Bing Spell Check API](https://azure.microsoft.com/services/cognitive-services/spell-check/)
* Using the **Text Analytics SDK** [azure-cognititiveservices-language-textanalytics](http://pypi.python.org/pypi/azure-cognititiveservices-language-textanalytics) for the [Tet Analytics API](https://azure.microsoft.com/services/cognitive-services/text-analytics/)

### Search

* Using the **Bing Custom Search SDK** [azure-cognititiveservices-search-customsearch](http://pypi.python.org/pypi/azure-cognititiveservices-search-customsearch) for the [Custom Search API](https://azure.microsoft.com/services/cognitive-services/bing-custom-search//)
* Using the **Bing Entity Search SDK** [azure-cognititiveservices-search-entitysearch](http://pypi.python.org/pypi/azure-cognititiveservices-search-entitysearch) for the [Entity Search API](https://azure.microsoft.com/services/cognitive-services/bing-entity-search-api/)
* Using the **Bing Image Search SDK** [azure-cognititiveservices-search-imagesearch](http://pypi.python.org/pypi/azure-cognititiveservices-search-imagesearch) for the [Image Search API](https://azure.microsoft.com/services/cognitive-services/bing-image-search-api/)
* Using the **Bing News Search SDK** [azure-cognititiveservices-search-newssearch](http://pypi.python.org/pypi/azure-cognititiveservices-search-newssearch) for the [News Search API](https://azure.microsoft.com/services/cognitive-services/bing-news-search-api/)
* Using the **Bing Video Search SDK** [azure-cognititiveservices-search-videosearch](http://pypi.python.org/pypi/azure-cognititiveservices-search-videosearch) for the [Video Search API](https://azure.microsoft.com/services/cognitive-services/bing-video-search-api/)
* Using the **Bing Web Search SDK** [azure-cognititiveservices-search-websearch](http://pypi.python.org/pypi/azure-cognititiveservices-search-websearch) for the [Web Search API](https://azure.microsoft.com/services/cognitive-services/bing-web-search-api/)

We provide several meta-packages to help you install several packages at a time. Please note that meta-packages are only recommended for development purpose. It's recommended in production to always pin specific version of individual packages.

## Getting Started

### Prerequisites

1.  A cognitive services API key with which to authenticate the SDK's calls. [Sign up here](https://azure.microsoft.com/services/cognitive-services/directory/) by navigating to the **Language** or **Search** services and acquiring an API key. You can get a trial key for **free** which will expire after 30 days or create a Cognitive Services account on the Azure portal through the *Use with an Azure subscription* button.

> Subscription keys are usually per service. For example, the subscription key for Spell Check will not be the same than Custom Search. Read the previous *sign up* link or the Azure portal for details on subscription keys.

### Installation

1.  If you don't already have it, [install Python](https://www.python.org/downloads/).

    This sample (and the SDK) is compatible with Python 2.7, 3.3, 3.4, 3.5 and 3.6.

2.  General recommendation for Python development is to use a Virtual Environment. 
    For more information, see https://docs.python.org/3/tutorial/venv.html
    
    Install and initialize the virtual environment with the "venv" module on Python 3 (you must install [virtualenv](https://pypi.python.org/pypi/virtualenv) for Python 2.7):

    ```
    python -m venv mytestenv # Might be "python3" or "py -3.6" depending on your Python installation
    cd mytestenv
    source bin/activate      # Linux shell (Bash, ZSH, etc.) only
    ./scripts/activate       # PowerShell only
    ./scripts/activate.bat   # Windows CMD only
    ```

### Quickstart

1.  Clone the repository.

    ```
    git clone https://github.com/Azure-Samples/cognitive-services-python-sdk-samples.git
    ```

2.  Install the dependencies using pip.

    ```
    cd cognitive-services-python-sdk-samples
    pip install -r requirements.txt
    ```

4.  Set up the environment variable `SPELLCHECK_SUBSCRIPTION_KEY` with your key if you want to execute SpellCheck tests.
4.  Set up the environment variable `TEXTANALYTICS_SUBSCRIPTION_KEY` with your key if you want to execute SpellCheck tests. You might override too `TEXTANALYTICS_LOCATION` (westcentralus by default).
3.  Set up the environment variable `CUSTOMSEARCH_SUBSCRIPTION_KEY` with your key if you want to execute CustomSearch tests.
3.  Set up the environment variable `ENTITYSEARCH_SUBSCRIPTION_KEY` with your key if you want to execute EntitySearch tests.
4.  Set up the environment variable `IMAGESEARCH_SUBSCRIPTION_KEY` with your key if you want to execute ImageSearch tests.
4.  Set up the environment variable `NEWSSEARCH_SUBSCRIPTION_KEY` with your key if you want to execute NewsSearch tests.
4.  Set up the environment variable `VIDEOSEARCH_SUBSCRIPTION_KEY` with your key if you want to execute VideoSearch tests.
4.  Set up the environment variable `WEBSEARCH_SUBSCRIPTION_KEY` with your key if you want to execute WebSearch tests.

## Demo

A demo app is included to show how to use the project.

To run the complete demo, execute `python example.py`

To run each individual demo, point directly to the file. For example (i.e. not complete list):

2. `python samples/language/spellcheck_samples.py`
1. `python samples/search/entity_search_samples.py`
2. `python samples/search/video_search_samples.py`

To see the code of each example, simply look at the examples in the Samples folder. They are written to be isolated in scope so that you can see only what you're interested in.

## Resources

- https://docs.microsoft.com/python/api/overview/azure/cognitive-services
- https://github.com/Azure/azure-sdk-for-python
