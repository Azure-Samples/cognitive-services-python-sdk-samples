# Bing Search Python SDK Samples

These samples will show you how to get up and running using the Python SDKs for various Bing Search services. They'll cover a few rudimentary use cases and hopefully express best practices for interacting with the data from these APIs.

## Features

This project framework provides examples for the following services:

* Using the **Bing Entity Search SDK** [azure-cognititiveservices-search-entitysearch](http://pypi.python.org/pypi/azure-cognititiveservices-search-entitysearch) for the [Entity Search API](https://azure.microsoft.com/en-us/services/cognitive-services/bing-entity-search-api/)
* Using the **Bing Web Search SDK** [azure-cognititiveservices-search-websearch](http://pypi.python.org/pypi/azure-cognititiveservices-search-websearch) for the [Web Search API](https://azure.microsoft.com/en-us/services/cognitive-services/bing-web-search-api/)
* Using the **Bing Video Search SDK** [azure-cognititiveservices-search-videosearch](http://pypi.python.org/pypi/azure-cognititiveservices-search-videosearch) for the [Video Search API](https://azure.microsoft.com/en-us/services/cognitive-services/bing-video-search-api/)

We provide several meta-packages to help you install several packages at a time. Please note that meta-packages are only recommended for development purpose. It's recommended in production to always pin specific version of individual packages.

## Getting Started

### Prerequisites

1.  A cognitive services API key with which to authenticate the SDK's calls. [Sign up here](https://azure.microsoft.com/en-us/services/cognitive-services/directory/) by navigating to the **Search** services and acquiring an API key. You can get a trial key for **free** which will expire after 30 days. To execute both samples, you need an EntitySearch key and a Bing WebSearch key.

### Installation

1.  If you don't already have it, [install Python](https://www.python.org/downloads/).

    This sample (and the SDK) is compatible with Python 2.7, 3.3, 3.4, 3.5 and 3.6.

2.  We recommend that you use a [virtual environment](https://docs.python.org/3/tutorial/venv.html)
    to run this example, but it's not required.
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
    git clone https://github.com/Azure-Samples/bing-search-python.git
    ```

2.  Install the dependencies using pip.

    ```
    cd bing-search-python
    pip install -r requirements.txt
    ```

3.  Set up the environment variable `ENTITYSEARCH_SUBSCRIPTION_KEY` with your CS key if you want to execute EntitySearch tests.
4.  Set up the environment variable `WEBSEARCH_SUBSCRIPTION_KEY` with your CS key if you want to execute WebSearch tests.
4.  Set up the environment variable `VIDEOSEARCH_SUBSCRIPTION_KEY` with your CS key if you want to execute VideoSearch tests.

## Demo

A demo app is included to show how to use the project.

To run the complete demo, execute `python example.py`

To run each individual demo, point directly to the file:

1. `python samples/entity_search_samples.py`
2. `python samples/web_search_samples.py`
2. `python samples/video_search_samples.py`

To see the code of each example, simply look at the examples in the Samples folder. They are written to be isolated in scope so that you can see only what you're interested in.

## Resources

- https://docs.microsoft.com/python/api/overview/azure/cognitive-services
- https://github.com/Azure/azure-sdk-for-python
