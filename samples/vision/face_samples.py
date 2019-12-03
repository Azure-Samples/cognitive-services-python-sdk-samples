import os
import uuid
import time

from azure.cognitiveservices.vision.face import FaceClient
from msrest.authentication import CognitiveServicesCredentials
from azure.cognitiveservices.vision.face.models import FaceAttributeType, HairColorType, TrainingStatusType, Person

SUBSCRIPTION_KEY_ENV_NAME = "FACE_SUBSCRIPTION_KEY"
FACE_LOCATION = os.environ.get("FACE_LOCATION", "westcentralus")

IMAGES_FOLDER = os.path.join(os.path.dirname(
    os.path.realpath(__file__)), "images", "Face")


def image_analysis_in_stream(subscription_key):
    """ImageAnalysisInStream.

    This will analyze an image from a stream and return all available features.
    """

    face_base_url = "https://{}.api.cognitive.microsoft.com".format(
        FACE_LOCATION)
    face_client = FaceClient(
        face_base_url, CognitiveServicesCredentials(subscription_key))

    faces = [jpgfile for jpgfile in os.listdir(
        IMAGES_FOLDER) if jpgfile.startswith("Family1")]
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
        print("Detected gender: {}".format(
            detected_face.face_attributes.gender))
        print("Detected emotion: {}".format(
            detected_face.face_attributes.emotion.happiness))
    print("\n")

    # Verification example for faces of the same person.
    verify_result = face_client.face.verify_face_to_face(
        faces_ids[0],
        faces_ids[1],
    )
    if verify_result.is_identical:
        print("Faces from {} & {} are of the same (Positive) person, similarity confidence: {}.".format(
            faces[0], faces[1], verify_result.confidence))
    else:
        print("Faces from {} & {} are of different (Negative) persons, similarity confidence: {}.".format(
            faces[0], faces[1], verify_result.confidence))

    # Verification example for faces of different persons.
    verify_result = face_client.face.verify_face_to_face(
        faces_ids[1],
        faces_ids[2],
    )
    if verify_result.is_identical:
        print("Faces from {} & {} are of the same (Positive) person, similarity confidence: {}.".format(
            faces[1], faces[2], verify_result.confidence))
    else:
        print("Faces from {} & {} are of different (Negative) persons, similarity confidence: {}.".format(
            faces[1], faces[2], verify_result.confidence))


def detect_faces(subscription_key):
    """DetectFaces.

    This will detect the faces found in the image with url image_url using the provided FaceClient instance and print out the number of faces detected in an image.
    """

    image_url = "https://csdx.blob.core.windows.net/resources/Face/Images/Family1-Dad1.jpg"
    face_base_url = "https://{}.api.cognitive.microsoft.com".format(
        FACE_LOCATION)
    face_client = FaceClient(
        endpoint=face_base_url, credentials=CognitiveServicesCredentials(subscription_key))
    detected_faces = face_client.face.detect_with_url(url=image_url)
    if not detected_faces:
        raise Exception('No face detected from image {}'.format(image_url))
    print("{} faces detected from image {}".format(
        len(detected_faces), image_url))
    if not detected_faces[0]:
        raise Exception(
            "Parameter return_face_id of detect_with_stream or detect_with_url must be set to true (by default) for recognition purpose.")


