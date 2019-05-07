import os, io, uuid, glob, time
from msrest.authentication import CognitiveServicesCredentials
from azure.cognitiveservices.vision.face import FaceClient
from azure.cognitiveservices.vision.face.models import TrainingStatusType, Person

'''
PersonGroup - Face API sample
References: 
    How-to guide: https://docs.microsoft.com/en-us/azure/cognitive-services/face/face-api-how-to-topics/howtoidentifyfacesinimage
    SDK: https://docs.microsoft.com/en-us/python/api/azure-cognitiveservices-vision-face/azure.cognitiveservices.vision.face?view=azure-python
    Sample images to download: https://github.com/Microsoft/Cognitive-Face-Windows/tree/master/Data
Prerequisites:
    Python 3+
    Install Face SDK: pip install azure-cognitiveservices-vision-face
'''
# Group image for testing against
group_photo = 'test-image.jpg'
# To add subdirectories, ex: (os.path.realpath(__file__), "images-directory", "above-images-directory")
IMAGES_FOLDER = os.path.join(os.path.dirname(os.path.realpath(__file__)))

''' 
Authentication
'''
# Replace with a valid subscription key (keeping the quotes in place).
KEY = '<ADD SUBSCRIPTION KEY HERE>'
# Replace westus if it's not your region
BASE_URL = 'https://westus.api.cognitive.microsoft.com'
face_client = FaceClient(BASE_URL, CognitiveServicesCredentials(KEY))

''' 
Create the PersonGroup
'''
# Create empty person group
# person_group_id = str(uuid.uuid4()) # Uncomment to generate a random ID
person_group_id = 'my-unique-person-group'
print(person_group_id)
face_client.person_group.create(person_group_id=person_group_id, name=person_group_id)

# Define woman friend 
woman = face_client.person_group_person.create(person_group_id, "Woman")
# Define man friend
man = face_client.person_group_person.create(person_group_id, "Man")
# Define child friend
child = face_client.person_group_person.create(person_group_id, "Child")

'''
Detect faces and register to correct person
'''
# Find all jpeg images of friends in working directory
woman_images = [file for file in glob.glob('*.jpg') if file.startswith("woman")]
man_images = [file for file in glob.glob('*.jpg') if file.startswith("man")]
child_images = [file for file in glob.glob('*.jpg') if file.startswith("child")]

# Add to a woman person
for image in woman_images:
    w = open(image, 'r+b')
    face_client.person_group_person.add_face_from_stream(person_group_id, woman.person_id, w)

# Add to a man person
for image in man_images:
    m = open(image, 'r+b')
    face_client.person_group_person.add_face_from_stream(person_group_id, man.person_id, m)

# Add to a child person
for image in child_images:
    ch = open(image, 'r+b')
    face_client.person_group_person.add_face_from_stream(person_group_id, child.person_id, ch)

''' 
Train PersonGroup
'''
# Train the person group
face_client.person_group.train(person_group_id)
training_status = face_client.person_group.get_training_status(person_group_id)
while (training_status.status == TrainingStatusType.running):
    print(training_status.status)
    if (training_status.status == TrainingStatusType.failed):
        raise Exception('Training failed with message {}.'.format(training_status.message))
    if (training_status.status == TrainingStatusType.succeeded):
        print(training_status.status)
        break
    time.sleep(1)

'''
Identify a face against a defined PersonGroup
'''
# Get test image
test_image_array = glob.glob(os.path.join(IMAGES_FOLDER, group_photo))
image = open(test_image_array[0], 'r+b')

# Detect faces
face_ids = []
faces = face_client.face.detect_with_stream(image)
for face in faces:
    face_ids.append(face.face_id)

# Identify faces
results = face_client.face.identify(face_ids, person_group_id)
if not results:
    print('No person identified in the person group for faces from the {}.'.format(os.path.basename(image.name)))
for person in results:
    print('Person for face ID {} is identified in {} with a confidence of {}.'.format(person.face_id, os.path.basename(image.name), person.candidates[0].confidence)) # Get topmost confidence score

# Once finished, since testing, delete the PersonGroup from your resource, otherwise when you create it again, it won't allow duplicate person groups.
face_client.person_group.delete(person_group_id)
