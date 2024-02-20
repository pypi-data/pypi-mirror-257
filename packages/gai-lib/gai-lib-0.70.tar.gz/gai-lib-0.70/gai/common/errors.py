class ApiException(Exception):
    def __init__(self, status_code, code, message, url):
        self.status_code = status_code
        self.code = code
        self.url = url
        super().__init__(message)

class InternalException(Exception):
    def __init__(self, error_id):
        self.status_code = 500
        self.code = "uknown_error"
        self.id = error_id
        super().__init__(message="An unexpected error occurred. Please try again later.")

class ContextLengthExceededException(Exception):
    def __init__(self):
        self.status_code = 400
        self.code = "context_length_exceeded"
        super().__init__(message="The message has exceeded the model's context length.")

class GeneratorMismatchException(Exception):
    def __init__(self):
        self.status_code = 400
        self.code = "generator_mismatch"
        super().__init__(message="The model does not correspond to this service.")

