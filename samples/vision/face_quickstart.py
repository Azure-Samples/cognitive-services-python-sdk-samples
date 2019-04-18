# Microsoft Azure Face API - Python Quickstart
#
# This script has two parts:
#   1. Recognize faces in a sample image and print information about each face
#   2. Draw a red rectangle around each face in the image
#
# This script requires the Cognitive Services Face API Python module:
#     python -m pip install azure-cognitiveservices-vision-face
#
# Drawing rectangles around faces requires the Pillow and Requests modules:
#     python -m pip install pillow
#     python -m pip install requests
#
# This script runs under Python 3.4 or later.

from azure.cognitiveservices.vision.face import FaceClient
from msrest.authentication import CognitiveServicesCredentials

# Add your subscription key below and make sure the endpoint given is in
# the same region as the subscription.  Free trial keys are in westcentralus,
# so if you are using a free trial, you won't need to change the endpoint.

subscription_key = ""
assert subscription_key, "Provide a valid Face subscription key"

endpoint = "https://westcentralus.api.cognitive.microsoft.com"

# Function to return bounding box given a face_rectangle from Face result
def get_rect(r):
    return r.left, r.top, r.left + r.width, r.top + r.height

# --------------------------------------------------------------------
# Find faces in image specified by URL and print a report on each face

client = FaceClient(endpoint, CognitiveServicesCredentials(subscription_key))

# You can use this example JPG or replace the URL below with your own
image_url = "https://raw.githubusercontent.com/Microsoft/Cognitive-Face-Windows/master/Data/detection1.jpg"

# Detect the faces in the image(s)
faces = client.face.detect_with_url(image_url)
print(len(faces), "face{} found in {}".format("s" * (len(faces) != 1), image_url))

# Print a report for each face
for i, face in enumerate(faces, 1):

    # get coordinates of face
    rect = face.face_rectangle
    top, left, bottom, right = get_rect(rect)

    print()
    print("Face", i)
    print("    ID:", face.face_id)
    print("    Rectangle: ({}, {}) to ({}, {}); height: {} width: {}".format(
        top, left, bottom, right, rect.height, rect.width))
    print("    Landmarks:", face.face_landmarks)
    print("    Attributes", face.face_attributes)

# -------------------------------------------------------------------
# Draw a rectangle around each face, then show the image

import requests
from PIL import Image, ImageDraw

# First, we need our own copy of the image
image = Image.open(requests.get(image_url, stream=True).raw)
draw = ImageDraw.Draw(image)

for face in faces:
    draw.rectangle(get_rect(face.face_rectangle), outline="red")

# Show image with face rects using your default image viewer
image.show()

# If you haven't yet chosen a default viewer, you may need to run
# this script again after choosing one in order to see the result
