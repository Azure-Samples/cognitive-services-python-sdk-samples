# Microsoft Azure Language Understanding (LUIS) - Train and Publish
#
# After you build a LUIS app, or modify its model, you must build and
# publish it to use it.  This script trains and publishes a LUIS app.
#
# This script requires the Cognitive Services LUIS Python module:
#     python -m pip install azure-cognitiveservices-language-luis
#
# This script runs under Python 3.4 or later.

from azure.cognitiveservices.language.luis.authoring import LUISAuthoringClient
from msrest.authentication import CognitiveServicesCredentials

from time import sleep

# Add your LUIS authoring key below (from the Settings page in the LUIS portal)
# and make sure the endpoint given is in the correct region (e.g. westus).

authoring_key = ""
assert authoring_key, "Provide a valid LUIS authoring key"

authoring_endpoint = "https://westus.api.cognitive.microsoft.com"

# Provide your LUIS app ID, version, locale, and publishing region here.
app_id      = ""
app_version = "0.1"
app_locale  = "en-us"
app_region  = "westus"      # region where the app will be published

assert app_id, "Provide a valid LUIS app ID"

# Instantiate a LUIS client
client = LUISAuthoringClient(authoring_endpoint,
             CognitiveServicesCredentials(authoring_key))

# Train the app and wait until training completes
client.train.train_version(app_id, app_version)

while any(m.details.status not in ("UpToDate", "Success")
          for m in client.train.get_status(app_id, app_version)): sleep(1)

print("Trained your app. You can now test it in the LUIS portal.")

# Publish the app and get its endpoint
app_endpoint = client.apps.publish(app_id, dict(version_id=app_version,
                is_staging=False, region=app_region)).endpoint_url

print("Published your app. Its endpoint is:\n")
print(app_endpoint)
