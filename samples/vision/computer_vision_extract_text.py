from azure.cognitiveservices.vision.computervision import ComputerVisionClient
from msrest.authentication import CognitiveServicesCredentials
from azure.cognitiveservices.vision.computervision.models import ReadOperationResult, OperationStatusCodes
import time

'''
References:
    Quickstart: https://docs.microsoft.com/en-us/azure/cognitive-services/computer-vision/quickstarts-sdk/python-sdk
    SDK: https://docs.microsoft.com/en-us/python/api/overview/azure/cognitiveservices/computervision?view=azure-python
'''

# Replace with your endpoint and key from the Azure portal
endpoint = '<ADD ENDPOINT HERE>'
key = '<ADD COMPUTER VISION SUBSCRIPTION KEY HERE>'

# Alternatively, uncomment and get endpoint/key from environment variables
'''
import os
endpoint = os.environ['COMPUTER_VISION_ENDPOINT']
key = os.environ['COMPUTER_VISION_SUBSCRIPTION_KEY']
'''

# Set credentials
credentials = CognitiveServicesCredentials(key)

# Create client
client = ComputerVisionClient(endpoint, credentials)

# change this URL to reflect the image that you would like to test.
url = "https://azurecomcdn.azureedge.net/cvt-181c82bceabc9fab9ec6f3dca486738800e04b45a0b3c1268609c94f4d67173a/images/shared/cognitive-services-demos/analyze-image/analyze-6-thumbnail.jpg"
# image_path = "images/computer_vision_ocr.png"
lang = 'en'
raw = True
custom_headers = None

# Read an image from a url
rawHttpResponse = client.read(url, language=lang, custom_headers=custom_headers, raw=raw)

# Uncomment the following code and comment out line 37 to read from image stream
# with open(image_path, "rb") as image_stream:
#     rawHttpResponse = client.read_in_stream(
#         image=image_stream, language=lang,
#         # Raw will return the raw response which can be used to find the operation_id
#         raw=True
#     )

# Get ID from returned headers
operationLocation = rawHttpResponse.headers["Operation-Location"]
operationId = operationLocation.split('/')[-1]

# SDK call
while True:
    result = client.get_read_result(operationId)
    if result.status not in [OperationStatusCodes.not_started, OperationStatusCodes.running]:
        break
    time.sleep(1)

# Get data: displays text captured and its bounding box (position in the image)

if result.status == OperationStatusCodes.succeeded:
    for read_result in result.analyze_result.read_results:
        for line in read_result.lines:
            print(line.text)
            print(line.bounding_box)