def face_detection(subscription_key):
    """FaceDetection.

    This will print out all of the facial attributes for a list of images.
    """

    def get_accessories(accessories):
        """Helper function for face_detection sample.

        This will return a string representation of a person's accessories.
        """

        accessory_str = ",".join([str(accessory) for accessory in accessories])
        return accessory_str if accessory_str else "No accessories"

    def get_emotion(emotion):
        """Helper function for face_detection sample.

        This will determine and return the emotion a person is showing.
        """

        max_emotion_value = 0.0
        emotion_type = None

        for emotion_name, emotion_value in vars(emotion).items():
            if emotion_name == "additional_properties":
                continue
            if emotion_value > max_emotion_value:
                max_emotion_value = emotion_value
                emotion_type = emotion_name
        return emotion_type

    def get_hair(hair):
        """Helper function for face_detection sample.

         This determines and returns the hair color detected for a face in an image.
        """

        if not hair.hair_color:
            return "invisible" if hair.invisible else "bald"
        return_color = HairColorType.unknown
        max_confidence = 0.0

        for hair_color in hair.hair_color:
            if hair_color.confidence > max_confidence:
                max_confidence = hair_color.confidence
                return_color = hair_color.color

        return return_color

    face_base_url = "https://{}.api.cognitive.microsoft.com".format(
        FACE_LOCATION)
    face_client = FaceClient(
        endpoint=face_base_url, credentials=CognitiveServicesCredentials(subscription_key))
    image_url_prefix = "https://csdx.blob.core.windows.net/resources/Face/Images/"
    image_file_names = [
        "detection1.jpg",
        "detection2.jpg",
        "detection3.jpg",
        "detection4.jpg",
        "detection5.jpg",
        "detection6.jpg"
    ]
    for image_file_name in image_file_names:
        detected_faces = face_client.face.detect_with_url(
            url=image_url_prefix + image_file_name,
            return_face_attributes=[
                FaceAttributeType.accessories,
                'age',
                'blur',
                'emotion',
                'exposure',
                'facialHair',
                'gender',
                'glasses',
                'hair',
                'headPose',
                'makeup',
                'noise',
                'occlusion',
                'smile'
            ]
        )
        if not detected_faces:
            raise Exception(
                "No face detected from image {}".format(image_file_name))
        print("{} faces detected from image {}".format(
            len(detected_faces), image_file_name))
        if not detected_faces[0].face_attributes:
            raise Exception(
                "Parameter return_face_attributes of detect_with_stream_async must be set to get face attributes.")

        for face in detected_faces:
            print("Face attributes of {}   Rectangle(Left/Top/Width/Height) : {} {} {} {}".format(
                image_file_name,
                face.face_rectangle.left,
                face.face_rectangle.top,
                face.face_rectangle.width,
                face.face_rectangle.height)
            )
            print("Face attributes of {}   Accessories : {}".format(
                image_file_name, get_accessories(face.face_attributes.accessories)))
            print("Face attributes of {}   Age : {}".format(
                image_file_name, face.face_attributes.age))
            print("Face attributes of {}   Blur : {}".format(
                image_file_name, face.face_attributes.blur.blur_level))
            print("Face attributes of {}   Emotion : {}".format(
                image_file_name, get_emotion(face.face_attributes.emotion)))
            print("Face attributes of {}   Exposure : {}".format(
                image_file_name, face.face_attributes.exposure.exposure_level))
            if face.face_attributes.facial_hair.moustache + face.face_attributes.facial_hair.beard + face.face_attributes.facial_hair.sideburns > 0:
                print("Face attributes of {}   FacialHair : Yes".format(
                    image_file_name))
            else:
                print("Face attributes of {}   FacialHair : No".format(
                    image_file_name))
            print("Face attributes of {}   Gender : {}".format(
                image_file_name, face.face_attributes.gender))
            print("Face attributes of {}   Glasses : {}".format(
                image_file_name, face.face_attributes.glasses))
            print("Face attributes of {}   Hair : {}".format(
                image_file_name, get_hair(face.face_attributes.hair)))
            print("Face attributes of {}   HeadPose : Pitch: {}, Roll: {}, Yaw: {}".format(
                image_file_name,
                round(face.face_attributes.head_pose.pitch, 2),
                round(face.face_attributes.head_pose.roll, 2),
                round(face.face_attributes.head_pose.yaw, 2))
            )
            if face.face_attributes.makeup.eye_makeup or face.face_attributes.makeup.lip_makeup:
                print("Face attributes of {}   Makeup : Yes".format(image_file_name))
            else:
                print("Face attributes of {}   Makeup : No".format(image_file_name))
            print("Face attributes of {}   Noise : {}".format(
                image_file_name, face.face_attributes.noise.noise_level))
            print("Face attributes of {}   Occlusion : EyeOccluded: {},   ForeheadOccluded: {},   MouthOccluded: {}".format(
                image_file_name,
                "Yes" if face.face_attributes.occlusion.eye_occluded else "No",
                "Yes" if face.face_attributes.occlusion.forehead_occluded else "No",
                "Yes" if face.face_attributes.occlusion.mouth_occluded else "No")
            )

            print("Face attributes of {}   Smile : {}".format(
                image_file_name, face.face_attributes.smile))


