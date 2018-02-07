import os.path
from pprint import pprint

from azure.cognitiveservices.vision.contentmoderator import ContentModeratorClient
from msrest.authentication import CognitiveServicesCredentials

SUBSCRIPTION_KEY_ENV_NAME = "CONTENTMODERATOR_SUBSCRIPTION_KEY"
CONTENTMODERATOR_LOCATION = os.environ.get("CONTENTMODERATOR_LOCATION", "westcentralus")


def image_lists(subscription_key):
    """ImageList.

    This will review an image using workflow and job.
    """
    
    client = ContentModeratorClient(
        CONTENTMODERATOR_LOCATION+'.api.cognitive.microsoft.com',
        CognitiveServicesCredentials(subscription_key)
    )

    print("Creating list MyList\n")
    custom_list = client.list_management_image_lists.create(
        "application/json",
        {
            "name": "MyList",
            "description": "A sample list",
            "metadata": {
                "key_one": "Acceptable",
                "key_two": "Potentially racy"
            }
        }
    )
    print("Item created:")
    pprint(custom_list.as_dict())
    list_id = custom_list.id

    def add_images(list_id, image_url, label):
        print("Adding image {} to list {} with label {}.".format(image_url, list_id, label))
        added_image = client.list_management_image.add_image_url_input(
            list_id,
            "application/json",
            data_representation="URL",
            value=image_url,
            label=label
        )
        pprint(added_image.as_dict())

if __name__ == "__main__":
    import sys, os.path
    sys.path.append(os.path.abspath(os.path.join(__file__, "..", "..")))
    from tools import execute_samples
    execute_samples(globals(), SUBSCRIPTION_KEY_ENV_NAME)