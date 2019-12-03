import os
import time

from azure.cognitiveservices.vision.customvision.training import CustomVisionTrainingClient

SUBSCRIPTION_KEY_ENV_NAME = "CUSTOMVISION_TRAINING_KEY"
PREDICTION_RESOURCE_ID_KEY_ENV_NAME = "CUSTOMVISION_PREDICTION_ID"

SAMPLE_PROJECT_NAME = "Python SDK Sample"
PUBLISH_ITERATION_NAME = "classifyModel"

# Add your Custom Vision endpoint to your environment variables.
ENDPOINT = os.environ["CUSTOM_VISION_ENDPOINT"]

IMAGES_FOLDER = os.path.join(os.path.dirname(
    os.path.realpath(__file__)), "images")


class PredictionResourceMissingError(Exception):
    pass

def train_project(subscription_key):
    try:
        prediction_resource_id = os.environ[PREDICTION_RESOURCE_ID_KEY_ENV_NAME]
    except KeyError:
        raise PredictionResourceMissingError("Didn't find a prediction resource to publish to. Please set the {} environment variable".format(PREDICTION_RESOURCE_ID_KEY_ENV_NAME))

    trainer = CustomVisionTrainingClient(subscription_key, endpoint=ENDPOINT)

    # Create a new project
    print("Creating project...")
    project = trainer.create_project(SAMPLE_PROJECT_NAME)

    # Make two tags in the new project
    hemlock_tag = trainer.create_tag(project.id, "Hemlock")
    cherry_tag = trainer.create_tag(project.id, "Japanese Cherry")

    print("Adding images...")
    hemlock_dir = os.path.join(IMAGES_FOLDER, "Hemlock")
    for image in os.listdir(hemlock_dir):
        with open(os.path.join(hemlock_dir, image), mode="rb") as img_data:
            trainer.create_images_from_data(
                project.id, img_data.read(), [hemlock_tag.id])

    cherry_dir = os.path.join(IMAGES_FOLDER, "Japanese Cherry")
    for image in os.listdir(cherry_dir):
        with open(os.path.join(cherry_dir, image), mode="rb") as img_data:
            trainer.create_images_from_data(
                project.id, img_data.read(), [cherry_tag.id])

    print("Training...")
    iteration = trainer.train_project(project.id)
    while (iteration.status == "Training"):
        iteration = trainer.get_iteration(project.id, iteration.id)
        print("Training status: " + iteration.status)
        time.sleep(1)

    # The iteration is now trained. Name and publish this iteration to a prediciton endpoint
    trainer.publish_iteration(project.id, iteration.id, PUBLISH_ITERATION_NAME, prediction_resource_id)
    print ("Done!")

    return project


if __name__ == "__main__":
    import sys, os.path
    sys.path.append(os.path.abspath(os.path.join(__file__, "..", "..", "..")))
    from samples.tools import execute_samples
    execute_samples(globals(), SUBSCRIPTION_KEY_ENV_NAME)