def find_similar_in_face_ids(subscription_key):
    """FindSimilarInFaceIds.

    This will detect similar faces from a list of images against a single image using face ids.
    """

    face_base_url = "https://{}.api.cognitive.microsoft.com".format(
        FACE_LOCATION)
    face_client = FaceClient(
        endpoint=face_base_url, credentials=CognitiveServicesCredentials(subscription_key))
    image_url_prefix = "https://csdx.blob.core.windows.net/resources/Face/Images/"
    target_image_file_names = [
        "Family1-Dad1.jpg",
        "Family1-Daughter1.jpg",
        "Family1-Mom1.jpg",
        "Family1-Son1.jpg",
        "Family2-Lady1.jpg",
        "Family2-Man1.jpg",
        "Family3-Lady1.jpg",
        "Family3-Man1.jpg"
    ]

    source_image_file_name = "findsimilar.jpg"
    # Detect faces from target image url and add detected face id to target_face_ids
    target_face_ids = [_detect_faces_helper(face_client=face_client, image_url=image_url_prefix + target_image_file_name)[0].face_id
                       for target_image_file_name in target_image_file_names]

    detected_faces = _detect_faces_helper(
        face_client=face_client, image_url=image_url_prefix + source_image_file_name)
    # Find similar example of face id to face ids.
    similar_results = face_client.face.find_similar(
        face_id=detected_faces[0].face_id, face_ids=target_face_ids)
    if not similar_results:
        print("No similar faces to {}.".format(source_image_file_name))
    for similar_result in similar_results:
        print("Faces from {} & {} are similar with confidence: {}.".format(
            source_image_file_name, similar_result.face_id, similar_result.confidence))


def find_similar_in_face_list(subscription_key):
    """FindSimilarInFaceList.

    This will detect similar faces from a list of images against a single image by placing the images in a face list.
    """

    face_base_url = "https://{}.api.cognitive.microsoft.com".format(
        FACE_LOCATION)
    face_client = FaceClient(
        endpoint=face_base_url, credentials=CognitiveServicesCredentials(subscription_key))
    image_url_prefix = "https://csdx.blob.core.windows.net/resources/Face/Images/"
    target_image_file_names = [
        "Family1-Dad1.jpg",
        "Family1-Daughter1.jpg",
        "Family1-Mom1.jpg",
        "Family1-Son1.jpg",
        "Family2-Lady1.jpg",
        "Family2-Man1.jpg",
        "Family3-Lady1.jpg",
        "Family3-Man1.jpg"
    ]

    source_image_file_name = "findsimilar.jpg"
    # Create a face list.
    face_list_id = str(uuid.uuid4())
    print("Create face list {}.".format(face_list_id))
    face_client.face_list.create(
        face_list_id=face_list_id,
        name="face list for find_similar_in_face_list sample",
        user_data="face list for find_similar_in_face_list sample"
    )

    for target_image_file_name in target_image_file_names:
        # Add face to face list.
        faces = face_client.face_list.add_face_from_url(
            face_list_id=face_list_id,
            url=image_url_prefix + target_image_file_name,
            user_data=target_image_file_name
        )
        if not faces:
            raise Exception("No face detected from image {}".format(
                target_image_file_name))
        print("Face from image {} is successfully added to the face list.".format(
            target_image_file_name))
    # Get persisted faces from the face list.
    persisted_faces = face_client.face_list.get(face_list_id).persisted_faces
    if not persisted_faces:
        raise Exception(
            "No persisted face in face list {}".format(face_list_id))

    # Detect faces from source image url.
    detected_faces = _detect_faces_helper(
        face_client=face_client, image_url=image_url_prefix + source_image_file_name)

    # Find similar example of face id to face list.
    similar_results = face_client.face.find_similar(
        face_id=detected_faces[0].face_id, face_list_id=face_list_id)
    for similar_result in similar_results:
        persisted_faces = [
            pf for pf in persisted_faces if pf.persisted_face_id == similar_result.persisted_face_id]
        if not persisted_faces:
            print("persisted face not found in similar result.")
            continue
        persisted_face = persisted_faces[0]
        print("Faces from {} & {} are similar with confidence: {}.".format(
            source_image_file_name, persisted_face.user_data, similar_result.confidence))

    # Delete the face list.
    face_client.face_list.delete(face_list_id=face_list_id)
    print("Delete face list {}.\n".format(face_list_id))


