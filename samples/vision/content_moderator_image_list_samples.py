import os.path
from pprint import pprint
import time

from azure.cognitiveservices.vision.contentmoderator import ContentModeratorClient
from azure.cognitiveservices.vision.contentmoderator.models import (
    APIErrorException,
    ImageList,
    ImageIds,
    Image,
    RefreshIndex,
    MatchResponse
)
from msrest.authentication import CognitiveServicesCredentials

# Add your Azure Content Moderator subscription key to your environment variables.
SUBSCRIPTION_KEY = os.environ['CONTENT_MODERATOR_SUBSCRIPTION_KEY']

# The number of minutes to delay after updating the search index before
# performing image match operations against the list.
LATENCY_DELAY = 0.5

IMAGE_LIST = {
    "Sports": [
        "https://moderatorsampleimages.blob.core.windows.net/samples/sample4.png",
        "https://moderatorsampleimages.blob.core.windows.net/samples/sample6.png",
        "https://moderatorsampleimages.blob.core.windows.net/samples/sample9.png"
    ],
    "Swimsuit": [
        "https://moderatorsampleimages.blob.core.windows.net/samples/sample1.jpg",
        "https://moderatorsampleimages.blob.core.windows.net/samples/sample3.png",
        "https://moderatorsampleimages.blob.core.windows.net/samples/sample4.png",
        "https://moderatorsampleimages.blob.core.windows.net/samples/sample16.png"
    ]
}

IMAGES_TO_MATCH = [
    "https://moderatorsampleimages.blob.core.windows.net/samples/sample1.jpg",
    "https://moderatorsampleimages.blob.core.windows.net/samples/sample4.png",
    "https://moderatorsampleimages.blob.core.windows.net/samples/sample5.png",
    "https://moderatorsampleimages.blob.core.windows.net/samples/sample16.png"
]


def image_lists(subscription_key):
    """ImageList.

    This will review an image using workflow and job.
    """

    client = ContentModeratorClient(
        endpoint=os.environ['CONTENT_MODERATOR_ENDPOINT'], # Add your Content Moderator endpoint to your environment variables.

        credentials=CognitiveServicesCredentials(subscription_key)
    )

    print("Creating list MyList\n")
    custom_list = client.list_management_image_lists.create(
        content_type="application/json",
        body={
            "name": "MyList",
            "description": "A sample list",
            "metadata": {
                "key_one": "Acceptable",
                "key_two": "Potentially racy"
            }
        }
    )
    print("List created:")
    assert isinstance(custom_list, ImageList)
    pprint(custom_list.as_dict())
    list_id = custom_list.id

    #
    # Add images
    #

    def add_images(list_id, image_url, label):
        """Generic add_images from url and label."""
        print("\nAdding image {} to list {} with label {}.".format(
            image_url, list_id, label))
        try:
            added_image = client.list_management_image.add_image_url_input(
                list_id=list_id,
                content_type="application/json",
                data_representation="URL",
                value=image_url,
                label=label
            )
        except APIErrorException as err:
            # sample4 will fail
            print("Unable to add image to list: {}".format(err))
        else:
            assert isinstance(added_image, Image)
            pprint(added_image.as_dict())
            return added_image

    print("\nAdding images to list {}".format(list_id))
    index = {}  # Keep an index url to id for later removal
    for label, urls in IMAGE_LIST.items():
        for url in urls:
            image = add_images(list_id, url, label)
            if image:
                index[url] = image.content_id

    #
    # Get all images ids
    #
    print("\nGetting all image IDs for list {}".format(list_id))
    image_ids = client.list_management_image.get_all_image_ids(list_id=list_id)
    assert isinstance(image_ids, ImageIds)
    pprint(image_ids.as_dict())

    #
    # Update list details
    #
    print("\nUpdating details for list {}".format(list_id))
    updated_list = client.list_management_image_lists.update(
        list_id=list_id,
        content_type="application/json",
        body={
            "name": "Swimsuits and sports"
        }
    )
    assert isinstance(updated_list, ImageList)
    pprint(updated_list.as_dict())

    #
    # Get list details
    #
    print("\nGetting details for list {}".format(list_id))
    list_details = client.list_management_image_lists.get_details(
        list_id=list_id)
    assert isinstance(list_details, ImageList)
    pprint(list_details.as_dict())

    #
    # Refresh the index
    #
    print("\nRefreshing the search index for list {}".format(list_id))
    refresh_index = client.list_management_image_lists.refresh_index_method(
        list_id=list_id)
    assert isinstance(refresh_index, RefreshIndex)
    pprint(refresh_index.as_dict())

    print("\nWaiting {} minutes to allow the server time to propagate the index changes.".format(
        LATENCY_DELAY))
    time.sleep(LATENCY_DELAY * 60)

    #
    # Match images against the image list.
    #
    for image_url in IMAGES_TO_MATCH:
        print("\nMatching image {} against list {}".format(image_url, list_id))
        match_result = client.image_moderation.match_url_input(
            content_type="application/json",
            list_id=list_id,
            data_representation="URL",
            value=image_url,
        )
        assert isinstance(match_result, MatchResponse)
        print("Is match? {}".format(match_result.is_match))
        print("Complete match details:")
        pprint(match_result.as_dict())

    #
    # Remove images
    #
    correction = "https://moderatorsampleimages.blob.core.windows.net/samples/sample16.png"
    print("\nRemove image {} from list {}".format(correction, list_id))
    client.list_management_image.delete_image(
        list_id=list_id,
        image_id=index[correction]
    )

    #
    # Refresh the index
    #
    print("\nRefreshing the search index for list {}".format(list_id))
    client.list_management_image_lists.refresh_index_method(list_id=list_id)

    print("\nWaiting {} minutes to allow the server time to propagate the index changes.".format(
        LATENCY_DELAY))
    time.sleep(LATENCY_DELAY * 60)

    #
    # Re-match
    #
    print("\nMatching image. The removed image should not match")
    for image_url in IMAGES_TO_MATCH:
        print("\nMatching image {} against list {}".format(image_url, list_id))
        match_result = client.image_moderation.match_url_input(
            content_type="application/json",
            list_id=list_id,
            data_representation="URL",
            value=image_url,
        )
        assert isinstance(match_result, MatchResponse)
        print("Is match? {}".format(match_result.is_match))
        print("Complete match details:")
        pprint(match_result.as_dict())

    #
    # Delete all images
    #
    print("\nDelete all images in the image list {}".format(list_id))
    client.list_management_image.delete_all_images(list_id=list_id)

    #
    # Delete list
    #
    print("\nDelete the image list {}".format(list_id))
    client.list_management_image_lists.delete(list_id=list_id)

    #
    # Get all list ids
    #
    print("\nVerify that the list {} was deleted.".format(list_id))
    image_lists = client.list_management_image_lists.get_all_image_lists()
    assert not any(list_id == image_list.id for image_list in image_lists)


if __name__ == "__main__":
    import sys, os.path
    sys.path.append(os.path.abspath(os.path.join(__file__, "..", "..", "..")))
    from samples.tools import execute_samples
    execute_samples(globals(), SUBSCRIPTION_KEY_ENV_NAME)
