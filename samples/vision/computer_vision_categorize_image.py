# Microsoft Azure Computer Vision API - Categorize Image

# This script categorizes two images, one local and one remote.  The
# Analyze Image method of the Computer Vision API is used in both cases;
# by default, this returns the image's category.

# Pass your Computer Vision subscription key on the command line when
# invoking this script:
#    python computer_vision_categorize_image.py <subscription key here>

# This script requires the Cognitive Services Computer Vision Python module:
#     python -m pip install azure-cognitiveservices-vision-computervision

# This script runs under Python 3.4 or later.

from azure.cognitiveservices.vision.computervision import ComputerVisionClient
from msrest.authentication import CognitiveServicesCredentials

from sys import argv    # for getting subscription key from command line

subscription_key = argv[1] if len(argv) > 1 else None
assert subscription_key, "Provide a valid Computer Vision subscription key on the command line when invoking this script"

# Make sure the endpoint given is in the same region as your subscription.
# Free trial keys are in westcentralus, so if you are using a free trial,
# you won't need to change the endpoint.

endpoint = "https://westcentralus.api.cognitive.microsoft.com"

# Paths to local and remote images.  The local image is a default Windows 10
# wallpaper; you may substitute the path of any other local image.

local_image =  r"C:\Windows\Web\Wallpaper\Theme1\img2.jpg"
remote_image = "https://raw.githubusercontent.com/Azure-Samples/cognitive-services-sample-data-files/master/ComputerVision/Images/celebrities.jpg"

# Helper function for printing categories

def format_categories(categories):
    categories.sort(key=lambda cat: -cat.score)
    return ", ".join("{} ({:.1f}%)".format(cat.name, cat.score * 100)
                     for cat in categories)

# Instantiate the client

client = ComputerVisionClient(endpoint,
                              CognitiveServicesCredentials(subscription_key))

# Get and print categories and scores of remote image

print("Analyzing", remote_image)
categories = client.analyze_image(remote_image).categories
print("Image categories:", format_categories(categories))

# Get and print categories and scores of local image

print("\nAnalyzing", local_image)
categories = client.analyze_image_in_stream(open(local_image, "rb")).categories
print("Image categories:", format_categories(categories))
