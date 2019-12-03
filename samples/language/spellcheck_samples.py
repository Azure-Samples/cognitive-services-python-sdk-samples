from azure.cognitiveservices.language.spellcheck import SpellCheckAPI
from msrest.authentication import CognitiveServicesCredentials

# Add your Bing Spell Check subscription key to your environment variables.
SUBSCRIPTION_KEY = os.environ['BING_SPELL_CHECK_SUBSCRIPTION_KEY']


def spellcheck(subscription_key):
    """SpellCheck.

    This will do a search for misspelled query and parse the response.
    """
    client = SpellCheckAPI(CognitiveServicesCredentials(subscription_key))

    try:
        result = client.spell_checker("Bill Gatas", mode="proof")
        print("Correction for Query# \"bill gatas\"")

        if result.flagged_tokens:
            first_spellcheck_result = result.flagged_tokens[0]

            print("SpellCheck result count: {}".format(
                len(result.flagged_tokens)))
            print("First SpellCheck token: {}".format(
                first_spellcheck_result.token))
            print("First SpellCheck type: {}".format(
                first_spellcheck_result.type))
            print("First SpellCheck suggestion count: {}".format(
                len(first_spellcheck_result.suggestions)))

            if first_spellcheck_result.suggestions:
                first_suggestion = first_spellcheck_result.suggestions[0]
                print("First SpellCheck suggestion score: {}".format(
                    first_suggestion.score))
                print("First SpellCheck suggestion: {}".format(
                    first_suggestion.suggestion))
            else:
                print("Couldn't get any Spell check results!")

        else:
            print("Didn't see any SpellCheck results..")

    except Exception as err:
        print("Encountered exception. {}".format(err))


if __name__ == "__main__":
    import sys, os.path
    sys.path.append(os.path.abspath(os.path.join(__file__, "..", "..", "..")))    
    from samples.tools import execute_samples
    execute_samples(globals(), SUBSCRIPTION_KEY_ENV_NAME)
