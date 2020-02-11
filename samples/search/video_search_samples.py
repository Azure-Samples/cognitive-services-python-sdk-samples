import os

from azure.cognitiveservices.search.videosearch import VideoSearchClient
from azure.cognitiveservices.search.videosearch.models import VideoPricing, VideoLength, VideoResolution, VideoInsightModule
from msrest.authentication import CognitiveServicesCredentials

# Add your Bing Search V7 subscription key to your environment variables.
SUBSCRIPTION_KEY = os.environ['BING_SEARCH_V7_SUBSCRIPTION_KEY']
ENDPOINT = os.environ['BING_SEARCH_V7_ENDPOINT']

def video_search(subscription_key):
    """VideoSearch.

    This will search videos for (SwiftKey) then verify number of results and print out id, name and url of first video result.
    """
    client = VideoSearchClient(ENDPOINT, CognitiveServicesCredentials(subscription_key))

    try:
        video_result = client.videos.search(query="SwiftKey")
        print("Search videos for query \"SwiftKey\"")

        if video_result.value:
            first_video_result = video_result.value[0]
            print("Video result count: {}".format(len(video_result.value)))
            print("First video id: {}".format(first_video_result.video_id))
            print("First video name: {}".format(first_video_result.name))
            print("First video url: {}".format(first_video_result.content_url))
        else:
            print("Didn't see any video result data..")

    except Exception as err:
        print("Encountered exception. {}".format(err))


def video_search_with_filtering(subscription_key):
    """VideoSearchWithFilters.

    This will search videos for (Bellevue Trailer) that is free, short and 1080p resolution then verify number of results and print out id, name and url of first video result
    """
    client = VideoSearchAPI(CognitiveServicesCredentials(subscription_key))

    try:
        video_result = client.videos.search(
            query="Bellevue Trailer",
            pricing=VideoPricing.free,  # Can use the str "free" too
            length=VideoLength.short,   # Can use the str "short" too
            resolution=VideoResolution.hd1080p  # Can use the str "hd1080p" too
        )
        print("Search videos for query \"Bellevue Trailer\" that is free, short and 1080p resolution")

        if video_result.value:
            first_video_result = video_result.value[0]
            print("Video result count: {}".format(len(video_result.value)))
            print("First video id: {}".format(first_video_result.video_id))
            print("First video name: {}".format(first_video_result.name))
            print("First video url: {}".format(first_video_result.content_url))
        else:
            print("Didn't see any video result data..")

    except Exception as err:
        print("Encountered exception. {}".format(err))


def video_trending(subscription_key):
    """VideoTrending.

    This will trending videos then verify banner tiles and categories.
    """
    client = VideoSearchAPI(CognitiveServicesCredentials(subscription_key))

    try:
        trending_result = client.videos.trending()
        print("Search trending video")

        # Banner tiles
        if trending_result.banner_tiles:
            first_banner_tile = trending_result.banner_tiles[0]
            print("Banner tile count: {}".format(
                len(trending_result.banner_tiles)))
            print("First banner tile text: {}".format(
                first_banner_tile.query.text))
            print("First banner tile url: {}".format(
                first_banner_tile.query.web_search_url))
        else:
            print("Couldn't find banner tiles!")

        # Categorires
        if trending_result.categories:
            first_category = trending_result.categories[0]
            print("Category count: {}".format(len(trending_result.categories)))
            print("First category title: {}".format(first_category.title))
            if first_category.subcategories:
                first_subcategory = first_category.subcategories[0]
                print("Subcategory count: {}".format(
                    len(first_category.subcategories)))
                print("First subcategory title: {}".format(
                    first_subcategory.title))
                if first_subcategory.tiles:
                    first_tile = first_subcategory.tiles[0]
                    print("Subcategory tile count: {}".format(
                        len(first_subcategory.tiles)))
                    print("First tile text: {}".format(first_tile.query.text))
                    print("First tile url: {}".format(
                        first_tile.query.web_search_url))
                else:
                    print("Couldn't find subcategory tiles!")
            else:
                print("Couldn't find subcategories!")
        else:
            print("Couldn't find categories!")

    except Exception as err:
        print("Encountered exception. {}".format(err))


def video_detail(subscription_key):
    """VideoDetail.

    This will search videos for (Bellevue Trailer) and then search for detail information of the first video
    """
    client = VideoSearchAPI(CognitiveServicesCredentials(subscription_key))

    try:
        video_result = client.videos.search(query="Bellevue Trailer")
        first_video_result = video_result.value[0]

        video_details = client.videos.details(
            query="Bellevue Trailer",
            id=first_video_result.video_id,
            modules=[VideoInsightModule.all]  # Can use ["all"] too
        )
        print("Search detail for video id={}, name={}".format(
            first_video_result.video_id,
            first_video_result.name
        ))

        if video_details.video_result:
            print("Expected Video id: {}".format(
                video_details.video_result.video_id))
            print("Expected Video name: {}".format(
                video_details.video_result.name))
            print("Expected Video url: {}".format(
                video_details.video_result.content_url))
        else:
            print("Couldn't find expected video")

        if video_details.related_videos.value:
            first_related_video = video_details.related_videos.value[0]
            print("Related video count: {}".format(
                len(video_details.related_videos.value)))
            print("First related video id: {}".format(
                first_related_video.video_id))
            print("First related video name: {}".format(
                first_related_video.name))
            print("First related video content url: {}".format(
                first_related_video.content_url))
        else:
            print("Couldn't find any related video!")

    except Exception as err:
        print("Encountered exception. {}".format(err))


if __name__ == "__main__":
    import sys, os.path
    sys.path.append(os.path.abspath(os.path.join(__file__, "..", "..", "..")))    
    from samples.tools import execute_samples
    execute_samples(globals(), SUBSCRIPTION_KEY)
