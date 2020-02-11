import os

from azure.cognitiveservices.search.imagesearch import ImageSearchClient
from azure.cognitiveservices.search.imagesearch.models import ImageType, ImageAspect, ImageInsightModule
from msrest.authentication import CognitiveServicesCredentials

SUBSCRIPTION_KEY = os.environ["BING_IMAGE_SEARCH_SUBSCRIPTION_KEY"]
ENDPOINT = os.environ['BING_IMAGE_SEARCH_ENDPOINT']

def image_search(subscription_key):
    """ImageSearch.

    This will search images for (canadian rockies) then verify number of results and print out first image result, pivot suggestion, and query expansion.
    """
    client = ImageSearchClient(
        endpoint=ENDPOINT,
        credentials=CognitiveServicesCredentials(subscription_key)
    )

    try:
        image_results = client.images.search(query="canadian rockies")
        print("Search images for query \"canadian rockies\"")

        # Image results
        if image_results.value:
            first_image_result = image_results.value[0]
            print("Image result count: {}".format(len(image_results.value)))
            print("First image insights token: {}".format(
                first_image_result.image_insights_token))
            print("First image thumbnail url: {}".format(
                first_image_result.thumbnail_url))
            print("First image content url: {}".format(
                first_image_result.content_url))
        else:
            print("Couldn't find image results!")

        print("Image result total estimated matches: {}".format(
            image_results.total_estimated_matches))
        print("Image result next offset: {}".format(image_results.next_offset))

        # Pivot suggestions
        if image_results.pivot_suggestions:
            first_pivot = image_results.pivot_suggestions[0]
            print("Pivot suggestion count: {}".format(
                len(image_results.pivot_suggestions)))
            print("First pivot: {}".format(first_pivot.pivot))

            if first_pivot.suggestions:
                first_suggestion = first_pivot.suggestions[0]
                print("Suggestion count: {}".format(
                    len(first_pivot.suggestions)))
                print("First suggestion text: {}".format(first_suggestion.text))
                print("First suggestion web search url: {}".format(
                    first_suggestion.web_search_url))
            else:
                print("Couldn't find suggestions!")
        else:
            print("Couldn't find pivot suggestions!")

        # Query expansions
        if image_results.query_expansions:
            first_query_expansion = image_results.query_expansions[0]
            print("Query expansion count: {}".format(
                len(image_results.query_expansions)))
            print("First query expansion text: {}".format(
                first_query_expansion.text))
            print("First query expansion search link: {}".format(
                first_query_expansion.search_link))
        else:
            print("Couldn't find image results!")

    except Exception as err:
        print("Encountered exception. {}".format(err))


def image_search_with_filters(subscription_key):
    """ImageSearchWithFilters.

    This will search images for (studio ghibli), filtered for animated gifs and wide aspect, then verify number of results and print out insightsToken, thumbnail url and web url of first result.
    """
    client = ImageSearchClient(
        endpoint="https://api.cognitive.microsoft.com",
        credentials=CognitiveServicesCredentials(subscription_key)
    )

    try:
        image_results = client.images.search(
            query="studio ghibli",
            image_type=ImageType.animated_gif,  # Could be the str "AnimatedGif"
            aspect=ImageAspect.wide  # Could be the str "Wide"
        )
        print("Search images for \"studio ghibli\" results that are animated gifs and wide aspect")

        if image_results.value:
            first_image_result = image_results.value[0]
            print("Image result count: {}".format(len(image_results.value)))
            print("First image insights token: {}".format(
                first_image_result.image_insights_token))
            print("First image thumbnail url: {}".format(
                first_image_result.thumbnail_url))
            print("First image web search url: {}".format(
                first_image_result.web_search_url))
        else:
            print("Couldn't find image results!")

    except Exception as err:
        print("Encountered exception. {}".format(err))


