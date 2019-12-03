import os
import sys

from azure.cognitiveservices.vision.customvision.training import CustomVisionTrainingClient
from azure.cognitiveservices.vision.customvision.prediction import CustomVisionPredictionClient

TRAINING_KEY_ENV_NAME = "CUSTOMVISION_TRAINING_KEY"
SUBSCRIPTION_KEY_ENV_NAME = "CUSTOMVISION_PREDICTION_KEY"

PUBLISH_ITERATION_NAME = "classifyModel"

ENDPOINT = "https://southcentralus.api.cognitive.microsoft.com"

# Add this directory to the path so that custom_vision_training_samples can be found
sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)), "."))

IMAGES_FOLDER = os.path.join(os.path.dirname(
    os.path.realpath(__file__)), "images")


def find_or_train_project():
    try:
        training_key = os.environ[TRAINING_KEY_ENV_NAME]
    except KeyError:
        raise SubscriptionKeyError("You need to set the {} env variable.".format(TRAINING_KEY_ENV_NAME))

    # Use the training API to find the SDK sample project created from the training example.
    from custom_vision_training_samples import train_project, SAMPLE_PROJECT_NAME
    trainer = CustomVisionTrainingClient(training_key, endpoint=ENDPOINT)

    for proj in trainer.get_projects():
        if (proj.name == SAMPLE_PROJECT_NAME):
            return proj

    # Or, if not found, we will run the training example to create it.
    return train_project(training_key)


def predict_project(subscription_key):
    predictor = CustomVisionPredictionClient(
        subscription_key, endpoint=ENDPOINT)

    # Find or train a new project to use for prediction.
    project = find_or_train_project()

    with open(os.path.join(IMAGES_FOLDER, "Test", "test_image.jpg"), mode="rb") as test_data:
         results = predictor.classify_image(project.id, PUBLISH_ITERATION_NAME, test_data.read())

    # Display the results.
    for prediction in results.predictions:
        print("\t" + prediction.tag_name +
              ": {0:.2f}%".format(prediction.probability * 100))


if __name__ == "__main__":
    import sys, os.path
    sys.path.append(os.path.abspath(os.path.join(__file__, "..", "..", "..")))
    from samples.tools import execute_samples, SubscriptionKeyError
    execute_samples(globals(), SUBSCRIPTION_KEY_ENV_NAME)