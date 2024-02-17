class BaseAscenderAIException(Exception):
    object: str
    model: str

    def __init__(self, object: str, model: str, *args, **kwargs) -> None:
        self.object = object
        self.model = model
        super().__init__(*args, **kwargs)

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(object={self.object!r}, model={self.model!r})"

class ContextWindowExceededError(BaseAscenderAIException):
    def __init__(self, object: str, model: str, message: str) -> None:
        self.message = message
        super().__init__(object, model)

    def __str__(self) -> str:
        return f"HTTP 429: {self.message}"


class InvalidRequestFormatError(BaseAscenderAIException):
    def __init__(self, object: str, model: str, reason: str) -> None:
        self.reason = reason
        super().__init__(object=object, model=model)
    
    def __str__(self) -> str:
        return f"HTTP 422: {self.reason}"


class InternalServerError(BaseAscenderAIException):
    def __str__(self) -> str:
        return "HTTP 500: Internal server error, please try again or contact your AscenderAI Cluster Provider."


class ServiceUnavailableError(BaseAscenderAIException):
    def __str__(self) -> str:
        return "HTTP 503: Services of AscenderAI Cluster aren't available currently, please try again later."
    

class GatewayTimeoutError(BaseAscenderAIException):
    def __str__(self) -> str:
        return "HTTP 504: Gateway Timeout, please try again later."