class StreamManagerException(Exception):
    def __init__(self, message="", status=None, request_id=None):
        super().__init__(message)
        self.status = status
        self.request_id = request_id
        self.message = message


class ClientException(StreamManagerException):
    pass


class ValidationException(ClientException):
    pass


class ConnectFailedException(ClientException):
    pass


class InvalidRequestException(StreamManagerException):
    pass


class RequestPayloadTooLargeException(StreamManagerException):
    pass


class ResourceNotFoundException(StreamManagerException):
    pass


class ResponsePayloadTooLargeException(StreamManagerException):
    pass


class ServerTimeoutException(StreamManagerException):
    pass


class UnauthorizedException(StreamManagerException):
    pass


class UnknownFailureException(StreamManagerException):
    pass


class NotEnoughMessagesException(StreamManagerException):
    pass


class MessageStoreReadErrorException(StreamManagerException):
    pass


class ServerOutOfMemoryException(StreamManagerException):
    pass


class UpdateFailedException(StreamManagerException):
    pass


class UnknownOperationException(StreamManagerException):
    pass


class UpdateNotAllowedException(InvalidRequestException):
    pass
