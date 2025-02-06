from flask import jsonify

class responseDto:
  MESSAGE = {
    "error": "has been an error please try again",
    "success": "service has been a successful response",
    "unknown": "this error is unknown please try again"
  }
  
  def response(self, response: dict, message: str, code: int) -> dict:
    return jsonify({
      "message": self.MESSAGE[message],
      "code":  code,
      "data": response
    })
    
  def errorOnService(self, code:int ) -> dict:
    return jsonify({
      "message": self.MESSAGE["error"],
      "code": code,
    })
  
  
  def unknownError(self) -> dict:
    return jsonify({
      "message": self.MESSAGE["unknown"],
      "code": 104,
    })