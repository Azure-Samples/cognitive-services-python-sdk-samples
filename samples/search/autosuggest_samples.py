import os

from azure.cognitiveservices.search.autosuggest import AutoSuggestClient
from azure.cognitiveservices.search.autosuggest.models import (
    Suggestions,
    SuggestionsSuggestionGroup,
    SearchAction,
    ErrorResponseException
)
from msrest.authentication import CognitiveServicesCredentials

# Add your Bing Autosuggest subscription key to your environment variables.
SUBSCRIPTION_KEY = os.environ['BING_AUTOSUGGEST_SUBSCRIPTION_KEY']
ENDPOINT = os.environ['BING_AUTOSUGGEST_ENDPOINT']

def autosuggest_lookup(subscription_key):
    """AutoSuggestLookup.

    This will look up a single query (Xbox) and print out name and url for first web result.
    """
    client = AutoSuggestClient(
        endpoint=ENDPOINT,
        credentials=CognitiveServicesCredentials(subscription_key)
    )

    try:
        suggestions = client.auto_suggest(
            query="Satya Nadella")  # type: Suggestions

        if suggestions.suggestion_groups:
            print("Searched for \"Satya Nadella\" and found suggestions:")
            suggestion_group = suggestions.suggestion_groups[0]  # type: SuggestionsSuggestionGroup
            for suggestion in suggestion_group.search_suggestions:  # type: SearchAction
                print("....................................")
                print(suggestion.query)
                print(suggestion.display_text)
                print(suggestion.url)
                print(suggestion.search_kind)
        else:
            print("Didn't see any suggestion..")

    except Exception as err:
        print("Encountered exception. {}".format(err))


def error(subscription_key):
    """Error.

    This triggers a bad request and shows how to read the error response.
    """

    # Breaking the subscription key on purpose
    client = AutoSuggestClient(
        endpoint=ENDPOINT,
        credentials=CognitiveServicesCredentials(subscription_key+"1")
    )

    try:
        suggestions = client.auto_suggest(
            query="Satya Nadella", market="no-ty")
    except ErrorResponseException as err:
        # The status code of the error should be a good indication of what occurred. However, if you'd like more details, you can dig into the response.
        # Please note that depending on the type of error, the response schema might be different, so you aren't guaranteed a specific error response schema.

        print("Exception occurred, status code {} with reason {}.\n".format(
            err.response.status_code, err))

        # if you'd like more descriptive information (if available)
        if err.error.errors:
            print("This is the errors I have:")
            for error in err.error.errors:
                print("Parameter \"{}\" has an invalid value \"{}\". SubCode is \"{}\". Detailed message is \"{}\"".format(
                    error.parameter, error.value, error.sub_code, error.message))
        else:
            print("There was no details on the error.")


if __name__ == "__main__":
    import sys
    import os.path
    sys.path.append(os.path.abspath(os.path.join(__file__, "..", "..")))
    from tools import execute_samples
    execute_samples(globals(), SUBSCRIPTION_KEY)
