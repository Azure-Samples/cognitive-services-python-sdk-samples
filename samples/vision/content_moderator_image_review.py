import os.path
from pprint import pprint
import uuid

from azure.cognitiveservices.vision.contentmoderator import ContentModeratorClient
from msrest.authentication import CognitiveServicesCredentials

# Add your Azure Content Moderator subscription key to your environment variables.
SUBSCRIPTION_KEY = os.environ['CONTENT_MODERATOR_SUBSCRIPTION_KEY']

def image_review(subscription_key):
    """ImageReview.

    This will create a review for images.
    """

    # The name of the team to assign the job to.
    # This must be the team name you used to create your Content Moderator account. You can
    # retrieve your team name from the Content Moderator web site. Your team name is the Id
    # associated with your subscription.
    team_name = "insert your team name here"

    # An image to review
    image_url = "https://moderatorsampleimages.blob.core.windows.net/samples/sample5.png"

    # Where you want to receive the approval/refuse event. This is the only way to get this information.
    call_back_endpoint = "https://requestb.in/qmsakwqm"

    client = ContentModeratorClient(
        endpoint=os.environ['CONTENT_MODERATOR_ENDPOINT'], # Add your Content Moderator endpoint to your environment variables.
        credentials=CognitiveServicesCredentials(subscription_key)
    )

    print("Create review for {}.\n".format(image_url))
    review_item = {
        "type": "Image",             # Possible values include: 'Image', 'Text'
        "content": image_url,        # How to download the image
        "content_id": uuid.uuid4(),  # Random id
        "callback_endpoint": call_back_endpoint,
        "metadata": [{
            "key": "sc",
            "value": True  # will be sent to Azure as "str" cast.
        }]
    }

    reviews = client.reviews.create_reviews(
        url_content_type="application/json",
        team_name=team_name,
        create_review_body=[review_item]  # As many review item as you need
    )
    review_id = reviews[0]  # Ordered list of string of review ID

    print("\nGet review details")
    review_details = client.reviews.get_review(
        team_name=team_name, review_id=review_id)
    pprint(review_details.as_dict())

    input("\nPerform manual reviews on the Content Moderator Review Site, and hit enter here.")

    print("\nGet review details")
    review_details = client.reviews.get_review(
        team_name=team_name, review_id=review_id)
    pprint(review_details.as_dict())

    # Your call back endpoint should have received an event like this:
    # {'callback_endpoint': 'https://requestb.in/qmsakwqm',
    #  'content': '',
    #  'content_id': '3ebe16cb-31ed-4292-8b71-1dfe9b0e821f',
    #  'created_by': 'cspythonsdk',
    #  'metadata': [{'key': 'sc', 'value': 'True'}],
    #  'review_id': '201901i14682e2afe624fee95ebb248643139e7',
    #  'reviewer_result_tags': [{'key': 'a', 'value': 'True'},
    #                           {'key': 'r', 'value': 'True'}],
    #  'status': 'Complete',
    #  'sub_team': 'public',
    #  'type': 'Image'}


if __name__ == "__main__":
    import sys, os.path
    sys.path.append(os.path.abspath(os.path.join(__file__, "..", "..", "..")))
    from samples.tools import execute_samples
    execute_samples(globals(), SUBSCRIPTION_KEY_ENV_NAME)
