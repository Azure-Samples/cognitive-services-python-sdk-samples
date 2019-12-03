import os
import time

from azure.cognitiveservices.knowledge.qnamaker import QnAMakerClient
from azure.cognitiveservices.knowledge.qnamaker.models import QnADTO, MetadataDTO, CreateKbDTO, OperationStateType, UpdateKbOperationDTO, UpdateKbOperationDTOAdd
from msrest.authentication import CognitiveServicesCredentials

# Add your QnaMaker subscription key and endpoint to your environment variables.
SUBSCRIPTION_KEY = os.environ['QNA_MAKER_SUBSCRIPTION_KEY']
QNA_ENDPOINT = os.environ['QNA_MAKER_ENDPOINT']


def knowledge_based_crud_sample(subscription_key):
    """KnowledgeBasedCRUDSample.

    This will create, update, publish, download, then delete a knowledge base.
    """
    def _create_sample_kb(client):
        """Helper function for knowledge_based_crud_sample.

        This helper function takes in a QnAMakerClient and returns an operation of a created knowledge base.
        """
        qna = QnADTO(
            answer="You can use our REST APIs to manage your knowledge base.",
            questions=["How do I manage my knowledgebase?"],
            metadata=[MetadataDTO(name="Category", value="api")]
        )
        urls = [
            "https://docs.microsoft.com/en-in/azure/cognitive-services/qnamaker/faqs"]
        create_kb_dto = CreateKbDTO(
            name="QnA Maker FAQ from quickstart",
            qna_list=[qna],
            urls=urls
        )
        create_op = client.knowledgebase.create(
            create_kb_payload=create_kb_dto)
        create_op = _monitor_operation(client=client, operation=create_op)
        return create_op.resource_location.replace("/knowledgebases/", "")

    def _monitor_operation(client, operation):
        """Helper function for knowledge_based_crud_sample.

        This helper function takes in a QnAMakerClient and an operation, and loops until the operation has either succeeded
        or failed and returns the operation.
        """
        for i in range(20):
            if operation.operation_state in [OperationStateType.not_started, OperationStateType.running]:
                print("Waiting for operation: {} to complete.".format(
                    operation.operation_id))
                time.sleep(5)
                operation = client.operations.get_details(
                    operation_id=operation.operation_id)
            else:
                break
        if operation.operation_state != OperationStateType.succeeded:
            raise Exception("Operation {} failed to complete.".format(
                operation.operation_id))
        return operation

    client = QnAMakerClient(endpoint=QNA_ENDPOINT, credentials=CognitiveServicesCredentials(subscription_key))

    # Create a KB
    print("Creating KB...")
    kb_id = _create_sample_kb(client=client)
    print("Created KB with ID: {}".format(kb_id))

    # Update the KB
    print("Updating KB...")
    update_kb_operation_dto = UpdateKbOperationDTO(
        add=UpdateKbOperationDTOAdd(
            qna_list=[
                QnADTO(questions=["bye"], answer="goodbye")
            ]
        )
    )
    update_op = client.knowledgebase.update(
        kb_id=kb_id, update_kb=update_kb_operation_dto)
    _monitor_operation(client=client, operation=update_op)

    # Publish the KB
    print("Publishing KB...")
    client.knowledgebase.publish(kb_id=kb_id)
    print("KB Published.")

    # Download the KB
    print("Downloading KB...")
    kb_data = client.knowledgebase.download(kb_id=kb_id, environment="Prod")
    print("KB Downloaded. It has {} QnAs.".format(len(kb_data.qna_documents)))

    # Delete the KB
    print("Deleting KB...")
    client.knowledgebase.delete(kb_id=kb_id)
    print("KB Deleted.")

knowledge_based_crud_sample(SUBSCRIPTION_KEY_ENV_NAME)
