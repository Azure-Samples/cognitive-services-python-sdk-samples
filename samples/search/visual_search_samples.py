import json
import os.path

from azure.cognitiveservices.search.visualsearch import VisualSearchClient
from azure.cognitiveservices.search.visualsearch.models import (
    VisualSearchRequest,
    CropArea,
    ImageInfo,
    Filters,
    KnowledgeRequest,
)
from msrest.authentication import CognitiveServicesCredentials

# Add your Bing Search V7 subscription key to your environment variables.
SUBSCRIPTION_KEY = os.environ['BING_SEARCH_V7_SUBSCRIPTION_KEY']

CWD = os.path.dirname(__file__)
TEST_IMAGES = os.path.join(CWD, "TestImages")


def search_image_binary(subscription_key):
    """VisualSearchImageBinary.

    This will send an image binary in the body of the post request and print out the imageInsightsToken, the number of tags, the number of actions, and the first actionType.
    """

    client = VisualSearchClient(endpoint="https://api.cognitive.microsoft.com",
                                credentials=CognitiveServicesCredentials(subscription_key))

    image_path = os.path.join(TEST_IMAGES, "image.jpg")
    with open(image_path, "rb") as image_fd:

        # You need to pass the serialized form of the model
        knowledge_request = json.dumps(VisualSearchRequest().serialize())

        print("Search visual search request with binary of dog image")
        result = client.images.visual_search(
            image=image_fd, knowledge_request=knowledge_request)

        if not result:
            print("No visual search result data.")
            return

        # Visual Search results
        if result.image.image_insights_token:
            print("Uploaded image insights token: {}".format(
                result.image.image_insights_token))
        else:
            print("Couldn't find image insights token!")

        # List of tags
        if result.tags:
            first_tag = result.tags[0]
            print("Visual search tag count: {}".format(len(result.tags)))

            # List of actions in first tag
            if first_tag.actions:
                first_tag_action = first_tag.actions[0]
                print("First tag action count: {}".format(
                    len(first_tag.actions)))
                print("First tag action type: {}".format(
                    first_tag_action.action_type))
            else:
                print("Couldn't find tag actions!")
        else:
            print("Couldn't find image tags!")


def search_image_binary_with_crop_area(subscription_key):
    """VisualSearchImageBinaryWithCropArea.

    This will send an image binary in the body of the post request, along with a cropArea object, and print out the imageInsightsToken, the number of tags, the number of actions, and the first actionType.
    """

    client = VisualSearchClient(endpoint="https://api.cognitive.microsoft.com",
                                credentials=CognitiveServicesCredentials(subscription_key))

    image_path = os.path.join(TEST_IMAGES, "image.jpg")
    with open(image_path, "rb") as image_fd:
        crop_area = CropArea(top=0.1, bottom=0.5, left=0.1, right=0.9)
        knowledge_request = VisualSearchRequest(
            image_info=ImageInfo(crop_area=crop_area))

        # You need to pass the serialized form of the model
        knowledge_request = json.dumps(knowledge_request.serialize())

        print("Search visual search request with binary of dog image")
        result = client.images.visual_search(
            image=image_fd, knowledge_request=knowledge_request)

        if not result:
            print("No visual search result data.")
            return

        # Visual Search results
        if result.image.image_insights_token:
            print("Uploaded image insights token: {}".format(
                result.image.image_insights_token))
        else:
            print("Couldn't find image insights token!")

        # List of tags
        if result.tags:
            first_tag = result.tags[0]
            print("Visual search tag count: {}".format(len(result.tags)))

            # List of actions in first tag
            if first_tag.actions:
                first_tag_action = first_tag.actions[0]
                print("First tag action count: {}".format(
                    len(first_tag.actions)))
                print("First tag action type: {}".format(
                    first_tag_action.action_type))
            else:
                print("Couldn't find tag actions!")
        else:
            print("Couldn't find image tags!")


def search_url_with_filters(subscription_key):
    """VisualSearchUrlWithFilters.

    This will send an image url in the knowledgeRequest parameter, along with a \"site:www.bing.com\" filter, and print out the imageInsightsToken, the number of tags, the number of actions, and the first actionType.
    """

    client = VisualSearchClient(endpoint="https://api.cognitive.microsoft.com",
                                credentials=CognitiveServicesCredentials(subscription_key))

    image_url = "https://images.unsplash.com/photo-1512546148165-e50d714a565a?w=600&q=80"
    filters = Filters(site="www.bing.com")

    knowledge_request = VisualSearchRequest(
        image_info=ImageInfo(url=image_url),
        knowledge_request=KnowledgeRequest(filters=filters)
    )

    # You need to pass the serialized form of the model
    knowledge_request = json.dumps(knowledge_request.serialize())

    print("Search visual search request with url of dog image")
    result = client.images.visual_search(knowledge_request=knowledge_request)

    if not result:
        print("No visual search result data.")
        return

    # Visual Search results
    if result.image.image_insights_token:
        print("Uploaded image insights token: {}".format(
            result.image.image_insights_token))
    else:
        print("Couldn't find image insights token!")

    # List of tags
    if result.tags:
        first_tag = result.tags[0]
        print("Visual search tag count: {}".format(len(result.tags)))

        # List of actions in first tag
        if first_tag.actions:
            first_tag_action = first_tag.actions[0]
            print("First tag action count: {}".format(len(first_tag.actions)))
            print("First tag action type: {}".format(
                first_tag_action.action_type))
        else:
            print("Couldn't find tag actions!")
    else:
        print("Couldn't find image tags!")


