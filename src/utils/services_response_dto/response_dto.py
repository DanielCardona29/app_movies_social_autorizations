from flask import jsonify

MESSAGE = {
    "error": "has been an error please try again",
    "success": "service has been a successful response",
    "unknown": "this error is unknown please try again",
    "value": "has a error on value",
    "syntax": "has an error on system",
}


class responseDto:
    def response(self, response: dict, message: str, code: int) -> dict:
        return jsonify(
            {"message": MESSAGE[message], "code": code, "data": response}
        ), code

    def errorOnService(self, code: int, error: dict = {}) -> dict:
        return jsonify({"message": MESSAGE["error"], "code": code, "data": error}), code

    def unknownError(self) -> dict:
        return jsonify({"message": MESSAGE["unknown"], "code": 500}), 500

    def valueError(self) -> dict:
        return jsonify({"message": MESSAGE["value"], "code": 500}), 500

    def syntaxError(self) -> dict:
        return jsonify({"message": MESSAGE["syntax"], "code": 500}), 500
