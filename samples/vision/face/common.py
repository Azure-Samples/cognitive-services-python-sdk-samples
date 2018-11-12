from azure.cognitiveservices.vision.face import FaceClient
from msrest.authentication import CognitiveServicesCredentials
import os
SUBSCRIPTION_KEY_ENV_NAME = os.environ.get("SUBSCRIPTION_KEY_ENV_NAME")
FACE_LOCATION = os.environ.get("FACE_LOCATION", "westcentralus")





def detect_faces(image_url, subscription_key):
    face_base_url = "https://{}.api.cognitive.microsoft.com".format(FACE_LOCATION)
    face_client = FaceClient(face_base_url, CognitiveServicesCredentials(subscription_key))
    detected_faces = face_client.face.detect_with_url(image_url, True, False, None, None, False)
    if detected_faces == None or len(detected_faces) == 0:
        raise Exception('No face detected from image {}'.format(image_url))
    print("{} faces detected from image {}".format(len(detected_faces), image_url))


if __name__ == "__main__":
    SUBSCRIPTION_KEY_ENV_NAME = os.environ.get("SUBSCRIPTION_KEY_ENV_NAME")
    FACE_LOCATION = os.environ.get("FACE_LOCATION", "westcentralus")
    detect_faces("https://www.elsworth.com/wp/wp-content/uploads/2018/04/8ODT-e1524703208444-768x1024.jpg", "e312068d12604dee97f59230ff788d60")