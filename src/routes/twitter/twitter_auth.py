from flask import Blueprint
from ...services.twitter_auth_services.twitter_oauth import getOauthTokenFromTwitter

routes = Blueprint('auth_twitter_blueprint', __name__)

@routes.route('/auth', methods=['GET'])
def twitterAuth():
  return getOauthTokenFromTwitter();

@routes.route('/access-token', methods=['GET'])
def twitterTokenConfirm():
  return 'it works'