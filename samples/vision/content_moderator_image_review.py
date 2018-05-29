import os.path
from pprint import pprint
import uuid

from azure.cognitiveservices.vision.contentmoderator import ContentModeratorClient
from azure.cognitiveservices.vision.contentmoderator.models import Content, Review
from msrest.authentication import CognitiveServicesCredentials

SUBSCRIPTION_KEY_ENV_NAME = "CONTENTMODERATOR_SUBSCRIPTION_KEY"
CONTENTMODERATOR_LOCATION = os.environ.get("CONTENTMODERATOR_LOCATION", "westcentralus")

def image_review(subscription_key):
    """ImageReview.

    This will create a review for images.
    """

    # The name of the team to assign the job to.
    # This must be the team name you used to create your Content Moderator account. You can 
    # retrieve your team name from the Content Moderator web site. Your team name is the Id 
    # associated with your subscription.
    team_name = "pysdktesting"

    # An image to review
    image_url = "https://moderatorsampleimages.blob.core.windows.net/samples/sample5.png"

    # Where you want to receive the approval/refuse event. This is the only way to get this information.
    call_back_endpoint = "https://requestb.in/qmsakwqm"

    client = ContentModeratorClient(
        CONTENTMODERATOR_LOCATION+'.api.cognitive.microsoft.com',
        CognitiveServicesCredentials(subscription_key)
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
        "application/json",
        team_name,
        [review_item]  # As many review item as you need
    )
    review_id = reviews[0]  # Ordered list of string of review ID

    print("\nGet review details")
    review_details = client.reviews.get_review(team_name, review_id)
    pprint(review_details.as_dict())

    input("\nPerform manual reviews on the Content Moderator Review Site, and hit enter here.")

    print("\nGet review details")
    review_details = client.reviews.get_review(team_name, review_id)
    pprint(review_details.as_dict())

    # Your call back endpoint should have received an event like this:
    # {
    #   "ReviewId": "201802idca99b6f3f7d4418b381d8c1bcc7e99a",
    #   "ModifiedOn": "2018-02-07T22:39:17.2868098Z",
    #   "ModifiedBy": "unknown",
    #   "CallBackType": "Review",
    #   "ContentId": "3dd26599-264a-4c3d-af00-3d8726a59e95",
    #   "ContentType": "Image",
    #   "Metadata": {
    #     "sc": "True"
    #   },
    #   "ReviewerResultTags": {
    #     "a": "True",
    #     "r": "False"
    #   }
    # }

if __name__ == "__main__":
    import sys, os.path
    sys.path.append(os.path.abspath(os.path.join(__file__, "..", "..", "..")))
    from samples.tools import execute_samples
    execute_samples(globals(), SUBSCRIPTION_KEY_ENV_NAME)