def find_similar_in_large_face_list(subscription_key):
    """FindSimilarInLargeFaceList.

    This will detect similar faces from a list of images against a single image by placing the list of images in a large face list.
    """

    face_base_url = "https://{}.api.cognitive.microsoft.com".format(
        FACE_LOCATION)
    face_client = FaceClient(
        endpoint=face_base_url, credentials=CognitiveServicesCredentials(subscription_key))
    image_url_prefix = "https://csdx.blob.core.windows.net/resources/Face/Images/"
    target_image_file_names = [
        "Family1-Dad1.jpg",
        "Family1-Daughter1.jpg",
        "Family1-Mom1.jpg",
        "Family1-Son1.jpg",
        "Family2-Lady1.jpg",
        "Family2-Man1.jpg",
        "Family3-Lady1.jpg",
        "Family3-Man1.jpg"
    ]

    source_image_file_name = "findsimilar.jpg"

    # Create a large face list.
    large_face_list_id = str(uuid.uuid4())
    print("Create large face list {}.".format(large_face_list_id))
    face_client.large_face_list.create(
        large_face_list_id=large_face_list_id,
        name="large face list for find_similar_in_large_face_list sample",
        user_data="large face list for find_similar_in_large_face_list sample"
    )

    for target_image_file_name in target_image_file_names:
        faces = face_client.large_face_list.add_face_from_url(
            large_face_list_id=large_face_list_id,
            url=image_url_prefix + target_image_file_name,
            user_data=target_image_file_name
        )
        if not faces:
            raise Exception("No face detected from image {}.".format(
                target_image_file_name))
        print("Face from image {} is successfully added to the large face list.".format(
            target_image_file_name))

    # Start to train the large face list.
    print("Train large face list {}".format(large_face_list_id))
    face_client.large_face_list.train(large_face_list_id=large_face_list_id)

    training_status = face_client.large_face_list.get_training_status(
        large_face_list_id=large_face_list_id)
    if training_status.status == TrainingStatusType.failed:
        raise Exception("Training failed with message {}.".format(
            training_status.message))

    # Get persisted faces from the large face list.
    persisted_faces = face_client.large_face_list.list_faces(
        large_face_list_id)
    if not persisted_faces:
        raise Exception(
            "No persisted face in large face list {}.".format(large_face_list_id))

    # Detect faces from source image url.
    detected_faces = _detect_faces_helper(
        face_client=face_client, image_url=image_url_prefix + source_image_file_name)

    # Find similar example of face id to large face list.
    similar_results = face_client.face.find_similar(
        face_id=detected_faces[0].face_id, large_face_list_id=large_face_list_id)

    for similar_result in similar_results:
        persisted_faces = [
            pf for pf in persisted_faces if pf.persisted_face_id == similar_result.persisted_face_id]
        if not persisted_faces:
            print("persisted face not found in similar result.")
            continue
        persisted_face = persisted_faces[0]
        print("Faces from {} & {} are similar with confidence: {}.".format(
            source_image_file_name, persisted_face.user_data, similar_result.confidence))

    # Delete the large face list.
    face_client.large_face_list.delete(large_face_list_id=large_face_list_id)
    print("Delete large face list {}.\n".format(large_face_list_id))


