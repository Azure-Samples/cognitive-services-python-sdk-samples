# Microsoft Azure Computer Vision API - Detect Domain-Specific Content
#
# This script detects the domain-specific content in a remote image. The
# Analyze Image By domain method of the Computer Vision API is used.
# Available domains are landscapes and celebrities.
#
# This script requires the Cognitive Services Computer Vision Python module:
#     python -m pip install azure-cognitiveservices-vision-computervision
#
# This script runs under Python 3.4 or later.

from azure.cognitiveservices.vision.computervision import ComputerVisionClient
from msrest.authentication import CognitiveServicesCredentials

# Add your subscription key below and make sure the endpoint given is in
# the same region as the subscription.  Free trial keys are in westcentralus,
# so if you are using a free trial, you won't need to change the endpoint.

subscription_key = ""
assert subscription_key, "Provide a valid Computer Vision subscription key"

endpoint = "https://westcentralus.api.cognitive.microsoft.com"

# Path to remote image

remote_image = "https://raw.githubusercontent.com/Azure-Samples/cognitive-services-sample-data-files/master/ComputerVision/Images/celebrities.jpg"

# Helper function to print celebrities
def print_celebrities(celebs, ):
    if not celebs:
        print("No celebrities found")
        return
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
