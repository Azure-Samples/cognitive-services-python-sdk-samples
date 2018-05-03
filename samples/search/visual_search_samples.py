import json
import os.path

from azure.cognitiveservices.search.visualsearch import VisualSearchAPI
from azure.cognitiveservices.search.visualsearch.models import VisualSearchRequest
from msrest.authentication import CognitiveServicesCredentials

SUBSCRIPTION_KEY_ENV_NAME = "VISUALSEARCH_SUBSCRIPTION_KEY"

CWD = os.path.dirname(__file__)
TEST_IMAGES = os.path.join(CWD, "TestImages")

def search_image_binary(subscription_key):
    """VisualSearchImageBinary.

    This will send an image binary in the body of the post request and print out the imageInsightsToken, the number of tags, the number of actions, and the first actionType.
    """
    client = VisualSearchAPI(CognitiveServicesCredentials(subscription_key))

    image_path = os.path.join(TEST_IMAGES, "image.jpg")
    with open(image_path, "rb") as image_fd:

        # You need to pass the serialized form of the model
        knowledge_request = json.dumps(VisualSearchRequest().serialize())

        result = client.images.visual_search(image=image_fd, knowledge_request=knowledge_request)

        print("Search visual search request with binary of dog image")
        if not result:
            print("No visual search result data.")
            return

        # Visual Search results
        if result.image.image_insights_token:
            print("Uploaded image insights token: {}".format(result.image.image_insights_token))
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
                print("First tag action type: {}".formaT(first_tag_action.action_type))
            else:
                print("Couldn't find tag actions!")
        else:
            print("Couldn't find image tags!")

if __name__ == "__main__":
    import sys, os.path
    sys.path.append(os.path.abspath(os.path.join(__file__, "..", "..")))
    from tools import execute_samples
    execute_samples(globals(), SUBSCRIPTION_KEY_ENV_NAME)