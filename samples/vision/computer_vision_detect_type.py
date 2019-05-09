# Microsoft Azure Computer Vision API - Detect Image Type

# This script detects the type of two images, one local and one
# remote.  The Analyze Image method of the Computer Vision API is used
# in both cases, specifying that we want the image's type.

# Pass your Computer Vision subscription key on the command line when
# invoking this script:
#    python computer_vision_detect_type.py <subscription key here>


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
# wallpaper image; you may substitute the path of any other local image.

local_image =  r"C:\Windows\Web\Wallpaper\Theme2\img11.jpg"
remote_image = "https://raw.githubusercontent.com/Azure-Samples/cognitive-services-python-sdk-samples/master/samples/vision/images/make_things_happen.jpg"

# Helper function to print image type
def describe_type(img_type):
    if img_type.clip_art_type > img_type.line_drawing_type and img_type.clip_art_type:
        return "clip art"
    elif img_type.line_drawing_type > img_type.clip_art_type and img_type.line_drawing_type:
        return "a line drawing"
    return "a photograph"

# Instantiate the client

client = ComputerVisionClient(endpoint,
                              CognitiveServicesCredentials(subscription_key))

# Get and print categories and scores of remote image

print("Analyzing", remote_image)
img_type = client.analyze_image(remote_image, visual_features=["imagetype"]).image_type
print("Image is", describe_type(img_type))

# Get and print categories and scores of local image
print("\nAnalyzing", local_image)
img_type = client.analyze_image_in_stream(open(local_image, "rb"),
                                            visual_features=["imagetype"]).image_type
print("Image is", describe_type(img_type))

