import requests
from decouple import config
from requests_oauthlib import OAuth1

from ...utils.constants import TWITTER_URL_AUTHENTICATE, TWITTER_TOKEN_REQUEST_URL
from ...utils.services_response_dto.response_dto import responseDto

responseController = responseDto()


class twitterOauthValidate:
    TWITTER_API_KEY: str = config("TWITTER_API_KEY")
    TWITTER_API_KEY_SECRET: str = config("TWITTER_API_KEY_SECRET")

    def makeARequest(self):
        oauth = OAuth1(self.TWITTER_API_KEY, self.TWITTER_API_KEY_SECRET)
        return requests.post(TWITTER_TOKEN_REQUEST_URL, auth=oauth)

    def handleServiceResponse(self):
        # request the auth token service
        response = self.makeARequest()
        if response.status_code == 200:
            credentials = dict(x.split("=") for x in response.text.split("&"))
            credentials = {
                "oauth_token": credentials["oauth_token"],
                "oauth_token_secret": credentials['oauth_token_secret'],
                "url": TWITTER_URL_AUTHENTICATE + credentials["oauth_token"],
            }
            return responseController.response(
                credentials, "success", response.status_code
            )
        else:
            return responseController.errorOnService(response.status_code, response.json())

    def init(self):
        try:
            # response the service
            return self.handleServiceResponse()
        except SyntaxError:
            return responseController.unknownError()