def group_run(subscription_key):
    """GroupRun.

    This will group faces based on similarity in a group, and will place faces that don't have any other similar faces in a messy group.
    """

    face_base_url = "https://{}.api.cognitive.microsoft.com".format(
        FACE_LOCATION)
    face_client = FaceClient(
        endpoint=face_base_url, credentials=CognitiveServicesCredentials(subscription_key))
    image_url_prefix = "https://csdx.blob.core.windows.net/resources/Face/Images/"
    image_file_names = [
        "Family1-Dad1.jpg",
        "Family1-Daughter1.jpg",
        "Family1-Mom1.jpg",
        "Family1-Son1.jpg",
        "Family2-Lady1.jpg",
        "Family2-Man1.jpg",
        "Family3-Lady1.jpg",
        "Family3-Man1.jpg"
    ]

    faces = {}

    for image_file_name in image_file_names:
        # Detect faces from target image url.
        detected_faces = _detect_faces_helper(
            face_client=face_client, image_url=image_url_prefix + image_file_name)

        # Add detected face id to faces.
        if not detected_faces:
            print("No face detected in {}".format(image_file_name))
            continue
        faces[detected_faces[0].face_id] = image_file_name

    # Call grouping, the grouping result is a group collection, each group contains similar faces.
    group_result = face_client.face.group(face_ids=list(faces.keys()))

    # Face groups containing faces that are similar.
    for i, group in enumerate(group_result.groups):
        print("Found face group {}: {}.".format(
            i + 1,
            " ".join([faces[face_id] for face_id in group])
        ))

    # Messy group contains all faces which are not similar to any other faces.
    if group_result.messy_group:
        print("Found messy face group: {}.".format(
            " ".join([faces[face_id] for face_id in group_result.messy_group])
        ))


def identify_in_person_group(subscription_key):
    """IdentifyInPersonGroup.

    This will identify faces in a group of people.
    """

    face_base_url = "https://{}.api.cognitive.microsoft.com".format(
        FACE_LOCATION)
    face_client = FaceClient(
        endpoint=face_base_url, credentials=CognitiveServicesCredentials(subscription_key))
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

    # Create a person group.
    person_group_id = str(uuid.uuid4())
    print("Create a person group {}.".format(person_group_id))
    face_client.person_group.create(
        person_group_id=person_group_id, name=person_group_id)

    for target_image_file_dictionary_name in target_image_file_dictionary.keys():
        person_id = face_client.person_group_person.create(
            person_group_id=person_group_id, name=target_image_file_dictionary_name).person_id

        # Create a person group person.
        person = Person(name=target_image_file_dictionary_name,
                        user_data="Person for sample", person_id=person_id)

        print("Create a person group person {}.".format(person.name))

        for target_image_file_name in target_image_file_dictionary[target_image_file_dictionary_name]:
            # Add face to the person group person
            print("Add face to the person group person {} from image.".format(
                target_image_file_dictionary_name, target_image_file_name))
            face = face_client.person_group_person.add_face_from_url(
                person_group_id=person_group_id,
                person_id=person.person_id,
                url=image_url_prefix + target_image_file_name,
                user_data=target_image_file_name
            )
            if not face:
                raise Exception("No persisted face from image {}".format(
                    target_image_file_name))

    # Start to train the person group.
    print("Train person group {}".format(person_group_id))
    face_client.person_group.train(person_group_id=person_group_id)
    training_status = face_client.person_group.get_training_status(
        person_group_id=person_group_id)
    print("Training status is {}".format(training_status.status))
    if training_status.status == TrainingStatusType.failed:
        raise Exception("Training failed with message {}.".format(
            training_status.message))

    # Detect faces from source image url and add detected face id to source_face_ids
    source_face_ids = [detected_face.face_id for detected_face in _detect_faces_helper(
        face_client=face_client, image_url=image_url_prefix + source_image_file_name)]

    # Identify example of identifying faces towards person group.
    identify_results = face_client.face.identify(
        face_ids=source_face_ids, person_group_id=person_group_id)
    if not identify_results:
        print("No person identified in the person group for faces from the {}.".format(
            source_image_file_name))
        return

    for identify_result in identify_results:
        person = face_client.person_group_person.get(
            person_group_id=person_group_id, person_id=identify_result.candidates[0].person_id)
        print("Person {} is identified for face: {} - {}, confidence: {}.".format(
            person.name,
            source_image_file_name,
            identify_result.face_id,
            identify_result.candidates[0].confidence)
        )

    # Delete the person group.
    face_client.person_group.delete(person_group_id=person_group_id)
    print("Delete the person group {}.\n\n".format(person_group_id))


