import time
import datetime

from azure.cognitiveservices.language.luis.authoring import LUISAuthoringClient

from msrest.authentication import CognitiveServicesCredentials

SUBSCRIPTION_KEY_ENV_NAME = "LUIS_SUBSCRIPTION_KEY"

def booking_app(subscription_key):
    """Authoring.

    This will create a LUIS Booking application.
    """
    client = LUISAuthoringClient(
        'https://westus.api.cognitive.microsoft.com',
        CognitiveServicesCredentials(subscription_key),
    )

    try:
        # Create a LUIS app
        default_app_name = "Contoso-{}".format(datetime.datetime.now())
        version_id = "0.1"

        print("Creating App {}, version {}".format(default_app_name, version_id))

        app_id = client.apps.add({
            'name': default_app_name,
            'initial_version_id': version_id,
            'description': "New App created with LUIS Python sample",
            'culture': 'en-us',
        })
        print("Created app {}".format(app_id))

        # Add information into the model

        print("\nWe'll create two new entities.")
        print("The \"Destination\" simple entity will hold the flight destination.")
        print("The \"Class\" hierarchical entity will accept \"First\", \"Business\" and \"Economy\" values.")

        destination_name = "Destination"
        destination_id = client.model.add_entity(
            app_id,
            version_id,
            destination_name
        )
        print("{} simple entity created with id {}".format(
            destination_name,
            destination_id
        ))

        class_name = "Class"
        class_id = client.model.add_hierarchical_entity(
            app_id,
            version_id,
            name=class_name,
            children=["First", "Business", "Economy"]
        )
        print("{} hierarchical entity created with id {}".format(
            class_name,
            class_id
        ))

        print("\nWe'll now create the \"Flight\" composite entity including \"Class\" and \"Destination\".")

        flight_name = "Flight"
        flight_id = client.model.add_composite_entity(
            app_id,
            version_id,
            name=flight_name,
            children=[class_name, destination_name]
        )
        print("{} composite entity created with id {}".format(
            flight_name,
            flight_id
        ))

        find_economy_to_madrid = "find flights in economy to Madrid"
        find_first_to_london = "find flights to London in first class"

        print("\nWe'll create a new \"FindFlights\" intent including the following utterances:")
        print(" - "+find_economy_to_madrid)
        print(" - "+find_first_to_london)

        intent_name = "FindFlights"
        intent_id = client.model.add_intent(
            app_id,
            version_id,
            intent_name
        )
        print("{} intent created with id {}".format(
            intent_name,
            intent_id
        ))

        def get_example_label(utterance, entity_name, value):
            """Build a EntityLabelObject.

            This will find the "value" start/end index in "utterance", and assign it to "entity name"
            """
            utterance = utterance.lower()
            value = value.lower()
            return {
                'entity_name': entity_name,
                'start_char_index': utterance.find(value),
                'end_char_index': utterance.find(value) + len(value)
            }

        utterances = [{
            'text': find_economy_to_madrid,
            'intent_name': intent_name,
            'entity_labels':[
                get_example_label(find_economy_to_madrid, "Flight", "economy to madrid"),
                get_example_label(find_economy_to_madrid, "Destination", "Madrid"),
                get_example_label(find_economy_to_madrid, "Class", "economy"),
            ]
        }, {
            'text': find_first_to_london,
            'intent_name': intent_name,
            'entity_labels':[
                get_example_label(find_first_to_london, "Flight", "London in first class"),
                get_example_label(find_first_to_london, "Destination", "London"),
                get_example_label(find_first_to_london, "Class", "first"),
            ]
        }]
        utterances_result = client.examples.batch(
            app_id,
            version_id,
            utterances
        )

        print("\nUtterances added to the {} intent".format(intent_name))

        # Training the model
        print("\nWe'll start training your app...")

        async_training = client.train.train_version(app_id, version_id)
        is_trained = async_training.status == "UpToDate"

        trained_status = ["UpToDate", "Success"]
        while not is_trained:
            time.sleep(1)
            status = client.train.get_status(app_id, version_id)
            is_trained = all(m.details.status in trained_status for m in status)

        print("Your app is trained. You can now go to the LUIS portal and test it!")

        # Publish the app
        print("\nWe'll start publishing your app...")

        publish_result = client.apps.publish(
            app_id,
            {
                'version_id': version_id,
                'is_staging': False,
                'region': 'westus'
            }
        )
        endpoint = publish_result.endpoint_url + "?subscription-key=" + subscription_key + "&q="
        print("Your app is published. You can now go to test it on\n{}".format(endpoint))

    except Exception as err:
        print("Encountered exception. {}".format(err))


if __name__ == "__main__":
    import sys, os.path
    sys.path.append(os.path.abspath(os.path.join(__file__, "..", "..")))
    from tools import execute_samples
    execute_samples(globals(), SUBSCRIPTION_KEY_ENV_NAME)
