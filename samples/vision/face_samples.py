from azure.cognitiveservices.vision.face import FaceClient
from msrest.authentication import CognitiveServicesCredentials
from azure.cognitiveservices.vision.face.models import FaceAttributeType, HairColorType, TrainingStatusType, Person
import os
import uuid
import time

SUBSCRIPTION_KEY_ENV_NAME = "FACE_SUBSCRIPTION_KEY"
FACE_LOCATION = os.environ.get("FACE_LOCATION", "westcentralus")

IMAGES_FOLDER = os.path.join(os.path.dirname(os.path.realpath(__file__)), "images", "Face")


'''
Sample that returns the faces detected in an image

Parameter face_client: a FaceClient instance.
Parameter image_url: the url for the image where faces are to be detected.
Returns: a list of faces detected in the image
'''
def detect_faces(face_client, image_url):
    '''Detect faces in an image'''

    detected_faces = face_client.face.detect_with_url(image_url, True, False, None, None, False)
    if detected_faces is None or len(detected_faces) == 0:
        raise Exception('No face detected from image {}'.format(image_url))
    print("{} faces detected from image {}".format(len(detected_faces), image_url))
    if detected_faces[0] is None:
        raise Exception("Parameter return_face_id of detect_with_stream or detect_with_url must be set to true (by default) for recognition purpose.")
    return list(detected_faces)



'''
Sample that prints out all of facial attributes for a list of images.

Parameter face_base_url: the endpoint for the Face API calls.
Parameter subscription_key: the Face API key.
'''
def face_detection(subscription_key):
    '''Face detection and attributes'''

    '''
    Helper function for face_detection sample that returns a string representation of a person's accessories.

    Parameter accessories: the accessories detected in an image.
    Return: string representation of a person's accessories.
    '''

    def get_accessories(accessories):
        if len(accessories) == 0:
            return "No accessories"
        accessory_array = []

        for i in range(len(accessories)):
            accessory_array.append(str(accessories[i]))
        return ",".join(accessory_array)

    '''
    Helper function for face_detection sample that determines the emotion a person is showing.

    Parameter emotion: the emotion object detected in an image.
    Return: the emotion that the face is showing in the image.
    '''

    def get_emotion(emotion):
        emotion_type = ""
        emotion_value = 0.0
        if emotion.anger > emotion_value:
            emotion_type = "anger"
            emotion_value = emotion.anger
        if emotion.contempt > emotion_value:
            emotion_type = "contempt"
            emotion_value = emotion.contempt
        if emotion.disgust > emotion_value:
            emotion_type = "disgust"
            emotion_value = emotion.disgust
        if emotion.fear > emotion_value:
            emotion_type = "fear"
            emotion_value = emotion.fear
        if emotion.happiness > emotion_value:
            emotion_type = "happiness"
            emotion_value = emotion.happiness
        if emotion.neutral > emotion_value:
            emotion_type = "neutral"
            emotion_value = emotion.neutral
        if emotion.sadness > emotion_value:
            emotion_type = "sadness"
            emotion_value = emotion.sadness
        if emotion.surprise > emotion_value:
            emotion_type = "surprise"
        return emotion_type

    '''
    Helper function for face_detection sample that determines the hair color detected for a face in an image.

    Parameter hair: hair object from a face detected in an image.
    Return: the hair color.
    '''

    def get_hair(hair):
        if len(hair.hair_color) == 0:
            return "invisible" if hair.invisible else "bald"
        return_color = HairColorType.unknown
        max_confidence = 0.0

        for hair_color in hair.hair_color:
            if hair_color.confidence <= max_confidence:
                continue;
            max_confidence = hair_color.confidence
            return_color = hair_color.color;

        return str(return_color)

    face_base_url = "https://{}.api.cognitive.microsoft.com".format(FACE_LOCATION)
    face_client = FaceClient(face_base_url, CognitiveServicesCredentials(subscription_key))
    image_url_prefix = "https://csdx.blob.core.windows.net/resources/Face/Images/"
    image_file_names = ["detection1.jpg",
                        "detection2.jpg",
                        "detection3.jpg",
                        "detection4.jpg",
                        "detection5.jpg",
                        "detection6.jpg"]
    for image_file_name in image_file_names:
        detected_faces = face_client.face.detect_with_url(image_url_prefix + image_file_name, True, return_face_attributes = [
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
                                                                                                    ])
        if detected_faces == None or len(detected_faces) == 0:
            raise Exception("No face detected from image {}".format(image_file_name))
        print("{} faces detected from image {}".format(len(detected_faces), image_file_name))
        if detected_faces[0].face_attributes is None:
            raise Exception("Parameter return_face_attributes of detect_with_stream_async must be set to get face attributes.")

        for face in detected_faces:
            print("Face attributes of {}   Rectangle(Left/Top/Width/Height) : {} {} {} {}".format(image_file_name, face.face_rectangle.left, face.face_rectangle.top, face.face_rectangle.width, face.face_rectangle.height))
            print("Face attributes of {}   Accessories : {}".format(image_file_name, get_accessories(face.face_attributes.accessories)))
            print("Face attributes of {}   Age : {}".format(image_file_name, face.face_attributes.age))
            print("Face attributes of {}   Blur : {}".format(image_file_name, face.face_attributes.blur.blur_level))
            print("Face attributes of {}   Emotion : {}".format(image_file_name, get_emotion(face.face_attributes.emotion)))
            print("Face attributes of {}   Exposure : {}".format(image_file_name, face.face_attributes.exposure.exposure_level))
            if face.face_attributes.facial_hair.moustache + face.face_attributes.facial_hair.beard + face.face_attributes.facial_hair.sideburns > 0:
                print("Face attributes of {}   FacialHair : Yes".format(image_file_name))
            else:
                print("Face attributes of {}   FacialHair : No".format(image_file_name))
            print("Face attributes of {}   Gender : {}".format(image_file_name, face.face_attributes.gender))
            print("Face attributes of {}   Glasses : {}".format(image_file_name, face.face_attributes.glasses))
            print("Face attributes of {}   Hair : {}".format(image_file_name, get_hair(face.face_attributes.hair)))
            print("Face attributes of {}   HeadPose : Pitch: {}, Roll: {}, Yaw: {}".format(image_file_name, round(face.face_attributes.head_pose.pitch, 2), round(face.face_attributes.head_pose.roll, 2), round(face.face_attributes.head_pose.yaw, 2)))
            if face.face_attributes.makeup.eye_makeup or face.face_attributes.makeup.lip_makeup:
                print("Face attributes of {}   Makeup : Yes".format(image_file_name))
            else:
                print("Face attributes of {}   Makeup : No".format(image_file_name))
            print("Face attributes of {}   Noise : {}".format(image_file_name, face.face_attributes.noise.noise_level))
            print("Face attributes of {}   Occlusion : EyeOccluded: {},   ForeheadOccluded: {},   MouthOccluded: {}".format(image_file_name, "Yes" if face.face_attributes.occlusion.eye_occluded else "No",
                                                                                                                        "Yes" if face.face_attributes.occlusion.forehead_occluded else "No", "Yes" if face.face_attributes.occlusion.mouth_occluded else "No"))

            print("Face attributes of {}   Smile : {}".format(image_file_name, face.face_attributes.smile))
            print()