def identify_in_large_person_group(subscription_key):
    """IdentifyInLargePersonGroup.

    This will identify faces in a large person group.
    """

    face_base_url = "https://{}.api.cognitive.microsoft.com".format(
        FACE_LOCATION)
    face_client = FaceClient(
        endpoint=face_base_url, credentials=CognitiveServicesCredentials(subscription_key))
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
    face_client.large_person_group.create(
        large_person_group_id=large_person_group_id, name=large_person_group_id)

    for target_image_file_dictionary_name in target_image_file_dictionary.keys():
        person_id = face_client.large_person_group_person.create(
            large_person_group_id=large_person_group_id, name=target_image_file_dictionary_name).person_id

        # Create a person group person.
        person = Person(name=target_image_file_dictionary_name,
                        user_data="Person for sample", person_id=person_id)

        print("Create a large person group person {}.".format(person.name))

        for target_image_file_name in target_image_file_dictionary[target_image_file_dictionary_name]:
            # Add face to the person group person
            print("Add face to the large person group person {} from image.".format(
                target_image_file_dictionary_name, target_image_file_name))
            face = face_client.large_person_group_person.add_face_from_url(
                large_person_group_id=large_person_group_id,
                person_id=person.person_id,
                url=image_url_prefix + target_image_file_name,
                user_data=target_image_file_name
            )
            if not face:
                raise Exception("No persisted face from image {}".format(
                    target_image_file_name))

    # Start to train the large person group.
    print("Train large person group {}.".format(large_person_group_id))
    face_client.large_person_group.train(
        large_person_group_id=large_person_group_id)
    training_status = face_client.large_person_group.get_training_status(
        large_person_group_id=large_person_group_id)
    print("Training status is {}".format(training_status.status))
    if training_status.status == TrainingStatusType.failed:
        raise Exception("Training failed with message {}.".format(
            training_status.message))

    # Detect faces from source image url and add detected face ids to source_face_ids
    source_face_ids = [detected_face.face_id for detected_face in _detect_faces_helper(
        face_client=face_client, image_url=image_url_prefix + source_image_file_name)]

    # Identify example of identifying faces towards large person group.
    identify_results = face_client.face.identify(
        face_ids=source_face_ids, large_person_group_id=large_person_group_id)
    if not identify_results:
        print("No person identified in the large person group for faces from the {}.".format(
            source_image_file_name))
        return

    for identify_result in identify_results:
        person = face_client.large_person_group_person.get(
            large_person_group_id=large_person_group_id, person_id=identify_result.candidates[0].person_id)
        print("Person {} is identified for face: {} - {}, confidence: {}.".format(
            person.name,
            source_image_file_name,
            identify_result.face_id,
            identify_result.candidates[0].confidence)
        )

    # Delete the person group.
    face_client.large_person_group.delete(
        large_person_group_id=large_person_group_id)
    print("Delete the large person group {}.\n".format(large_person_group_id))


