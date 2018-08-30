from azure.cognitiveservices.search.imagesearch import ImageSearchAPI
from azure.cognitiveservices.search.imagesearch.models import ImageType, ImageAspect, ImageInsightModule
from msrest.authentication import CognitiveServicesCredentials

subscription_key = "Enter your key here"
search_term = "canadian rockies"

"""
This application will search images on the web and print out first image result
"""
client = ImageSearchAPI(CognitiveServicesCredentials(subscription_key))

try:
    image_results = client.images.search(query="canadian rockies")
    print("Searching the web for images of \"canadian rockies\"")

    # Image results
    if image_results.value:
        first_image_result = image_results.value[0]
        print("Total number of images returned: {}".format(len(image_results.value)))
        print("First image thumbnail url: {}".format(first_image_result.thumbnail_url))
        print("First image content url: {}".format(first_image_result.content_url))
    else:
        print("Couldn't find image results!")

except Exception as err:
    print("Encountered exception. {}".format(err))
