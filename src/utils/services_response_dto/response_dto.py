from flask import jsonify

MESSAGE = {
  "error": "has been an error please try again",
  "success": "service has been a successful response",
  "unknown": "this error is unknown please try again"
}
class responseDto:  
  def response(self, response: dict, message: str, code: int) -> dict:
    return jsonify({
      "message": MESSAGE[message],
      "code":  code,
      "data": response
    }), code
    
  def errorOnService(self, code:int, error:dict={}) -> dict:
    return jsonify({
      "message": MESSAGE["error"],
      "code": code,
      "data": error
    }), code
  
  
  def unknownError(self) -> dict:
    return jsonify({
      "message": MESSAGE["unknown"],
      "code": 500,
    }), 500 