def verify_face_to_face(subscription_key):
    """VerifyFaceToFace.

    This will verify whether faces detected as similar are the same person.
    """

    face_base_url = "https://{}.api.cognitive.microsoft.com".format(
        FACE_LOCATION)
    face_client = FaceClient(
        endpoint=face_base_url, credentials=CognitiveServicesCredentials(subscription_key))

    image_url_prefix = "https://csdx.blob.core.windows.net/resources/Face/Images/"
    target_image_file_names = ["Family1-Dad1.jpg", "Family1-Dad2.jpg"]
    source_image_file_name1 = "Family1-Dad3.jpg"
    source_image_file_name2 = "Family1-Son1.jpg"

    # Detect faces from target image url and add their face ids to target_face_ids
    target_face_ids = [_detect_faces_helper(face_client=face_client, image_url=image_url_prefix + image_file_name)[0].face_id
                       for image_file_name in target_image_file_names]

    # Detect faces from source image file 1.
    detected_faces1 = _detect_faces_helper(
        face_client=face_client, image_url=image_url_prefix + source_image_file_name1)
    source_face_id1 = detected_faces1[0].face_id

    # Detect faces from source image file 2.
    detected_faces2 = _detect_faces_helper(
        face_client=face_client, image_url=image_url_prefix + source_image_file_name2)
    source_face_id2 = detected_faces2[0].face_id

    # Verification example for faces of the same person.
    verify_result1 = face_client.face.verify_face_to_face(
        face_id1=source_face_id1, face_id2=target_face_ids[0])
    if verify_result1.is_identical:
        print("Faces from {} & {} are of the same (Positive) person, similarity confidence: {}.".format(
            source_image_file_name1, target_image_file_names[0], verify_result1.confidence))
    else:
        print("Faces from {} & {} are of different (Negative) persons, similarity confidence: {}.".format(
            source_image_file_name1, target_image_file_names[0], verify_result1.confidence))

    # Verification example for faces of different persons.
    verify_result2 = face_client.face.verify_face_to_face(
        face_id1=source_face_id2, face_id2=target_face_ids[0])
    if verify_result2.is_identical:
        print("Faces from {} & {} are of the same (Negative) person, similarity confidence: {}.\n".format(
            source_image_file_name2, target_image_file_names[0], verify_result2.confidence))
    else:
        print("Faces from {} & {} are of different (Positive) persons, similarity confidence: {}.\n".format(
            source_image_file_name2, target_image_file_names[0], verify_result2.confidence))


def verify_in_person_group(subscription_key):
    """VerifyInPersonGroup.

    This will verify whether faces detected as similar in a group are of the same person.
    """

    face_base_url = "https://{}.api.cognitive.microsoft.com".format(
        FACE_LOCATION)
    face_client = FaceClient(
        endpoint=face_base_url, credentials=CognitiveServicesCredentials(subscription_key))

    image_url_prefix = "https://csdx.blob.core.windows.net/resources/Face/Images/"
    target_image_file_names = ["Family1-Dad1.jpg", "Family1-Dad2.jpg"]
    source_image_file_name1 = "Family1-Dad3.jpg"

    # Create a person group.
    person_group_id = str(uuid.uuid4())
    print("Create a person group {}.".format(person_group_id))
    face_client.person_group.create(
        person_group_id=person_group_id, name=person_group_id)

    person_id = face_client.person_group_person.create(
        person_group_id=person_group_id, name="Dad").person_id

    # Create a person group person.
    p = Person(name="Dad", user_data="Person for sample", person_id=person_id)
    print("Create a person group person {}.".format(p.name))

    for target_image_file_name in target_image_file_names:
        # Add face to the person group.
        print("Add face to the person group person {} from image {}.".format(
            p.name, target_image_file_name))
        faces = face_client.person_group_person.add_face_from_url(
            person_group_id=person_group_id,
            person_id=p.person_id,
            url=image_url_prefix + target_image_file_name, user_data=target_image_file_name
        )

        if not faces:
            raise Exception("No persisted face from image {}.".format(
                target_image_file_name))

    # Verification example for faces of the same person.
    verify_result = face_client.face.verify_face_to_person(
        face_id=_detect_faces_helper(face_client=face_client,
                                     image_url=image_url_prefix + source_image_file_name1)[0].face_id,
        person_id=p.person_id,
        person_group_id=person_group_id
    )
    if verify_result.is_identical:
        print("Faces from {} & {} are of the same (Positive) person, similarity confidence: {}.".format(
            source_image_file_name1, p.name, verify_result.confidence))
    else:
        print("Faces from {} & {} are of different (Negative) persons, similarity confidence: {}.".format(
            source_image_file_name1, p.name, verify_result.confidence))

    # Delete the person group.
    print("Delete the person group {}.\n".format(person_group_id))
    face_client.person_group.delete(person_group_id=person_group_id)


