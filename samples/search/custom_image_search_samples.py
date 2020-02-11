import os

from azure.cognitiveservices.search.customimagesearch import CustomImageSearchClient
from msrest.authentication import CognitiveServicesCredentials

# Add your Bing Custom Search subscription key to your environment variables.
SUBSCRIPTION_KEY = os.environ['BING_CUSTOM_SEARCH_SUBSCRIPTION_KEY']
ENDPOINT = os.environ['BING_CUSTOM_SEARCH_ENDPOINT']

def custom_image_search_result_lookup(subscription_key):
    """CustomImageSearchResultLookup.

    This will look up a single query (Xbox) and print out number of results, insights token, thumbnail url, content url for the first image result
    """

    client = CustomImageSearchClient(
        endpoint=ENDPOINT,
        credentials=CognitiveServicesCredentials(subscription_key))
    try:
        image_results = client.custom_instance.image_search(
            query="Xbox", custom_config=1)
        print("Searched for Query \" Xbox \"")

        # WebPages
        if image_results.value:
            # find the first web page
            first_image_result = image_results.value[0]

            if first_image_result:
                print("Image result count: {}".format(len(image_results.value)))
                print("First image insights token: {}".format(
                    first_image_result.image_insights_token))
                print("First image thumbnail url: {}".format(
                    first_image_result.thumbnail_url))
                print("First image content url: {}".format(
                    first_image_result.content_url))
            else:
                print("Couldn't find image results!")
        else:
            print("Couldn't find image results!")
    except Exception as e:
        print("encountered exception. " + str(e))


if __name__ == "__main__":
    import sys
    import os.path
    sys.path.append(os.path.abspath(os.path.join(__file__, "..", "..")))
    from tools import execute_samples
    execute_samples(globals(), SUBSCRIPTION_KEY)
