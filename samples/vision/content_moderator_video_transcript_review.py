from io import BytesIO
import os.path
from pprint import pprint
from random import random
import uuid

from azure.cognitiveservices.vision.contentmoderator import ContentModeratorClient
from azure.cognitiveservices.vision.contentmoderator.models import Content, Review, Frames, Screen
from msrest.authentication import CognitiveServicesCredentials

SUBSCRIPTION_KEY_ENV_NAME = "CONTENTMODERATOR_SUBSCRIPTION_KEY"
CONTENTMODERATOR_LOCATION = os.environ.get("CONTENTMODERATOR_LOCATION", "westcentralus")


def video_transcript_review(subscription_key):
    """VideoTranscriptReview.

    This will create and publish a transcript review for video
    """

    # The name of the team to assign the job to.
    # This must be the team name you used to create your Content Moderator account. You can 
    # retrieve your team name from the Content Moderator web site. Your team name is the Id 
    # associated with your subscription.
    team_name = "pysdktesting"

    # Create a review with the content pointing to a streaming endpoint (manifest)
    streamingcontent = "https://amssamples.streaming.mediaservices.windows.net/91492735-c523-432b-ba01-faba6c2206a2/AzureMediaServicesPromo.ism/manifest"

    transcript = b"""WEBVTT

        01:01.000 --> 02:02.000
        First line with a crap word in a transcript.

        02:03.000 --> 02:25.000
        This is another line in the transcript.
    """

    client = ContentModeratorClient(
        CONTENTMODERATOR_LOCATION+'.api.cognitive.microsoft.com',
        CognitiveServicesCredentials(subscription_key)
    )

    #
    # Create a video review
    #
    print("Create review for {}.\n".format(streamingcontent))
    review_item = {
        "content": streamingcontent, # How to download the image
        "content_id": uuid.uuid4(),  # Random id
        # Note: to create a published review, set the Status to "Pending".
        # However, you cannot add video frames or a transcript to a published review.
        "status": "Unpublished"
    }

    reviews = client.reviews.create_video_reviews(
        "application/json",
        team_name,
        [review_item]  # As many review item as you need
    )
    review_id = reviews[0]  # Ordered list of string of review ID

    #
    # Add transcript
    #
    print("\nAdding transcript to the review {}".format(review_id))
    client.reviews.add_video_transcript(
        team_name,
        review_id,
        BytesIO(transcript),  # Can be a file descriptor, as long as its stream type
    )

    #
    # Add transcript moderation result
    #
    print("\nAdding a transcript moderation result to the review with ID {}".format(review_id))
    screen = client.text_moderation.screen_text(
        "eng",
        "text/plain",
        transcript,
    )
    assert isinstance(screen, Screen)
    pprint(screen.as_dict())

    # Build a terms list with index
    terms = []
    for term in screen.terms:
        terms.append({"index": term.index, "term": term.term})

    client.reviews.add_video_transcript_moderation_result(
        "application/json",
        team_name,
        review_id,
        [{
            "timestamp": 0,
            "terms": terms
        }]
    )

    #
    # Public review
    #
    client.reviews.publish_video_review(team_name, review_id)

    print("\nOpen your Content Moderator Dashboard and select Review > Video to see the review.")


if __name__ == "__main__":
    import sys, os.path
    sys.path.append(os.path.abspath(os.path.join(__file__, "..", "..")))
    from tools import execute_samples
    execute_samples(globals(), SUBSCRIPTION_KEY_ENV_NAME)
