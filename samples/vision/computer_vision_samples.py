import os.path

from azure.cognitiveservices.vision.computervision import ComputerVisionAPI
from azure.cognitiveservices.vision.computervision.models import VisualFeatureTypes
from msrest.authentication import CognitiveServicesCredentials

SUBSCRIPTION_KEY_ENV_NAME = "COMPUTERVISION_SUBSCRIPTION_KEY"
COMPUTERVISION_LOCATION = os.environ.get("COMPUTERVISION_LOCATION", "westcentralus")

IMAGES_FOLDER = os.path.join(os.path.dirname(os.path.realpath(__file__)), "images")

def image_analysis_in_stream(subscription_key):
    """ImageAnalysisInStream.

    This will analysis an image from a stream and return all available features.
    """
    client = ComputerVisionAPI(COMPUTERVISION_LOCATION, CognitiveServicesCredentials(subscription_key))

    with open(os.path.join(IMAGES_FOLDER, "house.jpg"), "rb") as image_stream:
        image_analysis = client.analyze_image_in_stream(
            image_stream,
            visual_features=[
                VisualFeatureTypes.image_type, # Could use simple str "ImageType"
                VisualFeatureTypes.faces,      # Could use simple str "Faces"
                VisualFeatureTypes.categories, # Could use simple str "Categories"
                VisualFeatureTypes.color,      # Could use simple str "Color"
                VisualFeatureTypes.tags,       # Could use simple str "Tags"
                VisualFeatureTypes.description # Could use simple str "Description"
            ]
        )

    print("This imsage can be described as: {}\n".format(image_analysis.description.captions[0].text))

    print("Tags associated with this image:\nTag\t\tConfidence")
    for tag in image_analysis.tags:
        print("{}\t\t{}".format(tag.name, tag.confidence))

    print("\nThe primary colors of this image are: {}".format(image_analysis.color.dominant_colors))


if __name__ == "__main__":
    import sys, os.path
    sys.path.append(os.path.abspath(os.path.join(__file__, "..", "..")))
    from tools import execute_samples
    execute_samples(globals(), SUBSCRIPTION_KEY_ENV_NAME)