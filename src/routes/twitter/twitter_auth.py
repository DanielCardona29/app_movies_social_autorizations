from flask import Blueprint, request

from src.services.twitter_auth_services.twitter_invalidate_token import (
    twitterTokenInvalidate,
)
from src.utils.services_response_dto.response_dto import responseDto
from ...services.twitter_auth_services.twitter_oauth import twitterOauthValidate
from ...services.twitter_auth_services.twitter_oauth_access_token import (
    twitterTokenValidate,
)

routes = Blueprint("auth_twitter_blueprint", __name__)

responseController = responseDto()


@routes.route("/auth", methods=["GET"])
def twitterAuth():
    try:
        twitter_oauth_validate = twitterOauthValidate()
        return twitter_oauth_validate.init()
    except SyntaxError:
        return responseController.syntaxError()
    except ValueError:
        return responseController.valueError()
    except Exception:
        return responseController.unknownError()


@routes.route("/access-token", methods=["POST"])
def twitterTokenConfirm():
    try:
        # body has been build like {verifier..., oauth_token...}
        body = request.get_json()
        twitter_auth = twitterTokenValidate(body["oauth_token"], body["verifier"])
        return twitter_auth.init()
    except SyntaxError:
        return responseController.syntaxError()
    except ValueError:
        return responseController.valueError()
    except Exception:
        return responseController.unknownError()


@routes.route("/invalidate-token", methods=["POST"])
def twitterInvalidateToken():
    try:
        body = request.get_json()
        twitter_invalidate = twitterTokenInvalidate(body["authorize_token"], body["authorize_token_secret"])
        response = twitter_invalidate.init()
        return response
    except SyntaxError:
        return responseController.syntaxError()
    except ValueError:
        return responseController.valueError()
    except Exception:
        return responseController.unknownError()
