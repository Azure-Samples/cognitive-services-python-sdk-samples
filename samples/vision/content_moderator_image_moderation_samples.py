import os.path
from pprint import pprint

from azure.cognitiveservices.vision.contentmoderator import ContentModeratorClient
from azure.cognitiveservices.vision.contentmoderator.models import (
    Evaluate,
    OCR,
    FoundFaces
)
from msrest.authentication import CognitiveServicesCredentials

# Add your Azure Content Moderator subscription key to your environment variables.
SUBSCRIPTION_KEY = os.environ['CONTENT_MODERATOR_SUBSCRIPTION_KEY']

IMAGE_LIST = [
    "https://moderatorsampleimages.blob.core.windows.net/samples/sample2.jpg",
    "https://moderatorsampleimages.blob.core.windows.net/samples/sample5.png"
]


def image_moderation(subscription_key):
    """ImageModeration.

    This will review an image using workflow and job.
    """

    client = ContentModeratorClient(
        endpoint=os.environ['CONTENT_MODERATOR_ENDPOINT'], # Add your Content Moderator endpoint to your environment variables.
        credentials=CognitiveServicesCredentials(subscription_key)
    )

    for image_url in IMAGE_LIST:
        print("\nEvaluate image {}".format(image_url))

        print("\nEvaluate for adult and racy content.")
        evaluation = client.image_moderation.evaluate_url_input(
            content_type="application/json",
            cache_image=True,
            data_representation="URL",
            value=image_url
        )
        assert isinstance(evaluation, Evaluate)
        pprint(evaluation.as_dict())

        print("\nDetect and extract text.")
        evaluation = client.image_moderation.ocr_url_input(
            language="eng",
            content_type="application/json",
            data_representation="URL",
            value=image_url,
            cache_image=True,
        )
        assert isinstance(evaluation, OCR)
        pprint(evaluation.as_dict())

        print("\nDetect faces.")
        evaluation = client.image_moderation.find_faces_url_input(
            content_type="application/json",
            cache_image=True,
            data_representation="URL",
            value=image_url
        )
        assert isinstance(evaluation, FoundFaces)
        pprint(evaluation.as_dict())


if __name__ == "__main__":
    import sys, os.path
    sys.path.append(os.path.abspath(os.path.join(__file__, "..", "..", "..")))
    from samples.tools import execute_samples
    execute_samples(globals(), SUBSCRIPTION_KEY_ENV_NAME)
