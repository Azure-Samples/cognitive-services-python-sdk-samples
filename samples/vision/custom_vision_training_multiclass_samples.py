import os
import time

from azure.cognitiveservices.vision.customvision.training.custom_vision_training_client import CustomVisionTrainingClient
from azure.cognitiveservices.vision.customvision.training.models import Classifier

SUBSCRIPTION_KEY_ENV_NAME = "CUSTOMVISION_TRAINING_KEY"
SAMPLE_PROJECT_NAME = "Python SDK Sample"

ENDPOINT = "https://southcentralus.api.cognitive.microsoft.com"

IMAGES_FOLDER = os.path.join(os.path.dirname(os.path.realpath(__file__)), "images")

def train_project(subscription_key):

    trainer = CustomVisionTrainingClient(subscription_key, endpoint=ENDPOINT)

    # Create a new project
    print ("Creating project...")
    project = trainer.create_project(SAMPLE_PROJECT_NAME, classification_type=Classifier.multiclass)

    # Make two tags in the new project
    hemlock_tag = trainer.create_tag(project.id, "Hemlock")
    cherry_tag = trainer.create_tag(project.id, "Japanese Cherry")
    pine_needle_tag =  trainer.create_tag(project.id, "Pine Needle Leaves")
    flat_leaf_tag = trainer.create_tag(project.id, "Flat Leaves")

    print ("Adding images...")
    hemlock_dir = os.path.join(IMAGES_FOLDER, "Hemlock")
    for image in os.listdir(hemlock_dir):
        with open(os.path.join(hemlock_dir, image), mode="rb") as img_data: 
            trainer.create_images_from_data(project.id, img_data.read(), [ hemlock_tag.id, pine_needle_tag.id ])
    
    cherry_dir = os.path.join(IMAGES_FOLDER, "Japanese Cherry")
    for image in os.listdir(cherry_dir):
        with open(os.path.join(cherry_dir, image), mode="rb") as img_data: 
            trainer.create_images_from_data(project.id, img_data.read(), [ cherry_tag.id, flat_leaf_tag.id ])

    print ("Training...")
    iteration = trainer.train_project(project.id)
    while (iteration.status == "Training"):
        iteration = trainer.get_iteration(project.id, iteration.id)
        print ("Training status: " + iteration.status)
        time.sleep(1)

    # The iteration is now trained. Make it the default project endpoint
    trainer.update_iteration(project.id, iteration.id, is_default=True)
    print ("Done!")
    return project

if __name__ == "__main__":
    import sys, os.path
    sys.path.append(os.path.abspath(os.path.join(__file__, "..", "..")))
    from tools import execute_samples
    execute_samples(globals(), SUBSCRIPTION_KEY_ENV_NAME)