# Microsoft Azure Language Understanding (LUIS) - Build App
#
# This script builds a LUIS app, entities, and intents using the Python
# LUIS SDK.  A separate sample trains and publishes the app.
#
# This script requires the Cognitive Services LUIS Python module:
#     python -m pip install azure-cognitiveservices-language-luis
#
# This script runs under Python 3.4 or later.

# Be sure you understand how LUIS models work.  In particular, know what
# intents, entities, and utterances are, and how they work together in the
# context of a LUIS app. See the following:
#
# https://www.luis.ai/welcome
# https://docs.microsoft.com/azure/cognitive-services/luis/luis-concept-intent
# https://docs.microsoft.com/azure/cognitive-services/luis/luis-concept-entity-types
# https://docs.microsoft.com/azure/cognitive-services/luis/luis-concept-utterance

from azure.cognitiveservices.language.luis.authoring import LUISAuthoringClient
from msrest.authentication import CognitiveServicesCredentials

from datetime import datetime

# Add your LUIS authoring key below (from the Settings page in the LUIS portal)
# and make sure the endpoint given is in the correct region (e.g. westus).

authoring_key = ""
assert authoring_key, "Provide a valid LUIS authoring key"

authoring_endpoint = "https://westus.api.cognitive.microsoft.com"

# Provide a LUIS app ID here to work with an existing app.
# If app_id is left empty, a new app is created.
app_id = ""

# Instantiate a LUIS client
client = LUISAuthoringClient(authoring_endpoint,
             CognitiveServicesCredentials(authoring_key))

# Create a new LUIS app if app ID was not specified
if not app_id:
    app_name    = "Contoso {}".format(datetime.now())
    app_desc    = "Flight booking app built with LUIS Python SDK."
    app_version = "0.1"
    app_locale  = "en-us"

    app_id = client.apps.add(dict(name=app_name,
                                  initial_version_id=app_version,
                                  description=app_desc,
                                  culture=app_locale))

    print("Created LUIS app {}\n    with ID {}".format(app_name, app_id))
    print("Make a note of the ID to use this app with other samples.\n")
else:                               # get info on existing app
    app_info    = client.apps.get(app_id)
    app_name    = app_info.name
    app_desc    = app_info.description
    app_version = app_info.active_version
    app_locale  = app_info.culture
    print("Working on LUIS app", app_name, app_version)

# Declare entities:
#
#   Destination - A simple entity that will hold the flight destination
#
#   Class - A hierarchical entity that will hold the flight class
#           (First, Business, or Economy)
#
#   Flight - A composite entity represeting the flight (including
#               class and destination)
#
# Creating an entity (or other LUIS object) returns its ID.
# We don't use IDs further in this script, so we don't keep the return value.

client.model.add_entity(app_id, app_version, "Destination")

client.model.add_hierarchical_entity(app_id, app_version, name="Class",
                                     children=["First", "Business", "Economy"])

client.model.add_composite_entity(app_id, app_version, name="Flight",
                                  children=["Class", "Destination"])

print("Entities Destination, Class, Flight created.")

# Declare an intent, FindFlights, that recognizes a user's Flight request
# Creating an intent returns its ID, which we don't need, so don't keep.

client.model.add_intent(app_id, app_version, "FindFlights")

print("Intent FindFlights added.")

# Add example utterances for the intent.  Each utterance includes labels
# that identify the entities within each utterance by index.  LUIS learns
# how to find entities within user utterances from the provided examples.
#
# Example utterance: "find flights in economy to Madrid"
# Labels: Flight -> "economy to Madrid" (composite of Destination and Class)
#         Destination -> "Madrid"
#         Class -> "economy"

# Helper function for creating the utterance data structure.
def utterance(intent, utterance, *labels):
    """Add an example LUIS utterance from utterance text and a list of
       labels.  Each label is a 2-tuple containing a label name and the
       text within the utterance that represents that label.

       Utterances apply to a specific intent, which must be specified."""

    text = utterance.lower()

    def label(name, value):
        value = value.lower()
        start = text.index(value)
        return dict(entity_name=name, start_char_index=start,
                    end_char_index=start + len(value))

    return dict(text=text, intent_name=intent,
                entity_labels=[label(n, v) for (n, v) in labels])

# Now define the utterances
utterances = [utterance("FindFlights", "find flights in economy to Madrid",
                        ("Flight", "economy to Madrid"),
                        ("Destination", "Madrid"),
                        ("Class", "economy")),

              utterance("FindFlights", "find flights to London in first class",
                        ("Flight", "London in first class"),
                        ("Destination", "London"),
                        ("Class", "first"))]

# Add the utterances in batch. You may add any number of example utterances
# for any number of intents in one call.
client.examples.batch(app_id, app_version, utterances)

print("{} example utterance(s) added.".format(len(utterances)))
print("\nYou can now train and publish your app (see train_publish.py).")
