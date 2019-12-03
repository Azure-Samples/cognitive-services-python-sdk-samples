from os import getcwd, makedirs, path
# from urllib import parse # Python 3.x
from urlparse import urlparse # Python 2.x
import uuid
import datetime
import time

import adal
from msrestazure.azure_active_directory import AdalAuthentication
from msrestazure.azure_cloud import AZURE_PUBLIC_CLOUD
from azure.mgmt.media import AzureMediaServices
from azure.mgmt.media.models import *
from azure.storage.blob import BlockBlobService


def video_analyze():
    """VideoAnalyze.

    This will analyze a video and download insights for video analysis
    """
    # Your configurations for your AMS account
    account_name = 'ams account'
    resource_group_name = 'ResourceGroup'
    subscription_id = '00000000-0000-0000-0000-000000000000'
    aad_client_id = '00000000-0000-0000-0000-000000000000'
    aad_secret = 'XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX'
    tenant_id = 'tenant domain or tenant id'

    # Your input file name and output folder name for encoding
    input_mp4_file_name = 'ignite.mp4'
    input_mp4_files_baseurl = 'https://shigeyfampdemo.azurewebsites.net/videos/'
    input_mp4_files = ['ignite.mp4']
    output_folder_name = 'output'
    transform_name = 'MyVideoAnalyzerTransformName'

    # The Azure Media Services (AMS) Client
    # You can now use this object to perform different operations to your AMS account.
    login_endpoint = AZURE_PUBLIC_CLOUD.endpoints.active_directory
    resource = AZURE_PUBLIC_CLOUD.endpoints.active_directory_resource_id
    context = adal.AuthenticationContext(login_endpoint + '/' + tenant_id)
    credentials = AdalAuthentication(
        context.acquire_token_with_client_credentials,
        resource,
        aad_client_id,
        aad_secret
    )
    client = AzureMediaServices(credentials, subscription_id)

    # Creating a unique suffix so that we don't have name collisions if you run the sample
    # multiple times without cleaning up.
    uniqueness = str(uuid.uuid1())
    job_name = 'job-{}'.format(uniqueness)
    output_asset_name = 'output-{}'.format(uniqueness)
    input_asset_name = 'input-{}'.format(uniqueness)

    # Ensure that you have the desired video analyzer Transform. This is really a one time setup operation.
    get_or_create_transform(client, resource_group_name, account_name, transform_name, VideoAnalyzerPreset(audio_language = 'en-US'))

    # Create a new job input
    # Option 1) Create a new job input with Asset and upload the specified local video file into it.
    #create_input_asset(client, resource_group_name, account_name, input_asset_name, input_mp4_file_name)
    #job_input = JobInputAsset(asset_name = inputasset_name)
    # Option 2) Create a new job input with HTTP
    job_input = JobInputHttp(base_uri = input_mp4_files_baseurl, files = input_mp4_files)

    # Output from the encoding Job must be written to an Asset, so let's create one
    output_asset = create_output_asset(client, resource_group_name, account_name, output_asset_name)
    
    job = submit_job(client, resource_group_name, account_name, transform_name, job_name, job_input, output_asset.name)

    # In this demo code, we will poll for Job status
    # Polling is not a recommended best practice for production applications because of the latency it introduces.
    # Overuse of this API may trigger throttling. Developers should instead use Event Grid.
    job = wait_for_job_to_finish(client, resource_group_name, account_name, transform_name, job_name)

    if job.state == JobState.finished:
        print('Job finished.')
        download_output_asset(client, resource_group_name, account_name, output_asset.name, output_folder_name)
        print('Done.')


