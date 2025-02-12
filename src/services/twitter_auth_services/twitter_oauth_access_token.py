import requests
from decouple import config
from ...utils.constants import TWITTER_TOKEN_ACCESS_URL

from ...utils.services_response_dto.response_dto import responseDto

responseController = responseDto()


class twitterTokenValidate:
    TWITTER_API_KEY = config("TWITTER_API_KEY")
    TWITTER_API_KEY_SECRET = config("TWITTER_API_KEY_SECRET")

    def __init__(self, oauth_token, oauth_verifier) -> None:
        self.oauth_token = oauth_token
        self.oauth_verifier = oauth_verifier

    def requestTokenToTwitter(self):
        params = {
            "oauth_token": self.oauth_token,
            "oauth_verifier": self.oauth_verifier,
        }
        return requests.post(TWITTER_TOKEN_ACCESS_URL, params=params)

    def init(self):
        try:
            response = self.requestTokenToTwitter()
            if response.status_code == 200:
                credentials = dict(x.split("=") for x in response.text.split("&"))
                credentials = {
                    "authorize_token": credentials["oauth_token"],
                    "authorize_token_secret": credentials["oauth_token_secret"],
                    "user_id": credentials["user_id"],
                    "screen_name": credentials["screen_name"],
                }
                return responseController.response(
                    credentials, "success", response.status_code
                )
            else:
                return responseController.errorOnService(
                    response.status_code, error=response.text
                )
        except ValueError:
            return responseController.unknownError()
