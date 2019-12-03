import os.path
from pprint import pprint
from random import random
import uuid

from azure.cognitiveservices.vision.contentmoderator import ContentModeratorClient
from azure.cognitiveservices.vision.contentmoderator.models import Frames
from msrest.authentication import CognitiveServicesCredentials

# Add your Azure Content Moderator subscription key to your environment variables.
SUBSCRIPTION_KEY = os.environ['CONTENT_MODERATOR_SUBSCRIPTION_KEY']

def video_review(subscription_key):
    """VideoReview.

    This will create and publish a review for video
    """

    # The name of the team to assign the job to.
    # This must be the team name you used to create your Content Moderator account. You can
    # retrieve your team name from the Content Moderator web site. Your team name is the Id
    # associated with your subscription.
    team_name = "insert your team name here"

    # Create a review with the content pointing to a streaming endpoint (manifest)
    streamingcontent = "https://amssamples.streaming.mediaservices.windows.net/91492735-c523-432b-ba01-faba6c2206a2/AzureMediaServicesPromo.ism/manifest"

    frame1_url = "https://blobthebuilder.blob.core.windows.net/sampleframes/ams-video-frame1-00-17.PNG"
    frame2_url = "https://blobthebuilder.blob.core.windows.net/sampleframes/ams-video-frame-2-01-04.PNG"
    frame3_url = "https://blobthebuilder.blob.core.windows.net/sampleframes/ams-video-frame-3-02-24.PNG"

    client = ContentModeratorClient(
        endpoint=os.environ['CONTENT_MODERATOR_ENDPOINT'], # Add your Content Moderator endpoint to your environment variables.
        credentials=CognitiveServicesCredentials(subscription_key)
    )

    #
    # Create a video review
    #
    print("Create review for {}.\n".format(streamingcontent))
    review_item = {
        "content": streamingcontent,  # How to download the image
        "content_id": uuid.uuid4(),  # Random id
        # Note: to create a published review, set the Status to "Pending".
        # However, you cannot add video frames or a transcript to a published review.
        "status": "Unpublished"
    }

    reviews = client.reviews.create_video_reviews(
        content_type="application/json",
        team_name=team_name,
        # As many review item as you need
        create_video_reviews_body=[review_item]
    )
    review_id = reviews[0]  # Ordered list of string of review ID

    #
    # Add the frames from 17, 64, and 144 seconds.
    #
    print("\nAdding frames to the review {}".format(review_id))

    def create_frames_to_add_to_reviews(timestamp_seconds, url):
        return {
            'timestamp': timestamp_seconds * 1000,
            'frame_image': url,
            'reviewer_result_tags': [
                # Note: All non str value will be casted using "str()"
                {'key': 'reviewRecommended', 'value': True},
                {'key': 'adultScore', 'value': random()},
                {'key': 'a', 'value': False},
                {'key': 'racyScore', 'value': random()},
                {'key': 'a', 'value': False},
            ],
            'metadata': [
                # Note: All non str value will be casted using "str()"
                {'key': 'tag1', 'value': 'tag1'},
            ]
        }

    client.reviews.add_video_frame_url(
        content_type="application/json",
        team_name=team_name,
        review_id=review_id,
        video_frame_body=[
            create_frames_to_add_to_reviews(17, frame1_url),
            create_frames_to_add_to_reviews(64, frame2_url),
            create_frames_to_add_to_reviews(144, frame3_url)
        ]
    )

    #
    # Get frames
    #
    print("\nGetting frames for the review with ID {}".format(review_id))
    frames = client.reviews.get_video_frames(
        team_name=team_name,
        review_id=review_id,
        start_seed=0,
        no_of_records=100
    )
    assert isinstance(frames, Frames)
    pprint(frames.as_dict())

    #
    # Get reviews details
    #
    print("\nGetting review details for the review with ID {}".format(review_id))
    review_details = client.reviews.get_review(
        team_name=team_name, review_id=review_id)
    pprint(review_details.as_dict())

    #
    # Public review
    #
    client.reviews.publish_video_review(
        team_name=team_name, review_id=review_id)

    print("\nOpen your Content Moderator Dashboard and select Review > Video to see the review.")


if __name__ == "__main__":
    import sys, os.path
    sys.path.append(os.path.abspath(os.path.join(__file__, "..", "..", "..")))
    from samples.tools import execute_samples
    execute_samples(globals(), SUBSCRIPTION_KEY_ENV_NAME)
