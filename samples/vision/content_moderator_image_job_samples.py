import os.path
from pprint import pprint

from azure.cognitiveservices.vision.contentmoderator import ContentModeratorClient
from azure.cognitiveservices.vision.contentmoderator.models import Content
from msrest.authentication import CognitiveServicesCredentials

SUBSCRIPTION_KEY_ENV_NAME = "CONTENTMODERATOR_SUBSCRIPTION_KEY"
CONTENTMODERATOR_LOCATION = os.environ.get("CONTENTMODERATOR_LOCATION", "westcentralus")

def image_review_jobs(subscription_key):
    """ImageReviewJobs.

    This will review an image using workflow and job.
    """

    # The moderation job will use this workflow that you defined earlier.
    # See the quickstart article to learn how to setup custom workflows.
    # https://docs.microsoft.com/azure/cognitive-services/content-moderator/review-tool-user-guide/workflows
    workflow_name = "OCR"

    # The name of the team to assign the job to.
    # This must be the team name you used to create your Content Moderator account. You can 
    # retrieve your team name from the Content Moderator web site. Your team name is the Id 
    # associated with your subscription.
    team_name = "pysdktesting"

    # An image with this text:
    # IF WE DID ALL THE THINGS WE ARE CAPABLE OF DOING, WE WOULD LITERALLY ASTOUND OURSELVE 
    # Be sure your workflow create a review for this (e.g. OCR contains some words).
    image_url = "https://moderatorsampleimages.blob.core.windows.net/samples/sample2.jpg"

    # Where you want to receive the approval/refuse event. This is the only way to get this information.
    call_back_endpoint = "https://requestb.in/1l64pe71"

    client = ContentModeratorClient(
        CONTENTMODERATOR_LOCATION+'.api.cognitive.microsoft.com',
        CognitiveServicesCredentials(subscription_key)
    )

    print("Create moderation job for an image.\n")
    job_result = client.reviews.create_job(
        team_name,
        "Image",     # Possible values include: 'Image', 'Text', 'Video'
        "ContentID", # Id/Name to identify the content submitted.
        workflow_name,
        "application/json", # Possible values include: 'application/json', 'image/jpeg'
        image_url,
        call_back_endpoint=call_back_endpoint
    )
    job_id = job_result.job_id

    print("Get job status before review.")
    job_details = client.reviews.get_job_details(
        team_name,
        job_id,
    )
    pprint(job_details.as_dict())    

    input("\nPerform manual reviews on the Content Moderator Review Site, and hit enter here.")
    job_details = client.reviews.get_job_details(
        team_name,
        job_id,
    )
    pprint(job_details.as_dict())

    # Your call back endpoint should have received an event like this:
    # {
    #   "ReviewId": "201802i2957280730e04578aefe678ba6e5ea24",
    #   "ModifiedOn": "2018-02-06T23:46:26.3121698Z",
    #   "ModifiedBy": "unknown",
    #   "CallBackType": "Review",
    #   "ContentId": "ContentID",
    #   "ContentType": "Image",
    #   "Metadata": {
    #     "hastext": "True",
    #     "ocrtext": "IF WE DID \r\nALL \r\nTHE THINGS \r\nWE ARE \r\nCAPABLE \r\nOF DOING, \r\nWE WOULD \r\nLITERALLY \r\nASTOUND \r\nOURSELVE \r\n",
    #     "imagename": "ContentID"
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