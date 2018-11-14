from azure.cognitiveservices.vision.face import FaceClient
from msrest.authentication import CognitiveServicesCredentials
import os

SUBSCRIPTION_KEY_ENV_NAME = os.environ.get("FACE_SUBSCRIPTION_KEY")
FACE_LOCATION = os.environ.get("FACE_LOCATION", "westcentralus")





def detect_faces(face_client, image_url):
    detected_faces = face_client.face.detect_with_url(image_url, True, False, None, None, False)
    if detected_faces == None or len(detected_faces) == 0:
        raise Exception('No face detected from image {}'.format(image_url))
    print("{} faces detected from image {}".format(len(detected_faces), image_url))
    if detected_faces[0] is None:
        raise Exception("Parameter return_face_id of detect_with_stream or detect_with_url must be set to true (by default) for recognition purpose.")
    return list(detected_faces)


if __name__ == "__main__":
    face_base_url = "https://{}.api.cognitive.microsoft.com".format(FACE_LOCATION)
    face_client = FaceClient(face_base_url, CognitiveServicesCredentials(SUBSCRIPTION_KEY_ENV_NAME))
    detect_faces(face_client, "https://www.elsworth.com/wp/wp-content/uploads/2018/04/8ODT-e1524703208444-768x1024.jpg")