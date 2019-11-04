# <imports>
import os
from azure.cognitiveservices.search.customsearch import CustomSearchClient
from msrest.authentication import CognitiveServicesCredentials
# </imports>

# <vars>
SUBSCRIPTION_KEY = os.environ['BING_CUSTOM_SEARCH_SUBSCRIPTION_KEY']
search_term = "xbox" 
custom_config = "your-custom-config-id" # You can also use "1"
# </vars>

# <authentication>
client = CustomSearchClient(CognitiveServicesCredentials(SUBSCRIPTION_KEY))
# </authentication>

"""CustomSearch.
This will look up a single query and print out name and url for first web result.
"""
# <request>
def custom_search_web_page_result_lookup():
    try:
        web_data = client.custom_instance.search(query=search_term, custom_config=1)
        print("Searched for Query: " + search_term)

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
# <request>

if __name__ == "__main__":
    import sys
    import os.path
    sys.path.append(os.path.abspath(os.path.join(__file__, "..", "..")))
    from tools import execute_samples
    execute_samples(globals(), SUBSCRIPTION_KEY)
