# Microsoft Azure Computer Vision API - Describe Image
#
# This script retrieves a human-readable description of two images, one local
# and one remote.
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

# Paths to local and remote images.  The local image is a default Windows 10
# wallpaper; you may substitute the path of any other local image.

local_image =  r"C:\Windows\Web\Wallpaper\Theme2\img10.jpg"
remote_image = "https://raw.githubusercontent.com/Azure-Samples/cognitive-services-sample-data-files/master/ComputerVision/Images/objects.jpg"

# Instantiate the client

client = ComputerVisionClient(endpoint, CognitiveServicesCredentials(subscription_key))

# Get and print description of remote image

print("Analyzing", remote_image)
caption = client.describe_image(remote_image).captions[0]
print("This may be {} ({:.1f}% confidence)".format(caption.text,
                                                   caption.confidence * 100))

# Get and print description of local image

print("\nAnalyzing", local_image)
caption = client.describe_image_in_stream(open(local_image, "rb")).captions[0]
print("This may be {} ({:.1f}% confidence)".format(caption.text,
                                                   caption.confidence * 100))
