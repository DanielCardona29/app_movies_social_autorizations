from flask import Blueprint, request
from ...services.twitter_auth_services.twitter_oauth import getOauthTokenFromTwitter
from ...services.twitter_auth_services.twitter_oauth_access_token import twitterTokenValidate

routes = Blueprint('auth_twitter_blueprint', __name__)

@routes.route('/auth', methods=['GET'])
def twitterAuth():
  return getOauthTokenFromTwitter();

@routes.route('/access-token', methods=['POST'])
def twitterTokenConfirm():
  try:
    #body has been build like {verifier..., oauth_token...}
    body = request.get_json();
    twitter_auth = twitterTokenValidate(body['oauth-token'], body['verifier']);
    return twitter_auth.init()
  except ValueError:
    return 'Error'