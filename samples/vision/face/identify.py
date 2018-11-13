from azure.cognitiveservices.vision.face import FaceClient
from azure.cognitiveservices.vision.face.models import Person, TrainingStatusType
from msrest.authentication import CognitiveServicesCredentials
from samples.vision.face.common import detect_faces
import os
import uuid
import time

SUBSCRIPTION_KEY_ENV_NAME = "FACE_SUBSCRIPTION_KEY"
FACE_LOCATION = os.environ.get("FACE_LOCATION", "westcentralus")


def identify_in_person_group(face_base_url, subscription_key):
    print("Sample of identifying faces in a group of people.")

    face_client = FaceClient(face_base_url, CognitiveServicesCredentials(subscription_key))
    image_url_prefix = "https://csdx.blob.core.windows.net/resources/Face/Images/"
    target_image_file_dictionary = {
        "Family1-Dad" : ["Family1-Dad1.jpg", "Family1-Dad2.jpg"],
        "Family1-Mom" : ["Family1-Mom1.jpg", "Family1-Mom2.jpg"],
        "Family1-Son" : ["Family1-Son1.jpg", "Family1-Son2.jpg"],
        "Family1-Daughter" : ["Family1-Daughter1.jpg", "Family1-Daughter2.jpg"],
        "Family2-Lady" : ["Family2-Lady1.jpg", "Family2-Lady2.jpg"],
        "Family2-Man" : ["Family2-Man1.jpg", "Family2-Man2.jpg"]
    }
    source_image_file_name = "identification1.jpg"

    # Create a person group.
    person_group_id = str(uuid.uuid4())
    print("Create a person group {}.".format(person_group_id))
    face_client.person_group.create(person_group_id, person_group_id)

    for target_image_file_dictionary_name in target_image_file_dictionary.keys():
        person_id = face_client.person_group_person.create(person_group_id, target_image_file_dictionary_name).person_id

        # Limit TPS
        time.sleep(0.25)

        # Create a person group person.
        person = Person(name=target_image_file_dictionary_name, user_data="Person for sample", person_id=person_id)

        print("Create a person group person {}.".format(person.name))

        for target_image_file_name in target_image_file_dictionary[target_image_file_dictionary_name]:
            # Add face to the person group person
            print("Add face to the person group person {} from image.".format(target_image_file_dictionary_name, target_image_file_name))
            face = face_client.person_group_person.add_face_from_url(person_group_id, person.person_id, image_url_prefix + target_image_file_name, target_image_file_name)
            if face is None:
                raise Exception("No persisted face from image {}".format(target_image_file_name))

    # Start to train the person group.
    print("Train person group {}".format(person_group_id))
    face_client.person_group.train(person_group_id)
    training_status = face_client.person_group.get_training_status(person_group_id)
    print("Training status is {}".format(training_status.status))
    if training_status.status != TrainingStatusType.running:
        if training_status.status == TrainingStatusType.failed:
            raise Exception("Training failed with message {}.".format(training_status.message))

    source_face_ids = []

    # Detect faces from source image url.
    detected_faces = detect_faces(face_client, image_url_prefix + source_image_file_name)

    # Add detected face id to source_face_ids
    for detected_face in detected_faces:
        source_face_ids.append(detected_face.face_id)

    # Identify example of identifying faces towards person group.
    identify_results = face_client.face.identify(source_face_ids, person_group_id)
    if identify_results is None:
        print("No person identified in the person group for faces from the {}.".format(source_image_file_name))
        return

    for identify_result in identify_results:
        person = face_client.person_group_person.get(person_group_id, identify_result.candidates[0].person_id)
        print("Person {} is identified for face: {} - {}, confidence: {}.".format(person.name, source_image_file_name, identify_result.face_id, identify_result.candidates[0].confidence))

    # Delete the person group.
    face_client.person_group.delete(person_group_id)
    print("Delete the person group {}.".format(person_group_id))
    print("")


def identify_in_large_person_group(face_base_url, subscription_key):
    print("Sample of identify faces in large person group.")

    face_client = FaceClient(face_base_url, CognitiveServicesCredentials(subscription_key))
    image_url_prefix = "https://csdx.blob.core.windows.net/resources/Face/Images/"
    target_image_file_dictionary = {
        "Family1-Dad": ["Family1-Dad1.jpg", "Family1-Dad2.jpg"],
        "Family1-Mom": ["Family1-Mom1.jpg", "Family1-Mom2.jpg"],
        "Family1-Son": ["Family1-Son1.jpg", "Family1-Son2.jpg"],
        "Family1-Daughter": ["Family1-Daughter1.jpg", "Family1-Daughter2.jpg"],
        "Family2-Lady": ["Family2-Lady1.jpg", "Family2-Lady2.jpg"],
        "Family2-Man": ["Family2-Man1.jpg", "Family2-Man2.jpg"]
    }
    source_image_file_name = "identification1.jpg"

    # Create a large person group.
    large_person_group_id = str(uuid.uuid4())
    print("Create a large person group {}.".format(large_person_group_id))
    face_client.large_person_group.create(large_person_group_id, large_person_group_id)

    for target_image_file_dictionary_name in target_image_file_dictionary.keys():
        person_id = face_client.large_person_group_person.create(large_person_group_id, target_image_file_dictionary_name).person_id

        # Limit TPS
        time.sleep(0.25)

        # Create a person group person.
        person = Person(name=target_image_file_dictionary_name, user_data="Person for sample", person_id=person_id)

        print("Create a large person group person {}.".format(person.name))

        for target_image_file_name in target_image_file_dictionary[target_image_file_dictionary_name]:
            # Add face to the person group person
            print("Add face to the large person group person {} from image.".format(target_image_file_dictionary_name, target_image_file_name))
            face = face_client.large_person_group_person.add_face_from_url(large_person_group_id, person.person_id, image_url_prefix + target_image_file_name, target_image_file_name)
            if face is None:
                raise Exception("No persisted face from image {}".format(target_image_file_name))

    # Start to train the large person group.
    print("Train large person group {}.".format(large_person_group_id))
    face_client.large_person_group.train(large_person_group_id)
    training_status = face_client.large_person_group.get_training_status(large_person_group_id)
    print("Training status is {}".format(training_status.status))
    if training_status.status == TrainingStatusType.failed:
        raise Exception("Training failed with message {}.".format(training_status.message))


    source_face_ids = []

    # Detect faces from source image url.
    detected_faces = detect_faces(face_client, image_url_prefix + source_image_file_name)

    # Add detected face ids to source_face_ids
    for detected_face in detected_faces:
        source_face_ids.append(detected_face.face_id)

    # Identify example of identifying faces towards large person group.
    identify_results = face_client.face.identify(source_face_ids, None, large_person_group_id)
    if identify_results is None:
        print("No person identified in the large person group for faces from the {}.".format(source_image_file_name))
        return

    for identify_result in identify_results:
        person = face_client.large_person_group_person.get(large_person_group_id, identify_result.candidates[0].person_id)
        print ("Person {} is identified for face: {} - {}, confidence: {}.".format(person.name, source_image_file_name, identify_result.face_id, identify_result.candidates[0].confidence))

    # Delete the person group.
    face_client.large_person_group.delete(large_person_group_id)
    print("Delete the large person group {}.".format(large_person_group_id))
    print("")


if __name__ == "__main__":
    face_base_url = "https://{}.api.cognitive.microsoft.com".format(FACE_LOCATION)
    identify_in_person_group(face_base_url, "e312068d12604dee97f59230ff788d60")
    identify_in_large_person_group(face_base_url, "e312068d12604dee97f59230ff788d60")