import os.path

from azure.cognitiveservices.vision.face import FaceClient
from azure.cognitiveservices.vision.face.models import FaceAttributeType, Gender
from msrest.authentication import CognitiveServicesCredentials

SUBSCRIPTION_KEY_ENV_NAME = "FACE_SUBSCRIPTION_KEY"
FACE_LOCATION = os.environ.get("FACE_LOCATION", "westcentralus")

IMAGES_FOLDER = os.path.join(os.path.dirname(os.path.realpath(__file__)), "images", "Face")

def face_detect(subscription_key):
    """ImageAnalysisInStream.

    This will analysis an image from a stream and return all available features.
    """
    face_base_url = "https://{}.api.cognitive.microsoft.com".format(FACE_LOCATION)
    face_client = FaceClient(face_base_url, CognitiveServicesCredentials(subscription_key))

    faces = [jpgfile for jpgfile in os.listdir(IMAGES_FOLDER) if jpgfile.startswith("Family1")]
    faces_ids = []

    for face in faces:
        with open(os.path.join(IMAGES_FOLDER, face), "rb") as face_fd:
            # result type: azure.cognitiveservices.vision.face.models.DetectedFace
            result = face_client.face.detect_with_stream(
                face_fd,
                # You can use enum from FaceAttributeType, or direct string
                return_face_attributes=[
                    FaceAttributeType.age,  # Could have been the string 'age'
                    'gender',
                    'headPose',
                    'smile',
                    'facialHair',
                    'glasses',
                    'emotion',
                    'hair',
                    'makeup',
                    'occlusion',
                    'accessories',
                    'blur',
                    'exposure',
                    'noise'
                ]
            )

        if not result:
            print("Unable to detect any face in {}".format(face))

        detected_face = result[0]
        faces_ids.append(detected_face.face_id)

        print("\nImage {}".format(face))
        print("Detected age: {}".format(detected_face.face_attributes.age))
        print("Detected gender: {}".format(detected_face.face_attributes.gender))
        print("Detected emotion: {}".format(detected_face.face_attributes.emotion.happiness))
    print("\n")

    # Verification example for faces of the same person.
    verify_result = face_client.face.verify_face_to_face(
        faces_ids[0],
        faces_ids[1],
    )
    if verify_result.is_identical:
        print("Faces from {} & {} are of the same (Positive) person, similarity confidence: {}.".format(faces[0], faces[1], verify_result.confidence))
    else:
        print("Faces from {} & {} are of different (Negative) persons, similarity confidence: {}.".format(faces[0], faces[1], verify_result.confidence))

    # Verification example for faces of different persons.
    verify_result = face_client.face.verify_face_to_face(
        faces_ids[1],
        faces_ids[2],
    )
    if verify_result.is_identical:
        print("Faces from {} & {} are of the same (Positive) person, similarity confidence: {}.".format(faces[1], faces[2], verify_result.confidence))
    else:
        print("Faces from {} & {} are of different (Negative) persons, similarity confidence: {}.".format(faces[1], faces[2], verify_result.confidence))

if __name__ == "__main__":
    import sys, os.path
    sys.path.append(os.path.abspath(os.path.join(__file__, "..", "..")))
    from tools import execute_samples
    execute_samples(globals(), SUBSCRIPTION_KEY_ENV_NAME)