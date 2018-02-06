import os.path

from azure.cognitiveservices.vision.contentmoderator import ContentModeratorClient
from azure.cognitiveservices.vision.contentmoderator.models import Content
from msrest.authentication import CognitiveServicesCredentials

SUBSCRIPTION_KEY_ENV_NAME = "CONTENTMODERATOR_SUBSCRIPTION_KEY"
CONTENTMODERATOR_LOCATION = os.environ.get("CONTENTMODERATOR_LOCATION", "westcentralus")

IMAGES_FOLDER = os.path.join(os.path.dirname(os.path.realpath(__file__)), "images")

def image_review(subscription_key):
    """ImageReview.

    This will analysis an image in a review.
    """

    # The moderation job will use this workflow that you defined earlier.
    # See the quickstart article to learn how to setup custom workflows.
    workflow_name = "OCR"

    # The name of the team to assign the job to.
    # This must be the team name you used to create your Content Moderator account. You can 
    # retrieve your team name from the Conent Moderator web site. Your team name is the Id 
    # associated with your subscription.
    team_name = "testreview6"

    image_url = "https://moderatorsampleimages.blob.core.windows.net/samples/sample2.jpg"

    client = ContentModeratorClient(
        CONTENTMODERATOR_LOCATION+'.api.cognitive.microsoft.com',
        CognitiveServicesCredentials(subscription_key)
    )

    print("Create moderation job for an image.")
    job_result = client.reviews.create_job(
        team_name,
        "Image",     # Possible values include: 'Image', 'Text', 'Video'
        "ContentID", # Id/Name to identify the content submitted.
        workflow_name,
        "application/json", # Possible values include: 'application/json', 'image/jpeg'
        image_url
    )

    job_id = job_result.job_id

    print("Get job status before review.")
    job_details = client.reviews.get_job_details(
        team_name,
        job_id,
    )

    print(job_details.as_dict())


if __name__ == "__main__":
    import sys, os.path
    sys.path.append(os.path.abspath(os.path.join(__file__, "..", "..")))
    from tools import execute_samples
    execute_samples(globals(), SUBSCRIPTION_KEY_ENV_NAME)