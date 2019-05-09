# Microsoft Azure Computer Vision API - Detect Color Scheme

# This script detects the color schemes in two images, one local and one
# remote.  The Analyze Image method of the Computer Vision API is used
# in both cases, specifying that we want the image's color scheme.

# Pass your Computer Vision subscription key on the command line when
# invoking this script:
#    python computer_vision_detect_color_scheme.py <subscription key here>

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

local_image =  r"C:\Windows\Web\Wallpaper\Theme2\img11.jpg"
remote_image = "https://raw.githubusercontent.com/Azure-Samples/cognitive-services-sample-data-files/master/ComputerVision/Images/celebrities.jpg"

# Helper function for printing color scheme

def print_color_scheme(colors):
    print("\nImage is in", ("color", "black and white")[colors.is_bw_img])
    print("Dominant colors:", ", ".join(colors.dominant_colors))
    print("Dominant foreground color:", colors.dominant_color_foreground)
    print("Dominant background color:", colors.dominant_color_background)
    print("Suggested accent color: #{}".format(colors.accent_color))
    
# Instantiate the client

client = ComputerVisionClient(endpoint,
                              CognitiveServicesCredentials(subscription_key))

# Get and print color scheme of remote image

print("Analyzing", remote_image)
colors = client.analyze_image(remote_image, visual_features=["color"]).color
print_color_scheme(colors)

# Get and print color scheme of local image
print("\nAnalyzing", local_image)
colors = client.analyze_image_in_stream(open(local_image, "rb"),
                                            visual_features=["color"]).color
print_color_scheme(colors)
