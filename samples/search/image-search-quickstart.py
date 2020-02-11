import os

from azure.cognitiveservices.search.imagesearch import ImageSearchClient
from msrest.authentication import CognitiveServicesCredentials

# Add your Bing Search V7 subscription key and endpoint to your environment variables.
SUBSCRIPTION_KEY = os.environ['BING_SEARCH_V7_SUBSCRIPTION_KEY']
ENDPOINT = os.environ['BING_ENTITY_SEARCH_ENDPOINT']

search_term = "canadian rockies"

"""
This application will search images on the web with the Bing Image Search API and print out first image result.
"""
# create the image search client
client = ImageSearchClient(ENDPOINT, CognitiveServicesCredentials(SUBSCRIPTION_KEY))
# send a search query to the Bing Image Search API
image_results = client.images.search(query=search_term)
print("Searching the web for images of: {}".format(search_term))

# Image results
if image_results.value:
    first_image_result = image_results.value[0]
    print("Total number of images returned: {}".format(len(image_results.value)))
    print("First image thumbnail url: {}".format(
        first_image_result.thumbnail_url))
    print("First image content url: {}".format(first_image_result.content_url))
else:
    print("Couldn't find image results!")
