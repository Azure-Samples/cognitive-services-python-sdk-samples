import os.path
from pprint import pprint

from azure.cognitiveservices.vision.contentmoderator import ContentModeratorClient
from msrest.authentication import CognitiveServicesCredentials

# Add your Azure Content Moderator subscription key to your environment variables.
SUBSCRIPTION_KEY =  os.environ["CONTENT_MODERATOR_SUBSCRIPTION_KEY"]

def image_review_jobs(subscription_key):
    """ImageReviewJobs.

    This will review an image using workflow and job.
    """

    # The moderation job will use this workflow that you defined earlier.
    # See the quickstart article to learn how to setup custom workflows.
    # https://docs.microsoft.com/azure/cognitive-services/content-moderator/review-tool-user-guide/workflows
    workflow_name = "insert your workflow name here"

    # The name of the team to assign the job to.
    # This must be the team name you used to create your Content Moderator account. You can
    # retrieve your team name from the Content Moderator web site. Your team name is the Id
    # associated with your subscription.
    team_name = "insert your team name here"

    # An image with this text:
    # IF WE DID ALL THE THINGS WE ARE CAPABLE OF DOING, WE WOULD LITERALLY ASTOUND OURSELVE
    # Be sure your workflow create a review for this (e.g. OCR contains some words).
    image_url = "https://moderatorsampleimages.blob.core.windows.net/samples/sample2.jpg"

    # Where you want to receive the approval/refuse event. This is the only way to get this information.
    call_back_endpoint = "https://requestb.in/1l64pe71"

    client = ContentModeratorClient(
        endpoint=os.environ['CONTENT_MODERATOR_ENDPOINT'], # Add your Content Moderator endpoint to your environment variables.
        credentials=CognitiveServicesCredentials(subscription_key)
    )

    print("Create moderation job for an image.\n")
    job_result = client.reviews.create_job(
        team_name=team_name,
        content_type="Image",     # Possible values include: 'Image', 'Text', 'Video'
        content_id="ContentID",  # Id/Name to identify the content submitted.
        workflow_name=workflow_name,
        # Possible values include: 'application/json', 'image/jpeg'
        job_content_type="application/json",
        content_value=image_url,
        call_back_endpoint=call_back_endpoint
    )
    job_id = job_result.job_id

    print("Get job status before review.")
    job_details = client.reviews.get_job_details(
        team_name=team_name,
        job_id=job_id,
    )
    pprint(job_details.as_dict())

    input("\nPerform manual reviews on the Content Moderator Review Site, and hit enter here.")
    job_details = client.reviews.get_job_details(
        team_name=team_name,
        job_id=job_id,
    )
    pprint(job_details.as_dict())

    # Your call back endpoint should have received an event like this:
    # {'call_back_endpoint': 'https://requestb.in/1l64pe71',
    #  'id': '201901d49ee1a417ae45a991c5c1d6af25cace',
    #  'job_execution_report': [{'msg': 'Posted results to the Callbackendpoint: '
    #                                   'https://requestb.in/1l64pe71',
    #                            'ts': '2019-01-11T00:00:15.738452'},
    #                           {'msg': 'Job marked completed and job content has '
    #                                   'been removed',
    #                            'ts': '2019-01-11T00:00:15.6583757'},
    #                           {'msg': 'Execution Complete',
    #                            'ts': '2019-01-11T00:00:15.4872128'},
    #                           {'msg': 'Successfully got hasText response from '
    #                                   'Moderator',
    #                            'ts': '2019-01-11T00:00:14.1389317'},
    #                           {'msg': 'Getting hasText from Moderator',
    #                            'ts': '2019-01-11T00:00:13.0689178'},
    #                           {'msg': 'Starting Execution - Try 1',
    #                            'ts': '2019-01-11T00:00:12.1120066'}],
    #  'result_meta_data': [{'key': 'hasText', 'value': 'True'},
    #                       {'key': 'ocrText',
    #                        'value': 'IF WE DID \r\n'
    #                                 'ALL \r\n'
    #                                 'THE THINGS \r\n'
    #                                 'WE ARE \r\n'
    #                                 'CAPABLE \r\n'
    #                                 'OF DOING, \r\n'
    #                                 'WE WOULD \r\n'
    #                                 'LITERALLY \r\n'
    #                                 'ASTOUND \r\n'
    #                                 'OURSELVE \r\n'}],
    #  'review_id': '201901i6e4de824b0cf4aa587ac37f922f584c2',
    #  'status': 'Complete',
    #  'team_name': 'cspythonsdk',
    #  'type': 'Image',
    #  # 'workflow_id': 'textdetection'}


if __name__ == "__main__":
    import sys, os.path
    sys.path.append(os.path.abspath(os.path.join(__file__, "..", "..", "..")))
    from samples.tools import execute_samples
    execute_samples(globals(), SUBSCRIPTION_KEY_ENV_NAME)
