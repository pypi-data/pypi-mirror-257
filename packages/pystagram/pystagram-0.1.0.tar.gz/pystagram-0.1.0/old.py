from requests import request, HTTPError, Timeout, TooManyRedirects


class FacebookGraphAPI(object):
    """ Facebook Graph API Wrapper."""

    def __init__(self, api_url=None, api_version=None, app_id=None, app_secret=None, access_token=None):
        """ Initializes the Facebook Graph API.
        :param api_url: The URL of the Facebook Graph API.
        :param api_version: The version of the Facebook Graph API.
        :param app_id: The ID of the Facebook App.
        :param app_secret: The secret of the Facebook App.
        :param access_token: The access token of the Facebook App.
        """

        self.api_url = api_url
        self.api_version = api_version
        self.app_id = app_id
        self.app_secret = app_secret
        self._access_token = access_token
        self.instagram_id = self.get_instagram_account_id()

    def api_request(self, method, endpoint, params=None, element=None):
        """ Makes a request to the Facebook Graph API.
        :param method: The HTTP method to use (GET, POST, etc.)
        :param endpoint: The endpoint to request (/me, /oauth/access_token, etc.)
        :param params: A dictionary of parameters to send with the request.
        :param element: The element to return from the response.
        :return: The response from the API or the encountered error .
        """

        url = self.api_url + self.api_version + endpoint

        try:
            response = request(
                url=url,
                method=method,
                params=params)

            response.raise_for_status()

            if element:
                response = response.json().get(element)

        except HTTPError as err:
            response = err
        except Timeout as err:
            response = err
        except TooManyRedirects as err:
            response = err
        except Exception as err:
            response = err

        return response

    def get_token_expiration(self):
        """ Fetches the expiration of the actual access token."""

        response = self.api_request(
            method="GET",
            endpoint="/oauth/access_token",
            params={
                'grant_type': 'fb_exchange_token',
                'client_id': self.app_id,
                'client_secret': self.app_secret,
                'fb_exchange_token': self._access_token
            }
        )

        return response

    def get_long_lived_access_token(self, access_token):
        """ Fetches and replace the current access token with a long lived access token.
        :param access_token: The short lived access token.
        """

        response = self.api_request(
            method="GET",
            endpoint="/oauth/access_token",
            params={
                'grant_type': 'fb_exchange_token',
                'client_id': self.app_id,
                'client_secret': self.app_secret,
                'fb_exchange_token': access_token
            },
            element="access_token"
        )

        self._access_token = response
        return response

    def get_instagram_account_id(self):
        """ Fetches the Instagram Business Account id linked to the Facebook Page."""

        response = self.api_request(
            method="GET",
            endpoint="/me/accounts",
            params={
                'fields': 'instagram_business_account',
                'access_token': self._access_token
            },
            element="data"
        )

        return response[0]['instagram_business_account']['id']

    def create_image_container(self, image_url, is_carousel_item=False, caption="", location=None, user_tags=None,
                               product_tags=None):
        """ Creates a containers for the image to be uploaded.
        :param image_url: The path to the image. We will cURL the image using the URL that you specify so the image must be on a public server.
        :param is_carousel_item: Boolean value to indicate if the image is part of a carousel.
        :param caption: A caption for the image, video, or carousel. Can include hashtags (example: #crazywildebeest) and usernames of Instagram users (example: @natgeo). @Mentioned Instagram users receive a notification when the containers is published. Maximum 2200 characters, 30 hashtags, and 20 @ tags.
        :param location: The ID of a Page associated with a location that you want to tags the image or video with.
        :param user_tags: Applies only to images and carousels. An array of public usernames and x/y coordinates for any public Instagram users who you want to tags in the image.
        :param product_tags: The product tags of the image.
        :return: The ID of the image containers.
        """

        response = self.api_request(
            method="POST",
            endpoint=f"/{self.instagram_id}/media",
            params={
                "image_url": image_url,
                "is_carousel_item": is_carousel_item,
                "caption": caption,
                "location_id": location,
                "user_tags": user_tags,
                "product_tags": product_tags,
                "access_token": self._access_token
            },
            element="id"
        )

        return response

    def create_video_container(self, video_url, is_carousel_item=False, caption="", location=None, thumb_offset=0,
                               product_tags=None):
        """ Creates a containers for the video to be uploaded.
        :param video_url: Path to the video. We cURL the video using the passed-in URL, so it must be on a public server.
        :param is_carousel_item: Boolean value to indicate if the video is part of a carousel.
        :param caption: A caption for the image, video, or carousel. Can include hashtags (example: #crazywildebeest) and usernames of Instagram users (example: @natgeo). @Mentioned Instagram users receive a notification when the containers is published. Maximum 2200 characters, 30 hashtags, and 20 @ tags.
        :param location: The ID of a Page associated with a location that you want to tags the image or video with.
        :param thumb_offset: Location, in milliseconds, of the video or reel frame to be used as the cover thumbnail image. The default value is 0, which is the first frame of the video or reel. 
        :param product_tags: The product tags of the video.
        :return: The ID of the video containers.
        """

        response = self.api_request(
            method="POST",
            endpoint=f"/{self.instagram_id}/media",
            params={
                "media_type": "VIDEO",
                "video_url": video_url,
                "is_carousel_item": is_carousel_item,
                "caption": caption,
                "location_id": location,
                "thumb_offset": thumb_offset,
                "product_tags": product_tags,
                "access_token": self._access_token
            },
            element="id"
        )

        return response

    def create_reel_container(self, video_url, caption="", cover_url=None, location=None, thumb_offset=0,
                              share_to_feed=True):
        """ Creates a containers for the reel to be uploaded.
        :param video_url: Path to the video. We cURL the video using the passed-in URL, so it must be on a public server.
        :param caption: A caption for the image, video, or carousel. Can include hashtags (example: #crazywildebeest) and usernames of Instagram users (example: @natgeo). @Mentioned Instagram users receive a notification when the containers is published. Maximum 2200 characters, 30 hashtags, and 20 @ tags.
        :param location: The ID of a Page associated with a location that you want to tags the image or video with.
        :param thumb_offset: Location, in milliseconds, of the video or reel frame to be used as the cover thumbnail image. The default value is 0, which is the first frame of the video or reel. 
        :param share_to_feed: For Reels only. When true, indicates that the reel can appear in both the Feed and Reels tabs. When false, indicates the reel can only appear in the Reels tab.
        :return: The ID of the reel containers.
        """

        response = self.api_request(
            method="POST",
            endpoint=f"/{self.instagram_id}/media",
            params={
                "media_type": "REELS",
                "video_url": video_url,
                "caption": caption,
                "cover_url": cover_url,
                "location_id": location,
                "thumb_offset": thumb_offset,
                "share_to_feed ": share_to_feed,
                "access_token": self._access_token
            },
            element="id"
        )

        return response

    def create_carousel_container(self, children, caption="", location=None):
        """ Creates a containers for the carousel to be uploaded.
        :param children: An array of up to 10 containers IDs of each image and video that should appear in the published carousel. Carousels can have up to 10 total images, vidoes, or a mix of the two.
        :param caption: A caption for the carousel. Can include hashtags (example: #crazywildebeest) and usernames of Instagram users (example: @natgeo). @Mentioned Instagram users receive a notification when the containers is published. Maximum 2200 characters, 30 hashtags, and 20 @ tags.
        :param location: The ID of a Page associated with a location that you want to tags the carousel with.
        :return: The ID of the carousel containers.
        """

        response = self.api_request(
            method="POST",
            endpoint=f"/{self.instagram_id}/media",
            params={
                "media_type": "CAROUSEL",
                "caption": caption,
                "location_id": location,
                "children": children,
                "access_token": self._access_token
            },
            element="id"
        )

        return response

    def publish_container(self, container_id):
        """ Publishes the containers.
        :param container_id: The ID of the containers to be published.
        :return: The ID of the published containers.
        """

        response = self.api_request(
            method="POST",
            endpoint=f"/{self.instagram_id}/media_publish",
            params={
                "creation_id": container_id,
                "access_token": self._access_token
            },
            element="id"
        )

        return response

    def get_content_publishing_limit(self):
        """ Gets the content publishing limit for the account.
        :return: The content publishing limit for the account.
        """

        response = self.api_request(
            method="GET",
            endpoint=f"/{self.instagram_id}/media_publishing_limit",
            params={
                "fields": "quota_usage,rate_limit_settings",
                "access_token": self._access_token
            }
        )

        return response.get("config")["quota_total"] - response.get("quota_usage")
