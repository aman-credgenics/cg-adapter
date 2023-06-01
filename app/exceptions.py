

class CustomError(Exception):
    def __init__(self, message: str, code: str, data: dict = None):
        super().__init__(message)
        self.message = message
        self.code = code
        self.data = data

    def __str__(self):
        return f"Error occurred while processing request: {self.message} | {self.code}"

class ARIConnectionException(CustomError):
    def __init__(self, message: str = "ARI Connection Error", code: str = "ARI424", data: dict = None):
        super().__init__(message, code, data)