def get_or_create_transform(client, resource_group_name, account_name, transform_name, preset):
    """If the specified transform exists, get that transform.
    If the it does not exist, creates a new transform with the specified output. 
    In this case, the output is set to encode a video using one of the built-in encoding presets.
    :param client: The Azure Media Services Client.
    :param resource_group_name: The name of the resource group within the Azure subscription.
    :param account_name: The Media Services account name.
    :param transform_name: The transform name.
    :param preset: the preset.
    :return Transform
    :rtype: ~azure.mgmt.media.models.Transform
    """        
    # Does a Transform already exist with the desired name? Assume that an existing Transform with the desired name
    # also uses the same recipe or Preset for processing content.
    transform = client.transforms.get(resource_group_name, account_name, transform_name)

    if not transform:            
        transformOutput = TransformOutput(preset = preset)
        # You need to specify what you want it to produce as an output
        output = [transformOutput]
        # Create the Transform with the output defined above
        transform = client.transforms.create_or_update(resource_group_name, account_name, transform_name, output)

    return transform

def create_input_asset(client, resource_group_name, account_name, asset_name, file_to_upload):
    """ Creates a new input Asset and uploads the specified local video file into it.
    :param client: The Azure Media Services Client.
    :param resource_group_name: The name of the resource group within the Azure subscription.
    :param account_name: The Media Services account name.
    :param asset_name: The asset name.
    :param file_to_upload: The file you want to upload into the asset.
    :return Asset
    :rtype: ~azure.mgmt.media.models.Asset
    """
    # In this example, we are assuming that the asset name is unique.
    #
    # If you already have an asset with the desired name, use the Assets.Get method
    # to get the existing asset. In Media Services v3, the Get method on entities returns null 
    # if the entity doesn't exist (a case-insensitive check on the name).

    # Call Media Services API to create an Asset.
    # This method creates a container in storage for the Asset.
    # The files (blobs) associated with the asset will be stored in this container.
    asset = client.assets.create_or_update(resource_group_name, account_name, asset_name, Asset())

    # Use Media Services API to get back a response that contains
    # SAS URL for the Asset container into which to upload blobs.
    # That is where you would specify read-write permissions 
    # and the expiration time for the SAS URL.
    # expiryTime = datetime.datetime.utcnow() + datetime.timedelta(hours = 4)
    response = client.assets.list_container_sas(
        resource_group_name,
        account_name,
        asset_name,
        permissions = AssetContainerPermission.read_write,
        expiry_time= datetime.datetime.utcnow() + datetime.timedelta(hours = 4))

    sasUri = response.asset_container_sas_urls[0]

    # Use Storage API to get a reference to the Asset container
    # that was created by calling Asset's CreateOrUpdate method. 
    #parsed_url = parse.urlparse(sasUri) # Python 3.x
    parsed_url = urlparse(sasUri) # Python 2.x
    storage_account_name = parsed_url.netloc.split('.')[0]

    # Remove the leading /
    container_name = parsed_url.path[1:]
    token = parsed_url.query
    local_path = getcwd()
    block_blob_service = BlockBlobService(account_name = storage_account_name, sas_token = token)
        
    # Use Storage API to upload the file into the container in storage.
    block_blob_service.create_blob_from_path(container_name, file_to_upload, path.join(local_path, file_to_upload))

    return asset

def create_output_asset(client, resource_group_name, account_name, asset_name):
    """ Creates an output asset. The output from the encoding Job must be written to an Asset.
    :param client: The Azure Media Services Client.
    :param resource_group_name: The name of the resource group within the Azure subscription.
    :param account_name: The Media Services account name.
    :param asset_name: The asset name.
    :return Asset
    :rtype: ~azure.mgmt.media.models.Asset
    """
    # Check if an Asset already exists
    output_asset = client.assets.get(resource_group_name, account_name, asset_name)
    asset = Asset()
    output_asset_name = asset_name
    
    if output_asset is not None:
        # Name collision! In order to get the sample to work, let's just go ahead and create a unique asset name
        # Note that the returned Asset can have a different name than the one specified as an input parameter.
        # You may want to update this part to throw an Exception instead, and handle name collisions differently.
        uniqueness = uuid.uuid1
        output_asset_name += str(uniqueness)
        print('Warning - found an existing Asset with name = ' + asset_name)
        print('Creating an Asset with this name instead: ' + output_asset_name)                

    return client.assets.create_or_update(resource_group_name, account_name, output_asset_name, asset)
    