def verify_in_large_person_group(subscription_key):
    """VerifyInLargePersonGroup.

    This will verify whether faces detected as similar in a large group are of the same person.
    """

    face_base_url = "https://{}.api.cognitive.microsoft.com".format(
        FACE_LOCATION)
    face_client = FaceClient(
        endpoint=face_base_url, credentials=CognitiveServicesCredentials(subscription_key))

    image_url_prefix = "https://csdx.blob.core.windows.net/resources/Face/Images/"
    target_image_file_names = ["Family1-Dad1.jpg", "Family1-Dad2.jpg"]
    source_image_file_name1 = "Family1-Dad3.jpg"

    # Create a large person group.
    large_person_group_id = str(uuid.uuid4())
    print("Create a large person group {}.".format(large_person_group_id))
    face_client.large_person_group.create(
        large_person_group_id=large_person_group_id, name=large_person_group_id)

    person_id = face_client.large_person_group_person.create(
        large_person_group_id=large_person_group_id, name="Dad").person_id

    # Create a large person group person.
    p = Person(name="Dad", user_data="Person for sample", person_id=person_id)
    print("Create a large person group person {}.".format(p.name))

    for target_image_file_name in target_image_file_names:
        # Add face to the large person group.
        print("Add face to the large person group person {} from image {}.".format(
            p.name, target_image_file_name))
        faces = face_client.large_person_group_person.add_face_from_url(
            large_person_group_id=large_person_group_id,
            person_id=p.person_id,
            url=image_url_prefix + target_image_file_name,
            user_data=target_image_file_name
        )

        if not faces:
            raise Exception("No persisted face from image {}.".format(
                target_image_file_name))

    # Verification example for faces of the same person.
    verify_result = face_client.face.verify_face_to_person(
        face_id=_detect_faces_helper(
            face_client=face_client, image_url=image_url_prefix + source_image_file_name1)[0].face_id,
        person_id=p.person_id,
        large_person_group_id=large_person_group_id
    )
    if verify_result.is_identical:
        print("Faces from {} & {} are of the same (Positive) person, similarity confidence: {}.".format(
            source_image_file_name1,
            p.name,
            verify_result.confidence
        ))
    else:
        print("Faces from {} & {} are of different (Negative) persons, similarity confidence: {}.".format(
            source_image_file_name1,
            p.name,
            verify_result.confidence
        ))

    # Delete the person group.
    print("Delete the large person group {}.\n".format(large_person_group_id))
    face_client.large_person_group.delete(
        large_person_group_id=large_person_group_id)


def _detect_faces_helper(face_client, image_url):
    """Detect Faces Helper.

    This will detect the faces found in the image with url image_url using the provided FaceClient instance and return the faces identified in an image.
    """

    detected_faces = face_client.face.detect_with_url(url=image_url)
    if not detected_faces:
        raise Exception('No face detected from image {}'.format(image_url))
    print("{} faces detected from image {}".format(
        len(detected_faces), image_url))
    if not detected_faces[0]:
        raise Exception(
            "Parameter return_face_id of detect_with_stream or detect_with_url must be set to true (by default) for recognition purpose.")
    return detected_faces


if __name__ == "__main__":
    import sys
    import os.path
    sys.path.append(os.path.abspath(os.path.join(__file__, "..", "..")))
    from tools import execute_samples
    execute_samples(globals(), SUBSCRIPTION_KEY_ENV_NAME)
