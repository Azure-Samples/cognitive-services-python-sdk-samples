from azure.cognitiveservices.vision.face import FaceClient
from azure.cognitiveservices.vision.face.models import TrainingStatusType
from msrest.authentication import CognitiveServicesCredentials
from samples.vision.face.common import detect_faces

import os
import uuid
import time

SUBSCRIPTION_KEY_ENV_NAME = os.environ.get("FACE_SUBSCRIPTION_KEY")
FACE_LOCATION = os.environ.get("FACE_LOCATION", "westcentralus")

def find_similar_in_face_ids(face_base_url, subscription_key):
    print("Sample of finding similar faces in face ids.")
    face_client = FaceClient(face_base_url, CognitiveServicesCredentials(subscription_key))
    image_url_prefix = "https://csdx.blob.core.windows.net/resources/Face/Images/"
    target_image_file_names = ["Family1-Dad1.jpg",
                                "Family1-Daughter1.jpg",
                                "Family1-Mom1.jpg",
                                "Family1-Son1.jpg",
                                "Family2-Lady1.jpg",
                                "Family2-Man1.jpg",
                                "Family3-Lady1.jpg",
                                "Family3-Man1.jpg"]

    source_image_file_name = "findsimilar.jpg"
    target_face_ids = []

    for target_image_file_name in target_image_file_names:
        # Detect faces from target image url.
        faces = detect_faces(face_client, image_url_prefix + target_image_file_name)
        # Add detected face id to target_face_ids
        target_face_ids.append(faces[0].face_id)
    # Detect faces from source image url.
    detected_faces = detect_faces(face_client, image_url_prefix + source_image_file_name)
    # Find similar example of face id to face ids.
    similar_results = face_client.face.find_similar(detected_faces[0].face_id, None, None, target_face_ids)
    if len(similar_results) == 0:
        print("No similar faces to {}.".format(source_image_file_name))
    for similar_result in similar_results:
        print("Faces from {} & {} are similar with confidence: {}.".format(source_image_file_name, similar_result.face_id, similar_result.confidence))
    print("")

def find_similar_in_face_list(face_base_url, subscription_key):
    print("Sample of finding similar faces in face list.")
    face_client = FaceClient(face_base_url, CognitiveServicesCredentials(subscription_key))
    image_url_prefix = "https://csdx.blob.core.windows.net/resources/Face/Images/"
    target_image_file_names = ["Family1-Dad1.jpg",
                               "Family1-Daughter1.jpg",
                               "Family1-Mom1.jpg",
                               "Family1-Son1.jpg",
                               "Family2-Lady1.jpg",
                               "Family2-Man1.jpg",
                               "Family3-Lady1.jpg",
                               "Family3-Man1.jpg"]

    source_image_file_name = "findsimilar.jpg"
    # Create a face list.
    face_list_id = str(uuid.uuid4())
    print("Create face list {}.".format(face_list_id))
    face_client.face_list.create(face_list_id, "face list for find_similar_in_face_list sample", "face list for find_similar_in_face_list sample")

    for target_image_file_name in target_image_file_names:
        # Add face to face list.
        faces = face_client.face_list.add_face_from_url(face_list_id, image_url_prefix + target_image_file_name, target_image_file_name)
        if faces is None:
            raise Exception("No face detected from image {}".format(target_image_file_name))
        print("Face from image {} is successfully added to the face list.".format(target_image_file_name))
    # Get persisted faces from the face list.
    persisted_faces = list(face_client.face_list.get(face_list_id).persisted_faces)
    if len(persisted_faces) == 0:
        raise Exception("No persisted face in face list {}".format(face_list_id))

    # Detect faces from source image url.
    detected_faces = detect_faces(face_client, image_url_prefix + source_image_file_name)

    # Find similar example of face id to face list.
    similar_results = face_client.face.find_similar(detected_faces[0].face_id, face_list_id)
    for similar_result in similar_results:
        persisted_face = [pf for pf in persisted_faces if pf.persisted_face_id == similar_result.persisted_face_id][0]
        if persisted_face is None:
            print("persisted face not found in similar result.")
            continue
        print("Faces from {} & {} are similar with confidence: {}.".format(source_image_file_name, persisted_face.user_data, similar_result.confidence))

    # Delete the face list.
    face_client.face_list.delete(face_list_id)
    print("Delete face list {}.".format(face_list_id))
    print("")