def submit_job(client, resource_group_name, account_name, transform_name, job_name, job_input, outputasset_name):
    """Submits a request to Media Services to apply the specified Transform to a given input video.
    :param client: The Azure Media Services Client.
    :param resource_group_name: The name of the resource group within the Azure subscription.
    :param account_name: The Media Services account name.
    :param transform_name: The transform name.
    :param job_name: The job name. 
    :param inputasset_name: The inputAsset name.      
    :param outputasset_name: The outputAsset name.                   
    :return: Job
    :rtype: ~azure.mgmt.media.models.Job
    """ 
    job_output = JobOutputAsset(asset_name = outputasset_name)
    job_outputs = [job_output]
    job = Job(input = job_input, outputs = job_outputs)

    # In this example, we are assuming that the job name is unique.
    #
    # If you already have a job with the desired name, use the Jobs.Get method
    # to get the existing job. In Media Services v3, the Get method on entities returns null 
    # if the entity doesn't exist (a case-insensitive check on the name).    
    job = client.jobs.create(resource_group_name, account_name, transform_name, job_name, job)

    return job

def wait_for_job_to_finish(client, resource_group_name, account_name, transform_name, job_name):
    """ Polls Media Services for the status of the Job.
    :param client: The Azure Media Services Client.
    :param resource_group_name: The name of the resource group within the Azure subscription.
    :param account_name: The Media Services account name.
    :param transform_name: The transform name.
    :param job_name: The job name.
    :return: Job
    :rtype: ~azure.mgmt.media.models.Job
    """
    SleepIntervalMs = 5

    while True:
        job = client.jobs.get(resource_group_name, account_name, transform_name, job_name)
        print('Job is {}'.format(job.state))

        for i in range(len(job.outputs)):
            output = job.outputs[i]
            print(' JobOutput[{}] is {}'.format(i, output.state))
            if output.state == JobState.processing:
                print('  Progress: {}'.format(output.progress))
        
        if job.state == JobState.finished or job.state == JobState.error or job.state == JobState.canceled:
            break

        time.sleep(SleepIntervalMs)

    return job

def download_output_asset(client, resource_group_name, account_name, asset_name, output_folder_name):
    """Downloads the results from the specified output asset, so you can see what you got.
    :param client: The Azure Media Services Client.
    :param resource_group_name: The name of the resource group within the Azure subscription.
    :param account_name: The Media Services account name.
    :param asset_name: The asset name.
    :param output_folder_name: The output folder name.      
    """

    if not path.exists(output_folder_name):
        makedirs(output_folder_name)

    assetContainerSas = client.assets.list_container_sas(
        resource_group_name,
        account_name,
        asset_name,
        permissions = AssetContainerPermission.read,
        expiry_time= datetime.datetime.utcnow() + datetime.timedelta(hours = 4))
    container_sas_url = assetContainerSas.asset_container_sas_urls[0]
    
    directory = path.join(output_folder_name, asset_name)
    makedirs(directory)

    print('Downloading output results to {}'.format(directory))

    #parsed_url = parse.urlparse(container_sas_url) # Python 3.x
    parsed_url = urlparse(container_sas_url) # Python 2.x
    storage_account_name = parsed_url.netloc.split('.')[0]
    container_name = parsed_url.path[1:]
    token = parsed_url.query
    block_blob_service = BlockBlobService(account_name = storage_account_name, sas_token = token)

    # Download the blobs in the container.
    generator = block_blob_service.list_blobs(container_name)
    for blob in generator:
        print('Downloading Blob: {}'.format(blob.name))
        block_blob_service.get_blob_to_path(container_name, blob.name, path.join(directory, blob.name))

    print('Download complete.')

if __name__ == '__main__':
    video_analyze()
