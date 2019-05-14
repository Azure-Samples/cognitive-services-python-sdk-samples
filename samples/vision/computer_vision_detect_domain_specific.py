# Microsoft Azure Computer Vision API - Detect Domain-Specific Content

# This script detects the domain-specific content in a remote image. The
# Analyze Image By domain method of the Computer Vision API is used.
# Available domains are landscapes and celebrities.

# Pass your Computer Vision subscription key on the command line when
# invoking this script:
#    python computer_vision_detect_domain_specific.py <subscription key here>

# This script requires the Cognitive Services Computer Vision Python module:
#     python -m pip install azure-cognitiveservices-vision-computervision

# This script runs under Python 3.4 or later.

from azure.cognitiveservices.vision.computervision import ComputerVisionClient
from msrest.authentication import CognitiveServicesCredentials

from os import environ  # for getting subscription key from environment

KEY_VAR = "AZURE_COMPUTER_VISION_KEY"

subscription_key = environ.get(KEY_VAR)
assert subscription_key, "Set environment variable {} to your Computer Vision subscription key.".format(KEY_VAR)

# Make sure the endpoint given is in the same region as your subscription.
# Free trial keys are in westcentralus, so if you are using a free trial,
# you won't need to change the endpoint.

endpoint = "https://westcentralus.api.cognitive.microsoft.com"

# Path to remote image

remote_image = "https://raw.githubusercontent.com/Azure-Samples/cognitive-services-sample-data-files/master/ComputerVision/Images/celebrities.jpg"

# Helper function to print celebrities
def print_celebrities(celebs):
    if not celebs:
        print("No celebrities found")
        return
    print("Found", len(celebs), "celebrity" if len(celebs) == 1 else "celebrities")
    for celeb in celebs:
        print("    {0} ({1:.1f}%)".format(celeb["name"], celeb["confidence"] * 100))

# Instantiate the client

client = ComputerVisionClient(endpoint,
                              CognitiveServicesCredentials(subscription_key))

# Get and print celebrities found in remote image

print("Analyzing", remote_image)
celebs = client.analyze_image_by_domain("celebrities", remote_image).result["celebrities"]
print_celebrities(celebs)

# You can find landmarks or celebrities in local files as well, e.g.:
# analyze_image_by_domain_in_stream("celebrities", open(local_image, "rb"))
