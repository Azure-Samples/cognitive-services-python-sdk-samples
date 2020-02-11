import os

from azure.cognitiveservices.search.customsearch import CustomSearchClient
from msrest.authentication import CognitiveServicesCredentials

SUBSCRIPTION_KEY = os.environ['BING_CUSTOM_SEARCH_SUBSCRIPTION_KEY']
ENDPOINT = os.environ['BING_CUSTOM_SEARCH_ENDPOINT']

def custom_search_web_page_result_lookup(subscription_key):
    """CustomSearch.

    This will look up a single query (Xbox) and print out name and url for first web result.
    """

    client = CustomSearchClient(
        endpoint=ENDPOINT,
        credentials=CognitiveServicesCredentials(subscription_key))

    try:
        web_data = client.custom_instance.search(query="xbox", custom_config=1)
        print("Searched for Query 'xbox'")

        if web_data.web_pages.value:
            first_web_result = web_data.web_pages.value[0]
            print("Web Pages result count: {}".format(
                len(web_data.web_pages.value)))
            print("First Web Page name: {}".format(first_web_result.name))
            print("First Web Page url: {}".format(first_web_result.url))
        else:
            print("Didn't see any web data..")

    except Exception as err:
        print("Encountered exception. {}".format(err))


if __name__ == "__main__":
    import sys, os.path
    sys.path.append(os.path.abspath(os.path.join(__file__, "..", "..", "..")))    
    from samples.tools import execute_samples
    execute_samples(globals(), SUBSCRIPTION_KEY)
