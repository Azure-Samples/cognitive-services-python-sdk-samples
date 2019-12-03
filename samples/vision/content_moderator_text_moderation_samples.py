import os, os.path
from pprint import pprint

from azure.cognitiveservices.vision.contentmoderator import ContentModeratorClient
from azure.cognitiveservices.vision.contentmoderator.models import (
    Screen
)
from msrest.authentication import CognitiveServicesCredentials

# Add your Azure Content Moderator subscription key to your environment variables.
SUBSCRIPTION_KEY = os.environ['CONTENT_MODERATOR_SUBSCRIPTION_KEY']

TEXT_FOLDER = os.path.join(os.path.dirname(
    os.path.realpath(__file__)), "text_files")

# The number of minutes to delay after updating the search index before
# performing image match operations against the list.
LATENCY_DELAY = 0.5


def text_moderation(subscription_key):
    """TextModeration.

    This will moderate a given long text.
    """

    client = ContentModeratorClient(
        endpoint=os.environ['CONTENT_MODERATOR_ENDPOINT'], # Add your Content Moderator endpoint to your environment variables.
        credentials=CognitiveServicesCredentials(subscription_key)
    )

    # Screen the input text: check for profanity,
    # do autocorrect text, and check for personally identifying
    # information (PII)
    with open(os.path.join(TEXT_FOLDER, 'content_moderator_text_moderation.txt'), "rb") as text_fd:
        screen = client.text_moderation.screen_text(
            text_content_type="text/plain",
            text_content=text_fd,
            language="eng",
            autocorrect=True,
            pii=True
        )
        assert isinstance(screen, Screen)
        pprint(screen.as_dict())


if __name__ == "__main__":
    import sys, os.path
    sys.path.append(os.path.abspath(os.path.join(__file__, "..", "..", "..")))
    from samples.tools import execute_samples
    execute_samples(globals(), SUBSCRIPTION_KEY_ENV_NAME)
