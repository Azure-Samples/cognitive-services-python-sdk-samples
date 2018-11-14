from azure.cognitiveservices.vision.face import FaceClient
from azure.cognitiveservices.vision.face.models import Person, TrainingStatusType
from msrest.authentication import CognitiveServicesCredentials
from samples.vision.face.common import detect_faces
import os
import uuid

SUBSCRIPTION_KEY_ENV_NAME = os.environ.get("FACE_SUBSCRIPTION_KEY")
FACE_LOCATION = os.environ.get("FACE_LOCATION", "westcentralus")

def verify_face_to_face(face_base_url, subscription_key):
    print("Sample of verify face to face.")

    face_client = FaceClient(face_base_url, CognitiveServicesCredentials(subscription_key))

    image_url_prefix = "https://csdx.blob.core.windows.net/resources/Face/Images/"
    target_image_file_names = ["Family1-Dad1.jpg", "Family1-Dad2.jpg"]
    source_image_file_name1 = "Family1-Dad3.jpg"
    source_image_file_name2 = "Family1-Son1.jpg"

    target_face_ids = []
    for image_file_name in target_image_file_names:
        # Detect faces from target image url.
        detected_faces = detect_faces(face_client, image_url_prefix + image_file_name)
        target_face_ids.append(detected_faces[0].face_id)

    # Detect faces from source image file 1.
    detected_faces1 = detect_faces(face_client, image_url_prefix + source_image_file_name1)
    source_face_id1 = detected_faces1[0].face_id

    # Detect faces from source image file 2.
    detected_faces2 = detect_faces(face_client, image_url_prefix + source_image_file_name2)
    source_face_id2 = detected_faces2[0].face_id

    # Verification example for faces of the same person.
    verify_result1 = face_client.face.verify_face_to_face(source_face_id1, target_face_ids[0])
    if verify_result1.is_identical:
        print("Faces from {} & {} are of the same (Positive) person, similarity confidence: {}.".format(source_image_file_name1, target_image_file_names[0], verify_result1.confidence))
    else:
        print("Faces from {} & {} are of different (Negative) persons, similarity confidence: {}.".format(source_image_file_name1, target_image_file_names[0], verify_result1.confidence))

    # Verification example for faces of different persons.
    verify_result2 = face_client.face.verify_face_to_face(source_face_id2, target_face_ids[0])
    if verify_result2.is_identical:
        print("Faces from {} & {} are of the same (Negative) person, similarity confidence: {}.".format(
            source_image_file_name2, target_image_file_names[0], verify_result2.confidence))
    else:
        print("Faces from {} & {} are of different (Positive) persons, similarity confidence: {}.".format(
            source_image_file_name2, target_image_file_names[0], verify_result2.confidence))
    print("")


def verify_in_person_group(face_base_url, subscription_key):
    print("Sample of verify face to person group.")
    face_client = FaceClient(face_base_url, CognitiveServicesCredentials(subscription_key))

    image_url_prefix = "https://csdx.blob.core.windows.net/resources/Face/Images/"
    target_image_file_names = ["Family1-Dad1.jpg", "Family1-Dad2.jpg"]
    source_image_file_name1 = "Family1-Dad3.jpg"

    # Create a person group.
    person_group_id = str(uuid.uuid4())
    print("Create a person group {}.".format(person_group_id))
    face_client.person_group.create(person_group_id, person_group_id)

    person_id = face_client.person_group_person.create(person_group_id, "Dad").person_id

    # Create a person group person.
    p = Person(name="Dad", user_data="Person for sample", person_id=person_id)
    print("Create a person group person {}.".format(p.name))

    for target_image_file_name in target_image_file_names:
        # Add face to the person group.
        print("Add face to the person group person {} from image {}.".format(p.name, target_image_file_name))
        faces = face_client.person_group_person.add_face_from_url(person_group_id, p.person_id, image_url_prefix + target_image_file_name, target_image_file_name)

        if faces is None:
            raise Exception("No persisted face from image {}.".format(target_image_file_name))

    face_ids = []

    # Add detected face id to face_ids
    detected_faces = detect_faces(face_client, image_url_prefix + source_image_file_name1)
    face_ids.append(detected_faces[0].face_id)

    # Verification example for faces of the same person.
    verify_result = face_client.face.verify_face_to_person(face_ids[0], p.person_id, person_group_id)
    if verify_result.is_identical:
        print("Faces from {} & {} are of the same (Positive) person, similarity confidence: {}.".format(source_image_file_name1, p.name, verify_result.confidence))
    else:
        print("Faces from {} & {} are of different (Negative) persons, similarity confidence: {}.".format(source_image_file_name1, p.name, verify_result.confidence))

    # Delete the person group.
    print("Delete the person group {}.".format(person_group_id))
    face_client.person_group.delete(person_group_id)
    print("")


def verify_in_large_person_group(face_base_url, subscription_key):
    print("Sample of verify face to large person group.")
    face_client = FaceClient(face_base_url, CognitiveServicesCredentials(subscription_key))

    image_url_prefix = "https://csdx.blob.core.windows.net/resources/Face/Images/"
    target_image_file_names = ["Family1-Dad1.jpg", "Family1-Dad2.jpg"]
    source_image_file_name1 = "Family1-Dad3.jpg"

    # Create a large person group.
    large_person_group_id = str(uuid.uuid4())
    print("Create a large person group {}.".format(large_person_group_id))
    face_client.large_person_group.create(large_person_group_id, large_person_group_id)

    person_id = face_client.large_person_group_person.create(large_person_group_id, "Dad").person_id

    # Create a large person group person.
    p = Person(name="Dad", user_data="Person for sample", person_id=person_id)
    print("Create a large person group person {}.".format(p.name))

    for target_image_file_name in target_image_file_names:
        # Add face to the large person group.
        print("Add face to the large person group person {} from image {}.".format(p.name, target_image_file_name))
        faces = face_client.large_person_group_person.add_face_from_url(large_person_group_id, p.person_id,
                                                                  image_url_prefix + target_image_file_name,
                                                                  target_image_file_name)

        if faces is None:
            raise Exception("No persisted face from image {}.".format(target_image_file_name))

    face_ids = []

    # Add detected face id to face_ids
    detected_faces = detect_faces(face_client, image_url_prefix + source_image_file_name1)
    face_ids.append(detected_faces[0].face_id)

    # Verification example for faces of the same person.
    verify_result = face_client.face.verify_face_to_person(face_ids[0], p.person_id, None, large_person_group_id)
    if verify_result.is_identical:
        print("Faces from {} & {} are of the same (Positive) person, similarity confidence: {}.".format(
            source_image_file_name1, p.name, verify_result.confidence))
    else:
        print("Faces from {} & {} are of different (Negative) persons, similarity confidence: {}.".format(
            source_image_file_name1, p.name, verify_result.confidence))

    # Delete the person group.
    print("Delete the large person group {}.".format(large_person_group_id))
    face_client.large_person_group.delete(large_person_group_id)
    print("")


if __name__ == "__main__":
    face_base_url = "https://{}.api.cognitive.microsoft.com".format(FACE_LOCATION)
    verify_face_to_face(face_base_url, SUBSCRIPTION_KEY_ENV_NAME)
    verify_in_person_group(face_base_url, SUBSCRIPTION_KEY_ENV_NAME)
    verify_in_large_person_group(face_base_url, SUBSCRIPTION_KEY_ENV_NAME)