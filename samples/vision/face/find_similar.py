from azure.cognitiveservices.vision.face import FaceClient
from msrest.authentication import CognitiveServicesCredentials

def find_similar_in_face_ids(endpoint, subscription_key):
    print("Sample of finding similar faces in face ids.")
    face_client = FaceClient(endpoint, CognitiveServicesCredentials(subscription_key))
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
        faces = face_client.face.detect_with_url(image_url_prefix + target_image_file_name)
        target_face_ids.append(faces[0].face_id.value)
    detected_faces = face_client.face.detect_with_url(source_image_file_name)
    similar_results = face_client.face.find_similar(detected_faces[0].face_id.value, None, None, target_face_ids)
    if len(similar_results) == 0:
        print("No similar faces to {}.".format(source_image_file_name))
    for similar_result in similar_results:
        print("Faces from {} & {} are similar with confidence: {}.".format(source_image_file_name, similar_result.face_id, similar_result.confidence))