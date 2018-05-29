import os.path
from pprint import pprint
import time

from azure.cognitiveservices.vision.contentmoderator import ContentModeratorClient
from azure.cognitiveservices.vision.contentmoderator.models import (
    APIErrorException,
    Evaluate,
    OCR,
    FoundFaces
)
from msrest.authentication import CognitiveServicesCredentials

SUBSCRIPTION_KEY_ENV_NAME = "CONTENTMODERATOR_SUBSCRIPTION_KEY"
CONTENTMODERATOR_LOCATION = os.environ.get("CONTENTMODERATOR_LOCATION", "westcentralus")

IMAGE_LIST = [
    "https://moderatorsampleimages.blob.core.windows.net/samples/sample2.jpg",
    "https://moderatorsampleimages.blob.core.windows.net/samples/sample5.png"
]

def image_moderation(subscription_key):
    """ImageModeration.

    This will review an image using workflow and job.
    """
    
    client = ContentModeratorClient(
        CONTENTMODERATOR_LOCATION+'.api.cognitive.microsoft.com',
        CognitiveServicesCredentials(subscription_key)
    )
    
    for image_url in IMAGE_LIST:
        print("\nEvaluate image {}".format(image_url))

        print("\nEvaluate for adult and racy content.")
        evaluation = client.image_moderation.evaluate_url_input(
            "application/json",
            data_representation="URL",
            value=image_url,
            cache_image=True,
        )
        assert isinstance(evaluation, Evaluate)
        pprint(evaluation.as_dict())

        print("\nDetect and extract text.")
        evaluation = client.image_moderation.ocr_url_input(
            "eng",
            "application/json",
            data_representation="URL",
            value=image_url,
            cache_image=True,
        )
        assert isinstance(evaluation, OCR)
        pprint(evaluation.as_dict())

        print("\nDetect faces.")
        evaluation = client.image_moderation.find_faces_url_input(
            "application/json",
            data_representation="URL",
            value=image_url,
            cache_image=True,
        )
        assert isinstance(evaluation, FoundFaces)
        pprint(evaluation.as_dict())

if __name__ == "__main__":
    import sys, os.path
    sys.path.append(os.path.abspath(os.path.join(__file__, "..", "..", "..")))
    from samples.tools import execute_samples
    execute_samples(globals(), SUBSCRIPTION_KEY_ENV_NAME)
