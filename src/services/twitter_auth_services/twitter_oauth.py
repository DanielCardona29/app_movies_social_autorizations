import requests
from decouple import config
from requests_oauthlib import OAuth1

from ...utils.constants import TWITTER_URL_AUTHENTICATE, TWITTER_TOKEN_REQUEST_URL
from ...utils.services_response_dto.response_dto import responseDto

responseController = responseDto()

def makeARequest():
  TWITTER_API_KEY = config('API_KEY')
  TWITTER_API_KEY_SECRET = config('API_KEY_SECRET')
  oauth = OAuth1(TWITTER_API_KEY, TWITTER_API_KEY_SECRET)
  return requests.post(TWITTER_TOKEN_REQUEST_URL, auth=oauth)

def handleServiceResponse(response):
  if response.status_code == 200:
    credentials = dict(x.split("=") for x in  response.text.split("&"))
    credentials = {
      "oauth_token": credentials["oauth_token"],
      "url": TWITTER_URL_AUTHENTICATE + credentials["oauth_token"]             
    }
    return responseController.response(credentials, 'success', response.status_code)
  else:
    return responseController.errorOnService()
    
def getOauthTokenFromTwitter():
  try:
    #request the auth token service
    response = makeARequest()
    #response the service
    return handleServiceResponse(response)
  except:
    return responseController.unknownError()
    
      