from azure.cognitiveservices.vision.face import FaceClient
from msrest.authentication import CognitiveServicesCredentials
from azure.cognitiveservices.vision.face.models import FaceAttributeType, FaceAttributes, HairColorType
import os

SUBSCRIPTION_KEY_ENV_NAME = os.environ.get("FACE_SUBSCRIPTION_KEY")
FACE_LOCATION = os.environ.get("FACE_LOCATION", "westcentralus")

def face_detection_run(face_base_url, subscription_key):
    print("Sample of face detection.")

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


def get_accessories(accessories):
    if len(accessories) == 0:
        return "No accessories"
    accessory_array = []

    for i in range(len(accessories)):
        accessory_array.append(str(accessories[i]))
    return ",".join(accessory_array)


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


if __name__ == "__main__":
    face_base_url = "https://{}.api.cognitive.microsoft.com".format(FACE_LOCATION)
    face_detection_run(face_base_url, SUBSCRIPTION_KEY_ENV_NAME)






















