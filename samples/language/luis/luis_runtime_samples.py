import json
import os.path
from pprint import pprint

from azure.cognitiveservices.language.luis.runtime import LUISRuntimeClient

from msrest.authentication import CognitiveServicesCredentials

SUBSCRIPTION_KEY_ENV_NAME = "LUIS_SUBSCRIPTION_KEY"

CWD = os.path.dirname(__file__)


def runtime(subscription_key):
    """Resolve.

    This will execute LUIS prediction
    """
    client = LUISRuntimeClient(
        'https://westus.api.cognitive.microsoft.com',
        CognitiveServicesCredentials(subscription_key),
    )

    try:
        query = "Look for hotels near LAX airport"
        print("Executing query: {}".format(query))
        result = client.prediction.resolve(
            "bce13896-4de3-4783-9696-737d8fde8cd1",  # LUIS Application ID
            query
        )

        print("\nDetected intent: {} (score: {:d}%)".format(
            result.top_scoring_intent.intent,
            int(result.top_scoring_intent.score*100)
        ))
        print("Detected entities:")
        for entity in result.entities:
            print("\t-> Entity '{}' (type: {}, score:{:d}%)".format(
                entity.entity,
                entity.type,
                int(entity.additional_properties['score']*100)
            ))
        print("\nComplete result object as dictionnary")
        pprint(result.as_dict())

    except Exception as err:
        print("Encountered exception. {}".format(err))


if __name__ == "__main__":
    import sys
    import os.path
    sys.path.append(os.path.abspath(os.path.join(__file__, "..", "..")))
    from tools import execute_samples
    execute_samples(globals(), SUBSCRIPTION_KEY_ENV_NAME)
