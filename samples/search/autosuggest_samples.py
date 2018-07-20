from azure.cognitiveservices.search.autosuggest import AutoSuggestSearchAPI
from msrest.authentication import CognitiveServicesCredentials

SUBSCRIPTION_KEY_ENV_NAME = "AUTOSUGGEST_SUBSCRIPTION_KEY"


def autosuggest_by_query(subscription_key):
    client = AutoSuggestSearchAPI(CognitiveServicesCredentials(subscription_key))

    try:
        suggestions = client.auto_suggest(query="satya n")

        if len(suggestions.suggestion_groups) > 0:
            first_group = suggestions.suggestion_groups[0]

            first_suggestion = first_group.search_suggestions[0]

            print(first_suggestion.display_text)
        else:
            print("Didn't see any data..")

    except Exception as err:
        print("Encountered exception. {}".format(err))


if __name__ == "__main__":
    import sys
    import os.path
    sys.path.append(os.path.abspath(os.path.join(__file__, "..", "..")))
    from tools import execute_samples
    execute_samples(globals(), SUBSCRIPTION_KEY_ENV_NAME)