def find_similar_in_large_face_list(face_base_url, subscription_key):
    print("Sample of finding similar faces in large face list.")
    face_client = FaceClient(face_base_url, CognitiveServicesCredentials(subscription_key))
    image_url_prefix = "https://csdx.blob.core.windows.net/resources/Face/Images/"
    target_image_file_names = ["Family1-Dad1.jpg",
                               "Family1-Daughter1.jpg",
                               "Family1-Mom1.jpg",
                               "Family1-Son1.jpg",
                               "Family2-Lady1.jpg",
                               "Family2-Man1.jpg",
                               "Family3-Lady1.jpg",
                               "Family3-Man1.jpg"]

    source_image_file_name = "findsimilar.jpg"

    # Create a large face list.
    large_face_list_id = str(uuid.uuid4())
    print("Create large face list {}.".format(large_face_list_id))
    face_client.large_face_list.create(large_face_list_id, "large face list for find_similar_in_large_face_list sample", "large face list for find_similar_in_large_face_list sample")

    for target_image_file_name in target_image_file_names:
        faces = face_client.large_face_list.add_face_from_url(large_face_list_id, image_url_prefix + target_image_file_name, target_image_file_name)
        if faces is None:
            raise Exception("No face detected from image {}.".format(target_image_file_name))
        print("Face from image {} is successfully added to the large face list.".format(target_image_file_name))

    # Start to train the large face list.
    print("Train large face list {}".format(large_face_list_id))
    face_client.large_face_list.train(large_face_list_id)

    # Wait until the training is completed.
    while True:
        time.sleep(1)
        training_status = face_client.large_face_list.get_training_status(large_face_list_id)
        print("Training status is {}.".format(training_status.status))
        if training_status.status != TrainingStatusType.running:
            if training_status.status == TrainingStatusType.failed:
                raise Exception("Training failed with message {}.".format(training_status.message))
            break

    # Get persisted faces from the large face list.
    persisted_faces = list(face_client.large_face_list.list_faces(large_face_list_id))
    if len(persisted_faces) == 0:
        raise Exception("No persisted face in large face list {}.".format(large_face_list_id))

    # Detect faces from source image url.
    detected_faces = detect_faces(face_client, image_url_prefix + source_image_file_name)

    # Find similar example of face id to large face list.
    similar_results = face_client.face.find_similar(detected_faces[0].face_id, None, large_face_list_id)

    for similar_result in similar_results:
        persisted_face = [pf for pf in persisted_faces if pf.persisted_face_id == similar_result.persisted_face_id][0]
        if persisted_face is None:
            print("persisted face not found in similar result.")
            continue
        print("Faces from {} & {} are similar with confidence: {}.".format(source_image_file_name, persisted_face.user_data, similar_result.confidence))

    # Delete the large face list.
    face_client.large_face_list.delete(large_face_list_id)
    print("Delete large face list {}.".format(large_face_list_id))
    print("")


if __name__ == "__main__":
    face_base_url = "https://{}.api.cognitive.microsoft.com".format(FACE_LOCATION)
    find_similar_in_face_ids(face_base_url, SUBSCRIPTION_KEY_ENV_NAME)
    find_similar_in_face_list(face_base_url, SUBSCRIPTION_KEY_ENV_NAME)
    find_similar_in_large_face_list(face_base_url, SUBSCRIPTION_KEY_ENV_NAME)