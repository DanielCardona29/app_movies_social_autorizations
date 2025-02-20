import requests
from decouple import config
from requests_oauthlib import OAuth1

from src.utils.constants import TWITTER_TOKEN_INVALIDATE_TOKEN_URL
from src.utils.services_response_dto.response_dto import responseDto

responseController = responseDto()


class twitterTokenInvalidate:
    '''
        Validate the token and secret of the user to invalidate the token
        Returns a response from the twitter API
    '''
    TWITTER_API_KEY: str = config("TWITTER_API_KEY")
    TWITTER_API_KEY_SECRET: str = config("TWITTER_API_KEY_SECRET")

    def __init__(self, authorize_token: str, authorize_token_secret: str) -> None:
        self.authorize_token = authorize_token
        self.authorize_token_secret = authorize_token_secret
        pass

    def makeARequest(self):
        oauth = OAuth1(
            self.TWITTER_API_KEY,
            self.TWITTER_API_KEY_SECRET,
            self.authorize_token,
            self.authorize_token_secret,
        )
        response = requests.post(TWITTER_TOKEN_INVALIDATE_TOKEN_URL, auth=oauth, timeout=5)
        return response

    def handleServiceResponse(self):
        response = self.makeARequest()
        if response.status_code == 200:
            return response.json()
        else:
            return responseController.errorOnService(
                response.status_code, response.json()
            )

    def init(self):
        try:
            return self.handleServiceResponse()
        except ValueError:
            return responseController.unknownError()
