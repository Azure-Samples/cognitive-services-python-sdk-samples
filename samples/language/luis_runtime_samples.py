import json
import os.path

from azure.cognitiveservices.language.luis.authoring import LUISAuthoringClient
from azure.cognitiveservices.language.luis.authoring.models import (
    ErrorResponseException
)
from azure.cognitiveservices.language.luis.runtime import LUISRuntimeClient

from msrest.authentication import CognitiveServicesCredentials

SUBSCRIPTION_KEY_ENV_NAME = "LUIS_SUBSCRIPTION_KEY"

CWD = os.path.dirname(__file__)

def runtime(subscription_key):
    """Authoring.

    This will execute LUIS command
    """
    # First step will be to create the test app from an already made file.
    # If you wish to create your own app programmatically, please refer
    # to the other sample "luis_authoring_samples.py"
    with open(os.path.join(CWD, "luis", "LuisApp.json"), 'r') as reader:
        luis_app_as_json = json.load(reader)

    # Azure prod url
    # This works with programmatic key from luis.ia
    base_url = "https://westus.api.cognitive.microsoft.com/luis/api/v2.0"
    # luis.ai portal
    #           https://westus.api.cognitive.microsoft.com/luis/api/v2.0/apps/import?appName=rezrezre
    # base_url = 'https://api.cognitive.microsoft.com/luis/api/v2.0'

    try:
        authoring_client = LUISAuthoringClient(CognitiveServicesCredentials(subscription_key), base_url=base_url)
        authoring_client.apps.import_method(
            luis_app_as_json,
            app_name="LuisTesting"
        )
    except ErrorResponseException as err:
        # The status code of the error should be a good indication of what occurred. However, if you'd like more details, you can dig into the response.
        # Please note that depending on the type of error, the response schema might be different, so you aren't guaranteed a specific error response schema.

        print("Exception occurred, status code {} with reason {}.\n".format(err.response.status_code, err))

        # if you'd like more descriptive information (if available)
        if err.error:
            print("This is the errors I have:")
            print(err.error.as_dict())
        else:
            print("There was no details on the error.")

    # client = LUISAuthoringClient(CognitiveServicesCredentials(subscription_key))

    # try:
    #     result = client.spell_checker("Bill Gatas", mode="proof")
    #     print("Correction for Query# \"bill gatas\"")

    #     if result.flagged_tokens:
    #         first_spellcheck_result = result.flagged_tokens[0]

    #         print("SpellCheck result count: {}".format(len(result.flagged_tokens)))
    #         print("First SpellCheck token: {}".format(first_spellcheck_result.token))
    #         print("First SpellCheck type: {}".format(first_spellcheck_result.type))
    #         print("First SpellCheck suggestion count: {}".format(len(first_spellcheck_result.suggestions)))

    #         if first_spellcheck_result.suggestions:
    #             first_suggestion = first_spellcheck_result.suggestions[0]
    #             print("First SpellCheck suggestion score: {}".format(first_suggestion.score))
    #             print("First SpellCheck suggestion: {}".format(first_suggestion.suggestion))
    #         else:
    #             print("Couldn't get any Spell check results!")

    #     else:
    #         print("Didn't see any SpellCheck results..")

    # except Exception as err:
    #     print("Encountered exception. {}".format(err))


if __name__ == "__main__":
    import sys, os.path
    sys.path.append(os.path.abspath(os.path.join(__file__, "..", "..")))
    from tools import execute_samples
    execute_samples(globals(), SUBSCRIPTION_KEY_ENV_NAME)
