# Microsoft Azure Language Understanding (LUIS) - Call Endpoint
#
# This script sends a sample query to a publicly-available home automation
# app using the LUIS Python SDK.  This app already exists and is accessible
# using your LUIS authoring key.
#
# This script requires the Cognitive Services LUIS Python module:
#     python -m pip install azure-cognitiveservices-language-luis
#
# This script runs under Python 3.4 or later.

from azure.cognitiveservices.language.luis.runtime import LUISRuntimeClient
from msrest.authentication import CognitiveServicesCredentials

import sys

# Use hard-coded sample utterance, or get it from the command line
utterance = "Turn on the left light"

if len(sys.argv) > 1:           # grab all command line args as utterance
    utterance = " ".join(sys.argv[1:])

# Add your LUIS endpoint key below.  For demonstration purposes, you may
# use your LUIS authoring key (from the Settings page in the LUIS portal).
endpoint_key = "46a5a28da55f495b9b91d941cd4d6973"
assert endpoint_key, "Provide a valid LUIS authoring or endpoint key"

# The values below are correct for the publicly-available app.  Change
# them if you are adapting this code for use with a different LUIS app.
app_endpoint = "https://westus.api.cognitive.microsoft.com/"
app_id       = "df67dcdb-c37d-46af-88e1-8b97951ca1c2"

assert app_id, "Provide a valid LUIS app ID"

# Instantiate a LUIS client
client = LUISRuntimeClient(app_endpoint,
                           CognitiveServicesCredentials(endpoint_key))

# Perform the query
result = client.prediction.resolve(app_id, utterance)
intent = result.top_scoring_intent

# Print some results: top intent, other entities 
print("For query:", utterance)
print("Detected intent: {} (score: {:.2f})".format(intent.intent, intent.score))

if result.intents and len(result.intents) > 1:
    print("Other possible intents:", ", ".join(i.intent for i in result.intents[1:]))

print("With entities:", ", ".join("{}: {}".format(e.type, e.entity)
                                  for e in result.entities) or "None")

if result.composite_entities:
    print("Composite entities:")
    for entity in result.composite_entities:
        print("    {}: {}; {}", entity.parent_type, entity.value,
              ", ".join("{}: {}".format(e.type, e.value) for e in entity.children))
