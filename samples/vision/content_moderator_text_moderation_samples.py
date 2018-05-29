import os.path
from pprint import pprint
import time

from azure.cognitiveservices.vision.contentmoderator import ContentModeratorClient
from azure.cognitiveservices.vision.contentmoderator.models import (
    Screen
)
from msrest.authentication import CognitiveServicesCredentials

SUBSCRIPTION_KEY_ENV_NAME = "CONTENTMODERATOR_SUBSCRIPTION_KEY"
CONTENTMODERATOR_LOCATION = os.environ.get("CONTENTMODERATOR_LOCATION", "westcentralus")

# The number of minutes to delay after updating the search index before
# performing image match operations against the list.
LATENCY_DELAY = 0.5

TEXT = """
Is this a grabage email abcdef@abcd.com, phone: 6657789887, IP: 255.255.255.255, 1 Microsoft Way, Redmond, WA 98052.
Crap is the profanity here. Is this information PII? phone 3144444444
"""

def text_moderation(subscription_key):
    """TextModeration.

    This will moderate a given long text.
    """
    
    client = ContentModeratorClient(
        CONTENTMODERATOR_LOCATION+'.api.cognitive.microsoft.com',
        CognitiveServicesCredentials(subscription_key)
    )

    # Screen the input text: check for profanity, 
    # do autocorrect text, and check for personally identifying 
    # information (PII)
    screen = client.text_moderation.screen_text(
        "eng",
        "text/plain",
        TEXT,
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