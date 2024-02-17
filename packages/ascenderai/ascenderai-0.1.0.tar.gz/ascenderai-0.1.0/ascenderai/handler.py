from aiohttp import ClientResponse
from ascenderai.errors import BaseAscenderAIException, ContextWindowExceededError, GatewayTimeoutError, InternalServerError, InvalidRequestFormatError, ServiceUnavailableError


class AscenderExceptionManager:
    def __init__(self, model: str) -> None:
        self.model = model
    
    def listen_for_errors(self, object: str, response: ClientResponse):
        handler = AscenderErrorHandler(object, self.model)
        handler(response)

class AscenderErrorHandler:
    def __init__(self, object: str, model: str) -> None:
        self.object = object
        self.model = model

    def __call__(self, response: ClientResponse) -> None:
        if response.status == 200:
            return
        
        match response.status:
            case 429:
                raise ContextWindowExceededError(self.object, self.model, response.reason)
            case 422:
                raise InvalidRequestFormatError(self.object, self.model, response.reason)
            case 500:
                raise InternalServerError(self.object, self.model)
            case 503:
                raise ServiceUnavailableError(self.object, self.model)
            case 504:
                raise GatewayTimeoutError(self.object, self.model)
            case _:
                raise BaseAscenderAIException(self.object, self.model, f"HTTP {response.status}: {response.reason}")