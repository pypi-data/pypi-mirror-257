from http.client import HTTPException

class ApiException(HTTPException):
    def __init__(self, status_code, code, message, url=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.status_code = status_code
        self.detail = {
            "code": code,
            "message": message,
            "url": url
        }

class InternalException(HTTPException):
    def __init__(self, error_id, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.status_code = 500
        self.detail = {
            "code": "unknown_error",
            "message": "An unexpected error occurred. Please try again later.",
            "id": error_id,
        }

class ContextLengthExceededException(Exception):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)    
        self.status_code = 400
        self.detail={
            "code": "context_length_exceeded",
            "message": "The context length exceeded the maximum allowed length."
        }

class GeneratorMismatchException(Exception):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)    
        self.status_code = 400
        self.detail={
            "code": "generator_mismatch",
            "message": "The model does not correspond to this service."
        }

class UserNotFoundException(Exception):
    def __init__(self,user_id=None, *args, **kwargs):
        super().__init__(*args, **kwargs)    
        self.status_code = 404
        self.detail={
            "code": "user_not_found",
            "message": "User not found"
        }
        if (user_id):
            self.detail["message"] = f"User {user_id} not found"

class MessageNotFoundException(Exception):
    def __init__(self,message_id=None, *args, **kwargs):
        super().__init__(*args, **kwargs)    
        self.status_code = 404
        self.detail={
            "code": "message_not_found",
            "message": "Message not found"
        }
        if (message_id):
            self.detail["message"] = f"Message {message_id} not found"