def image_trending(subscription_key):
    """ImageTrending.

    This will search for trending images then verify categories and tiles.
    """
    client = ImageSearchClient(
        endpoint="https://api.cognitive.microsoft.com",
        credentials=CognitiveServicesCredentials(subscription_key)
    )

    try:
        trending_result = client.images.trending()
        print("Search trending images")

        # Categorires
        if trending_result.categories:
            first_category = trending_result.categories[0]
            print("Category count: {}".format(len(trending_result.categories)))
            print("First category title: {}".format(first_category.title))
            if first_category.tiles:
                first_tile = first_category.tiles[0]
                print("Subcategory tile count: {}".format(
                    len(first_category.tiles)))
                print("First tile text: {}".format(first_tile.query.text))
                print("First tile url: {}".format(
                    first_tile.query.web_search_url))
            else:
                print("Couldn't find subcategory tiles!")
        else:
            print("Couldn't find categories!")

    except Exception as err:
        print("Encountered exception. {}".format(err))


def image_detail(subscription_key):
    """ImageDetail.

    This will search images for (degas) and then search for image details of the first image.
    """
    client = ImageSearchClient(
        endpoint="https://api.cognitive.microsoft.com",
        credentials=CognitiveServicesCredentials(subscription_key)
    )

    try:
        image_results = client.images.search(query="degas")
        print("Search images for \"degas\"")

        first_image = image_results.value[0]

        image_detail = client.images.details(
            query="degas",
            insights_token=first_image.image_insights_token,
            modules=[
                ImageInsightModule.all  # Could be the str "all"
            ],

        )
        print("Search detail for image insights token: {}".format(
            first_image.image_insights_token))
        print("Expected image insights token: {}".format(
            image_detail.image_insights_token))

        # Best representative query
        if image_detail.best_representative_query:
            print("Best representative query text: {}".format(
                image_detail.best_representative_query.text))
            print("Best representative query web search url: {}".format(
                image_detail.best_representative_query.web_search_url))
        else:
            print("Couldn't find best representative query!")

        # Caption
        if image_detail.image_caption:
            print("Image caption: {}".format(
                image_detail.image_caption.caption))
            print("Image caption data source url: {}".format(
                image_detail.image_caption.data_source_url))
        else:
            print("Couldn't find image caption!")

        # Pages including the image
        if image_detail.pages_including.value:
            first_page = image_detail.pages_including.value[0]
            print("Pages including cound: {}".format(
                len(image_detail.pages_including.value)))
            print("First page content url: {}".format(first_page.content_url))
            print("First page name: {}".format(first_page.name))
            print("First page date published: {}".format(
                first_page.date_published))
        else:
            print("Couldn't find any pages including this image!")

        # Related searched
        if image_detail.related_searches.value:
            first_related_search = image_detail.related_searches.value[0]
            print("Related searches count: {}".format(
                len(image_detail.related_searches.value)))
            print("First related search text: {}".format(
                first_related_search.text))
            print("First related search web search url: {}".format(
                first_related_search.web_search_url))
        else:
            print("Couldn't find any related searches!")

        # Visually similar images
        if image_detail.visually_similar_images.value:
            first_visually_similar_images = image_detail.visually_similar_images.value[0]
            print("Visually similar images count: {}".format(
                len(image_detail.visually_similar_images.value)))
            print("First visually similar image name: {}".format(
                first_visually_similar_images.name))
            print("First visually similar image content url: {}".format(
                first_visually_similar_images.content_url))
            print("First visually similar image content size: {}".format(
                first_visually_similar_images.content_size))
        else:
            print("Couldn't find any visually similar images!")

        # Image tags:
        if image_detail.image_tags.value:
            first_image_tag = image_detail.image_tags.value[0]
            print("Image tags count: {}".format(
                len(image_detail.image_tags.value)))
            print("First tag name: {}".format(first_image_tag.name))
        else:
            print("Couldn't find any image tags!")

    except Exception as err:
        print("Encountered exception. {}".format(err))


if __name__ == "__main__":
    import sys, os.path
    sys.path.append(os.path.abspath(os.path.join(__file__, "..", "..", "..")))    
    from samples.tools import execute_samples
    execute_samples(globals(), SUBSCRIPTION_KEY)
