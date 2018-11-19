from azure.cognitiveservices.search.customsearch import CustomSearchClient
from azure.cognitiveservices.search.imagesearch import ImageSearchAPI
from msrest.authentication import CognitiveServicesCredentials


def custom_image_search_result_lookup(subscription_key, custom_config):
    """CustomImageSearchResultLookup

    This will look up a single query (Xbox) and print out number of results, insights token, thumbnail url, content url for the first image result
    """
    client = ImageSearchAPI(credentials=CognitiveServicesCredentials(subscription_key))
    try:
        image_results = client.images.search(query="Xbox", custom_config=1)
        print("Searched for Query \" Xbox \"")

        # WebPages
        if (len(image_results) > 0):
            # find the first web page
            first_image_result = image_results[0]

            if (first_image_result):
                print("Image result count: {}".format(len(image_results)))
                print("First image insights token: {}".format(first_image_result.image_insights_token))
                print("First image thumbnail url: {}".format(first_image_result.thumbnail_url))
                print("First image content url: {}".format(first_image_result.content_url))
            else:
                print("Couldn't find image results!")
        else:
            print("Couldn't find image results!")
    except Exception as e:
        print("encountered exception. " + str(e))



if __name__ == "__main__":
    custom_image_search_result_lookup("65bcdb9d6e9e4b7faf271ef2e2dc0fa4", 1)