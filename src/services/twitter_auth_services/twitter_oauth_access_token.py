import requests
from decouple import config
from requests_oauthlib import OAuth1
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
    
    def getUserinfo(self, oauth_token, oauth_token_secret):
        url = "https://api.twitter.com/1.1/account/verify_credentials.json?include_email=true"
        auth = OAuth1(self.TWITTER_API_KEY, self.TWITTER_API_KEY_SECRET, oauth_token, oauth_token_secret)
        response = requests.get(url, auth=auth)
        return response.json()

    def buildReponse(self, response):
        '''Build the response to be returned to the user'''

        credentials = dict(x.split("=") for x in response.text.split("&"))
        user_data = self.getUserinfo(credentials["oauth_token"], credentials["oauth_token_secret"])
        data = {
            "credentials": {
                "authorize_token": credentials["oauth_token"],
                "authorize_token_secret": credentials["oauth_token_secret"],
                "user_id": credentials["user_id"],
                "screen_name": credentials["screen_name"],
            },
            "user_data": {
                "email": user_data['email'],
                "name": user_data['name'],
                "images": {
                    "profile": user_data['profile_image_url_https'],
                    "banner": user_data['profile_banner_url'],
                }
            },
        }
        return data

    def init(self):
        try:
            response = self.requestTokenToTwitter()
            if response.status_code == 200:
                return responseController.response(
                    self.buildReponse(response), "success", response.status_code
                )
            else:
                return responseController.errorOnService(
                    response.status_code, error=response.text
                )
        except ValueError:
            return responseController.unknownError()
