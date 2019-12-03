import os.path
from pprint import pprint
import time

from azure.cognitiveservices.vision.contentmoderator import ContentModeratorClient
from azure.cognitiveservices.vision.contentmoderator.models import (
    TermList,
    Terms,
    TermsData,
    RefreshIndex,
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


def terms_lists(subscription_key):
    """TermsList.

    This will screen text using a term list.
    """

    client = ContentModeratorClient(
        endpoint=os.environ['CONTENT_MODERATOR_ENDPOINT'], # Add your Content Moderator endpoint to your environment variables.
        credentials=CognitiveServicesCredentials(subscription_key)
    )

    #
    # Create list
    #

    print("\nCreating list")
    custom_list = client.list_management_term_lists.create(
        content_type="application/json",
        body={
            "name": "Term list name",
            "description": "Term list description",
        }
    )
    print("List created:")
    assert isinstance(custom_list, TermList)
    pprint(custom_list.as_dict())
    list_id = custom_list.id

    #
    # Update list details
    #
    print("\nUpdating details for list {}".format(list_id))
    updated_list = client.list_management_term_lists.update(
        list_id=list_id,
        content_type="application/json",
        body={
            "name": "New name",
            "description": "New description"
        }
    )
    assert isinstance(updated_list, TermList)
    pprint(updated_list.as_dict())

    #
    # Add terms
    #
    print("\nAdding terms to list {}".format(list_id))
    client.list_management_term.add_term(
        list_id=list_id,
        term="term1",
        language="eng"
    )
    client.list_management_term.add_term(
        list_id=list_id,
        term="term2",
        language="eng"
    )

    #
    # Get all terms ids
    #
    print("\nGetting all term IDs for list {}".format(list_id))
    terms = client.list_management_term.get_all_terms(
        list_id=list_id, language="eng")
    assert isinstance(terms, Terms)
    terms_data = terms.data
    assert isinstance(terms_data, TermsData)
    pprint(terms_data.as_dict())

    #
    # Refresh the index
    #
    print("\nRefreshing the search index for list {}".format(list_id))
    refresh_index = client.list_management_term_lists.refresh_index_method(
        list_id=list_id, language="eng")
    assert isinstance(refresh_index, RefreshIndex)
    pprint(refresh_index.as_dict())

    print("\nWaiting {} minutes to allow the server time to propagate the index changes.".format(
        LATENCY_DELAY))
    time.sleep(LATENCY_DELAY * 60)

    #
    # Screen text
    #
    text = 'This text contains the terms "term1" and "term2".'
    print('\nScreening text "{}" using term list {}'.format(text, list_id))
    with open(os.path.join(TEXT_FOLDER, 'content_moderator_term_list.txt'), "rb") as text_fd:
        screen = client.text_moderation.screen_text(
            text_content_type="text/plain",
            text_content=text_fd,
            language="eng",
            autocorrect=False,
            pii=False,
            list_id=list_id
        )
        assert isinstance(screen, Screen)
        pprint(screen.as_dict())

    #
    # Remove terms
    #
    term_to_remove = "term1"
    print("\nRemove term {} from list {}".format(term_to_remove, list_id))
    client.list_management_term.delete_term(
        list_id=list_id,
        term=term_to_remove,
        language="eng"
    )

    #
    # Refresh the index
    #
    print("\nRefreshing the search index for list {}".format(list_id))
    refresh_index = client.list_management_term_lists.refresh_index_method(
        list_id=list_id, language="eng")
    assert isinstance(refresh_index, RefreshIndex)
    pprint(refresh_index.as_dict())

    print("\nWaiting {} minutes to allow the server time to propagate the index changes.".format(
        LATENCY_DELAY))
    time.sleep(LATENCY_DELAY * 60)

    #
    # Re-Screen text
    #
    with open(os.path.join(TEXT_FOLDER, 'content_moderator_term_list.txt'), "rb") as text_fd:
        print('\nScreening text "{}" using term list {}'.format(text, list_id))
        screen = client.text_moderation.screen_text(
            text_content_type="text/plain",
            text_content=text_fd,
            language="eng",
            autocorrect=False,
            pii=False,
            list_id=list_id
        )
        assert isinstance(screen, Screen)
        pprint(screen.as_dict())

    #
    # Delete all terms
    #
    print("\nDelete all terms in the image list {}".format(list_id))
    client.list_management_term.delete_all_terms(
        list_id=list_id, language="eng")

    #
    # Delete list
    #
    print("\nDelete the term list {}".format(list_id))
    client.list_management_term_lists.delete(list_id=list_id)


if __name__ == "__main__":
    import sys, os.path
    sys.path.append(os.path.abspath(os.path.join(__file__, "..", "..", "..")))
    from samples.tools import execute_samples
    execute_samples(globals(), SUBSCRIPTION_KEY_ENV_NAME)
