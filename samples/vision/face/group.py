from azure.cognitiveservices.vision.face import FaceClient
from msrest.authentication import CognitiveServicesCredentials
from samples.vision.face.common import detect_faces
import os

SUBSCRIPTION_KEY_ENV_NAME = "FACE_SUBSCRIPTION_KEY"
FACE_LOCATION = os.environ.get("FACE_LOCATION", "westcentralus")

def group_run(face_base_url, subscription_key):
    print("Sample of grouping faces.")

    face_client = FaceClient(face_base_url, CognitiveServicesCredentials(subscription_key))
    image_url_prefix = "https://csdx.blob.core.windows.net/resources/Face/Images/"
    image_file_names = ["Family1-Dad1.jpg",
                               "Family1-Daughter1.jpg",
                               "Family1-Mom1.jpg",
                               "Family1-Son1.jpg",
                               "Family2-Lady1.jpg",
                               "Family2-Man1.jpg",
                               "Family3-Lady1.jpg",
                               "Family3-Man1.jpg"]
    source_image_file_name = "findsimilar.jpg"

    faces = {}
    face_ids = []

    for image_file_name in image_file_names:
        # Detect faces from target image url.
        detected_faces = detect_faces(face_client, image_url_prefix + image_file_name)

        # Add detected face id to face_ids and faces.
        face_ids.append(detected_faces[0].face_id)
        faces[str(detected_faces[0].face_id)] = image_file_name

    # Call grouping, the grouping result is a group collection, each group contains similar faces.
    group_result = face_client.face.group(face_ids)

    # Face groups containing faces that are similar.
    for i in range(len(group_result.groups)):
        to_print = "Found face group {}: ".format(i + 1)
        for face_id in group_result.groups[i]:
            to_print = to_print + "{}".format(str(faces[str(face_id)]))
        print(to_print + ".")

    # Messy group contains all faces which are not similar to any other faces.
    if len(group_result.messy_group) > 0:
        to_print = "Found messy face group: "
        for face_id in group_result.messy_group:
            to_print = to_print + str(faces[face_id]) + " "
        print(to_print + ".")

    print("")


if __name__ == "__main__":
    face_base_url = "https://{}.api.cognitive.microsoft.com".format(FACE_LOCATION)
    group_run(face_base_url, "e312068d12604dee97f59230ff788d60")