def search_insights_token_with_crop_area(subscription_key):
    """VisualSearchInsightsTokenWithCropArea.

    This will send an image insights token in the knowledgeRequest parameter, along with a cropArea object, and print out the imageInsightsToken, the number of tags, the number of actions, and the first actionType.
    """

    client = VisualSearchClient(endpoint="https://api.cognitive.microsoft.com",
                                credentials=CognitiveServicesCredentials(subscription_key))

    image_insights_token = "bcid_113F29C079F18F385732D8046EC80145*ccid_oV/QcH95*mid_687689FAFA449B35BC11A1AE6CEAB6F9A9B53708*thid_R.113F29C079F18F385732D8046EC80145"
    crop_area = CropArea(top=0.1, bottom=0.5, left=0.1, right=0.9)

    knowledge_request = VisualSearchRequest(
        image_info=ImageInfo(
            image_insights_token=image_insights_token,
            crop_area=crop_area
        ),
    )

    # You need to pass the serialized form of the model
    knowledge_request = json.dumps(knowledge_request.serialize())

    print("Search visual search request with url of dog image")
    result = client.images.visual_search(knowledge_request=knowledge_request)

    if not result:
        print("No visual search result data.")
        return

    # Visual Search results
    if result.image.image_insights_token:
        print("Uploaded image insights token: {}".format(
            result.image.image_insights_token))
    else:
        print("Couldn't find image insights token!")

    # List of tags
    if result.tags:
        first_tag = result.tags[0]
        print("Visual search tag count: {}".format(len(result.tags)))

        # List of actions in first tag
        if first_tag.actions:
            first_tag_action = first_tag.actions[0]
            print("First tag action count: {}".format(len(first_tag.actions)))
            print("First tag action type: {}".format(
                first_tag_action.action_type))
        else:
            print("Couldn't find tag actions!")
    else:
        print("Couldn't find image tags!")


def search_url_with_json(subscription_key):
    """VisualSearchURLWithJSON.

    This will send a visual search request in JSON form, and print out the imageInsightsToken, the number of tags, and the first actionCount and actionType.
    """

    client = VisualSearchClient(endpoint="https://api.cognitive.microsoft.com",
                                credentials=CognitiveServicesCredentials(subscription_key))
    try:
        """
         The visual search request can be passed in as a JSON string
         The image is specified via URL in the ImageInfo object, along with a crop area as shown below:
         {
           "imageInfo": {
             "url": "https://images.unsplash.com/photo-1512546148165-e50d714a565a?w=600&q=80",
             "cropArea": {
               "top": 0.1,
               "bottom": 0.5,
               "left": 0.1,
               "right": 0.9
             }
           },
           "knowledgeRequest": {
             "filters": {
               "site": "www.bing.com"
             }
           }
         } 
        """
        visual_search_request_json = "{\"imageInfo\":{\"url\":\"https://images.unsplash.com/photo-1512546148165-e50d714a565a?w=600&q=80\",\"cropArea\":{\"top\":0.1,\"bottom\":0.5,\"left\":0.1,\"right\":0.9}},\"knowledgeRequest\":{\"filters\":{\"site\":\"www.bing.com\"}}}"

        # An image binary is not necessary here, as the image is specified via URL
        visual_search_results = client.images.visual_search(
            knowledge_request=visual_search_request_json)
        print("Search visual search request with url of dog image")

        if not visual_search_results:
            print("No visual search result data.")
        else:
            # Visual Search results
            if visual_search_results.image.image_insights_token:
                print("Uploaded image insights token: {}".format(
                    visual_search_results.image.image_insights_token))
            else:
                print("Couldn't find image insights token!")

            # List of tags
            if visual_search_results.tags:
                first_tag_result = visual_search_results.tags[0]
                print("Visual search tag count: {}".format(
                    len(visual_search_results.tags)))

                # List of actions in first tag
                if first_tag_result.actions:
                    first_action_result = first_tag_result.actions[0]
                    print("First tag action count: {}".format(
                        len(first_tag_result.actions)))
                    print("First tag action type: {}".format(
                        first_action_result.action_type))
                else:
                    print("Couldn't find tag actions!")
            else:
                print("Couldn't find image tags!")

    except Exception as e:
        print("Encountered exception. " + str(e))


if __name__ == "__main__":
    import sys, os.path
    sys.path.append(os.path.abspath(os.path.join(__file__, "..", "..", "..")))
    from samples.tools import execute_samples
    execute_samples(globals(), SUBSCRIPTION_KEY)
