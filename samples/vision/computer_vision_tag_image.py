# Microsoft Azure Computer Vision API - Tag Images

# This script tags two images, one local and one remote.  The Analyze Image
# method of the Computer Vision API is used in both cases, specifying that
# we want tags related to the image.

# Pass your Computer Vision subscription key on the command line when
# invoking this script:
#    python computer_vision_tag_images.py <subscription key here>

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

# Paths to local and remote images.  The local image is a default Windows 10
# wallpaper image; you may substitute the path of any other local image.

local_image =  r"C:\Windows\Web\Wallpaper\Theme1\img1.jpg"
remote_image = "https://raw.githubusercontent.com/Azure-Samples/cognitive-services-python-sdk-samples/master/samples/vision/images/house.jpg"

# Instantiate the client

client = ComputerVisionClient(endpoint,
                              CognitiveServicesCredentials(subscription_key))

# Get and print tags of remote image

print("Analyzing", remote_image)
tags = client.analyze_image(remote_image, visual_features=["tags"]).tags
print("Tags:", ", ".join(tag.name for tag in tags))

# Get and print tags of local image

print("\nAnalyzing", local_image)
tags = client.analyze_image_in_stream(open(local_image, "rb"),
                                      visual_features=["tags"]).tags
print("Tags:", ", ".join(tag.name for tag in tags))
