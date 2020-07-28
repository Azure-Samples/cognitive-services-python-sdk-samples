import os

from azure.cognitiveservices.search.newssearch import NewsSearchClient
from msrest.authentication import CognitiveServicesCredentials

# Add your Bing Search V7 subscription key to your environment variables.
SUBSCRIPTION_KEY = os.environ['BING_SEARCH_V7_SUBSCRIPTION_KEY']
# Note: your endpoint should not include the /bing/v7.0 suffix
ENDPOINT = os.environ['BING_SEARCH_V7_ENDPOINT']

def news_search(subscription_key):
    """NewsSearch.

    This will search news for (Quantum  Computing) with market and count parameters then verify number of results and print out totalEstimatedMatches, name, url, description, published time and name of provider of the first news result
    """
    client = NewsSearchClient(
        endpoint=ENDPOINT,
        credentials=CognitiveServicesCredentials(subscription_key)
    )

    try:
        news_result = client.news.search(
            query="Quantum Computing", market="en-us", count=10)
        print("Search news for query \"Quantum Computing\" with market and count")

        if news_result.value:
            first_news_result = news_result.value[0]
            print("Total estimated matches value: {}".format(
                news_result.total_estimated_matches))
            print("News result count: {}".format(len(news_result.value)))
            print("First news name: {}".format(first_news_result.name))
            print("First news url: {}".format(first_news_result.url))
            print("First news description: {}".format(
                first_news_result.description))
            print("First published time: {}".format(
                first_news_result.date_published))
            print("First news provider: {}".format(
                first_news_result.provider[0].name))
        else:
            print("Didn't see any news result data..")

    except Exception as err:
        print("Encountered exception. {}".format(err))


def news_search_with_filtering(subscription_key):
    """NewsSearchWithFilters.

    This will search most recent news for (Artificial Intelligence) with freshness and sortBy parameters then verify number of results and print out totalEstimatedMatches, name, url, description, published time and name of provider of the first news result.
    """
    client = NewsSearchClient(
        endpoint="https://api.cognitive.microsoft.com",
        credentials=CognitiveServicesCredentials(subscription_key)
    )

    try:
        news_result = client.news.search(
            query="Artificial Intelligence",
            market="en-us",
            freshness="Week",
            sort_by="Date"
        )
        print("Search most recent news for query \"Artificial Intelligence\" with freshness and sortBy")

        if news_result.value:
            first_news_result = news_result.value[0]
            print("News result count: {}".format(len(news_result.value)))
            print("First news name: {}".format(first_news_result.name))
            print("First news url: {}".format(first_news_result.url))
            print("First news description: {}".format(
                first_news_result.description))
            print("First published time: {}".format(
                first_news_result.date_published))
            print("First news provider: {}".format(
                first_news_result.provider[0].name))
        else:
            print("Didn't see any news result data..")

    except Exception as err:
        print("Encountered exception. {}".format(err))


def news_category(subscription_key):
    """NewsCategory.

    This will search category news for movie and TV entertainment with safe search then verify number of results and print out category, name, url, description, published time and name of provider of the first news result.
    """
    client = NewsSearchClient(
        endpoint="https://api.cognitive.microsoft.com",
        credentials=CognitiveServicesCredentials(subscription_key)
    )

    try:
        news_result = client.news.category(
            category="Entertainment_MovieAndTV",
            market="en-us",
            safe_search="strict"
        )
        print("Search category news for movie and TV entertainment with safe search")

        if news_result.value:
            first_news_result = news_result.value[0]
            print("News result count: {}".format(len(news_result.value)))
            print("First news category: {}".format(first_news_result.category))
            print("First news name: {}".format(first_news_result.name))
            print("First news url: {}".format(first_news_result.url))
            print("First news description: {}".format(
                first_news_result.description))
            print("First published time: {}".format(
                first_news_result.date_published))
            print("First news provider: {}".format(
                first_news_result.provider[0].name))
        else:
            print("Didn't see any news result data..")

    except Exception as err:
        print("Encountered exception. {}".format(err))


def news_trending(subscription_key):
    """NewsTrending.

    This will search news trending topics in Bing then verify number of results and print out name, text of query, webSearchUrl, newsSearchUrl and image Url of the first news result.
    """
    client = NewsSearchClient(
        endpoint="https://api.cognitive.microsoft.com",
        credentials=CognitiveServicesCredentials(subscription_key)
    )

    try:
        trending_topics = client.news.trending(market="en-us")
        print("Search news trending topics in Bing")

        if trending_topics.value:
            first_topic = trending_topics.value[0]
            print("News result count: {}".format(len(trending_topics.value)))
            print("First topic name: {}".format(first_topic.name))
            print("First topic query: {}".format(first_topic.query.text))
            print("First topic image url: {}".format(first_topic.image.url))
            print("First topic webSearchUrl: {}".format(
                first_topic.web_search_url))
            print("First topic newsSearchUrl: {}".format(
                first_topic.news_search_url))
        else:
            print("Didn't see any topics result data..")

    except Exception as err:
        print("Encountered exception. {}".format(err))


if __name__ == "__main__":
    import sys, os.path
    sys.path.append(os.path.abspath(os.path.join(__file__, "..", "..", "..")))    
    from samples.tools import execute_samples
    execute_samples(globals(), SUBSCRIPTION_KEY)