'''
Sample that shows how to detect similar faces from a list of images against a single image using face ids.

Parameter face_base_url: the endpoint for the Face API calls.
Parameter subscription_key: the Face API key.
'''
def find_similar_in_face_ids(subscription_key):
    '''Finding similar faces using face ids'''

    face_base_url = "https://{}.api.cognitive.microsoft.com".format(FACE_LOCATION)
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


'''
Sample that shows how to detect similar faces from a list of images against a single image by placing the list of images in a face list.

Parameter face_base_url: the endpoint for the Face API calls.
Parameter subscription_key: the Face API key.
'''
def find_similar_in_face_list(subscription_key):
    '''Detecting similar faces in a face list'''

    face_base_url = "https://{}.api.cognitive.microsoft.com".format(FACE_LOCATION)
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



'''
Sample that shows how to detect similar faces from a list of images against a single image by placing the list of images in a large face list.

Parameter face_base_url: the endpoint for the Face API calls.
Parameter subscription_key: the Face API key.
'''
def find_similar_in_large_face_list(subscription_key):
    '''Detecting similar faces in a large face list'''

    face_base_url = "https://{}.api.cognitive.microsoft.com".format(FACE_LOCATION)
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


'''
Sample of grouping faces based on similarity in a group and of grouping faces that don't have any other faces with similar features into a messy group.

Parameter face_base_url: the endpoint for the Face API calls.
Parameter subscription_key: the Face API key.
'''
def group_run(subscription_key):
    '''Sample of grouping faces'''

    face_base_url = "https://{}.api.cognitive.microsoft.com".format(FACE_LOCATION)
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


'''
Sample of how to identify faces in a group of people.

Parameter face_base_url: the endpoint for the Face API calls.
Parameter subscription_key: the Face API key.
'''
def identify_in_person_group(subscription_key):
    '''Identifying faces in a group of people'''

    face_base_url = "https://{}.api.cognitive.microsoft.com".format(FACE_LOCATION)
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


'''
Sample of how to identify faces in a large person group.

Parameter face_base_url: the endpoint for the Face API calls.
Parameter subscription_key: the Face API key.
'''
def identify_in_large_person_group(subscription_key):
    '''Identifying faces in a large person group'''

    face_base_url = "https://{}.api.cognitive.microsoft.com".format(FACE_LOCATION)
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

'''
Sample of verifying whether faces detected as similar are the same person.

Parameter face_base_url: the endpoint for the Face API calls.
Parameter subscription_key: the Face API key.
'''
def verify_face_to_face(subscription_key):
    '''Verifying face to face'''

    face_base_url = "https://{}.api.cognitive.microsoft.com".format(FACE_LOCATION)
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


'''
Sample of verifying whether faces detected as similar in a group are of the same person.

Parameter face_base_url: the endpoint for the Face API calls.
Parameter subscription_key: the Face API key.
'''
def verify_in_person_group(subscription_key):
    '''Verifying face to person group'''

    face_base_url = "https://{}.api.cognitive.microsoft.com".format(FACE_LOCATION)
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


'''
Sample of verifying whether faces detected as similar in a large group are of the same person.
'''
def verify_in_large_person_group(subscription_key):
    '''Verifying person to large person group'''

    face_base_url = "https://{}.api.cognitive.microsoft.com".format(FACE_LOCATION)
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
    import sys, os.path
    sys.path.append(os.path.abspath(os.path.join(__file__, "..", "..")))
    from samples.tools import execute_samples
    execute_samples(globals(), SUBSCRIPTION_KEY_ENV_NAME)