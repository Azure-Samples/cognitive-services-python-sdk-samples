import os
import uuid
import time

from azure.cognitiveservices.vision.face import FaceClient
from msrest.authentication import CognitiveServicesCredentials
from azure.cognitiveservices.vision.face.models import TrainingStatusType, Person

# NOTE: Replace this with a valid Face subscription key.
SUBSCRIPTION_KEY = "INSERT KEY HERE"

# You must use the same region as you used to get your subscription
# keys. For example, if you got your subscription keys from westus,
# replace "westcentralus" with "westus".
FACE_LOCATION = "westcentralus"

face_base_url = "https://{}.api.cognitive.microsoft.com".format(FACE_LOCATION)
face_client = FaceClient(face_base_url, CognitiveServicesCredentials(SUBSCRIPTION_KEY))

# This image should contain a single face.
remote_image_URL_1 = "https://www.biography.com/.image/t_share/MTQ1MzAyNzYzOTgxNTE0NTEz/john-f-kennedy---mini-biography.jpg"

# This image should contain several faces, at least one of which is similar to the face in remote_image_URL_1.
remote_image_URL_2 = "https://www.biography.com/.image/t_share/MTQ1NDY3OTIxMzExNzM3NjE3/john-f-kennedy---debating-richard-nixon.jpg"

# Detect faces in a remote image.
def detect_faces(face_client, image_url):
	print ("Detecting faces...")
	detected_faces = face_client.face.detect_with_url(url=image_url)
	if not detected_faces:
		raise Exception('No face detected from image {}'.format(image_url))
	if not detected_faces[0]:
		raise Exception("Parameter return_face_id of detect_with_stream or detect_with_url must be set to true (by default) for recognition purpose.")
	return detected_faces

# Find similar faces to @face_ID in @face_IDs.
def find_similar_faces(face_client, face_ID, face_IDs):
	print("Finding similar faces ...")
	return face_client.face.find_similar(face_id=face_ID, face_ids=face_IDs)

# Detect a face in the first image.
faces_1 = detect_faces(face_client, remote_image_URL_1)
if not faces_1[0]:
	print("No faces detected in " + remote_image_URL_1 + ".")
else:
	print("Face IDs of faces detected in " + remote_image_URL_1 + ":")
	for x in faces_1: print (x.face_id)

	print("Using first face ID.")
	face_ID = faces_1[0].face_id

	# Detect a list of faces in the second image.
	faces_2 = detect_faces(face_client, remote_image_URL_2)
	if not faces_2[0]:
		print("No faces detected in " + remote_image_URL_2 + ".")
	else:
		print("Face IDs of faces detected in " + remote_image_URL_2 + ":")
		for x in faces_2: print (x.face_id)

		# Search the faces detected in the second image to find a similar face to the first one.
		similar_faces = find_similar_faces(face_client, face_ID, list(map(lambda x: x.face_id, faces_2)))
		if not similar_faces[0]:
			print("No similar faces found in " + remote_image_URL_2 + ".")
		else:
			print("Similar faces found in " + remote_image_URL_2 + ":")
			for face in similar_faces:
				face_ID = face.face_id
				# SimilarFace only contains a Face ID, Persisted Face ID, and confidence score.
				# So we look up the Face ID in the list of DetectedFaces found in
				# remote_image_URL_2 to get the rest of the face information.
				face_info = next(x for x in faces_2 if x.face_id == face_ID)
				if face_info:
					print("Face ID: " + face_ID)
					print("Face rectangle:")
					print("Left: " + str(face_info.face_rectangle.left))
					print("Top: " + str(face_info.face_rectangle.top))
					print("Width: " + str(face_info.face_rectangle.width))
					print("Height: " + str(face_info.face_rectangle.height))
