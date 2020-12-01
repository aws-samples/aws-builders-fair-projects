import asyncio
import json
import re
import uuid
from typing import Sequence

from .data import ResponseStatusCode
from .exceptions import (
    InvalidRequestException,
    MessageStoreReadErrorException,
    NotEnoughMessagesException,
    RequestPayloadTooLargeException,
    ResourceNotFoundException,
    ResponsePayloadTooLargeException,
    ServerOutOfMemoryException,
    ServerTimeoutException,
    StreamManagerException,
    UnauthorizedException,
    UnknownFailureException,
    UnknownOperationException,
    UpdateFailedException,
    UpdateNotAllowedException,
)


class UtilInternal:
    __ENDIAN = "big"
    _MAX_PACKET_SIZE = 1 << 30

    @staticmethod
    def sync(coro, loop: asyncio.AbstractEventLoop):
        if asyncio.iscoroutine(coro):
            # Run async function in the loop and return the value or raise the exception
            return asyncio.run_coroutine_threadsafe(coro, loop=loop).result()

        return coro

    """
    Delete keys with the value ``None`` in a dictionary, recursively.
    This alters the input so you may wish to ``copy`` the dict first.
    """

    @staticmethod
    def del_empty_arrays(d):

        for key, value in list(d.items()):
            if isinstance(value, list) and len(value) == 0:
                del d[key]
            elif isinstance(value, dict):
                UtilInternal.del_empty_arrays(value)
        return d

    @staticmethod
    def serialize_to_json_with_empty_array_as_null(data):
        s = json.dumps(UtilInternal.del_empty_arrays(data.as_dict()))

        return s.encode()

    @staticmethod
    def int_to_bytes(i, length=4):
        return int.to_bytes(i, length=length, byteorder=UtilInternal.__ENDIAN, signed=True)

    @staticmethod
    def int_from_bytes(b):
        return int.from_bytes(b, byteorder=UtilInternal.__ENDIAN, signed=True)

    @staticmethod
    def encode_frame(frame) -> Sequence[bytes]:
        if len(frame.payload) + 1 > UtilInternal._MAX_PACKET_SIZE:
            raise RequestPayloadTooLargeException()
        return [
            bytes(
                [
                    *UtilInternal.int_to_bytes(len(frame.payload) + 1),
                    *UtilInternal.int_to_bytes(frame.operation.value, length=1),
                ]
            ),
            frame.payload,
        ]

    @staticmethod
    def get_request_id():
        return str(uuid.uuid4())

    @staticmethod
    def is_invalid(o):
        if not hasattr(o, "_validations_map"):
            return False
        if not hasattr(o, "_types_map"):
            return False
        for prop_name, validations in o._validations_map.items():
            if not hasattr(o, prop_name):
                return "Object is malformed, missing property: {}".format(prop_name)
            # Validate all properties on lists
            if type(getattr(o, prop_name)) == list:
                for i, v in enumerate(getattr(o, prop_name)):
                    result = UtilInternal.is_invalid(v)
                    if result:
                        return "Property {}[{}] is invalid because {}".format(prop_name, i, result)

            # Recurse down to check validity of objects within objects
            result = UtilInternal.is_invalid(getattr(o, prop_name))
            if result:
                return "Property {} is invalid because {}".format(prop_name, result)

            # Validate the property
            if "required" in validations and validations["required"] and getattr(o, prop_name) is None:
                return "Property {} is required, but was None".format(prop_name)
            if (
                "minLength" in validations
                and getattr(o, prop_name) is not None
                and len(getattr(o, prop_name)) < validations["minLength"]
            ):
                return "Property {} must have a minimum length of {}, but found length of {}".format(
                    prop_name, validations["minLength"], len(getattr(o, prop_name))
                )
            if (
                "maxLength" in validations
                and getattr(o, prop_name) is not None
                and len(getattr(o, prop_name)) > validations["maxLength"]
            ):
                return "Property {} must have a maximum length of {}, but found length of {}".format(
                    prop_name, validations["maxLength"], len(getattr(o, prop_name))
                )
            if (
                "minItems" in validations
                and getattr(o, prop_name) is not None
                and len(getattr(o, prop_name)) < validations["minItems"]
            ):
                return "Property {} must have at least {} items, but found {}".format(
                    prop_name, validations["minItems"], len(getattr(o, prop_name))
                )
            if (
                "maxItems" in validations
                and getattr(o, prop_name) is not None
                and len(getattr(o, prop_name)) > validations["maxItems"]
            ):
                return "Property {} must have at most {} items, but found {}".format(
                    prop_name, validations["maxItems"], len(getattr(o, prop_name))
                )
            if (
                "maximum" in validations
                and getattr(o, prop_name) is not None
                and getattr(o, prop_name) > validations["maximum"]
            ):
                return "Property {} must be at most {}".format(prop_name, validations["maximum"])
            if (
                "minimum" in validations
                and getattr(o, prop_name) is not None
                and getattr(o, prop_name) < validations["minimum"]
            ):
                return "Property {} must be at least {}".format(prop_name, validations["minimum"])
            if (
                "pattern" in validations
                and getattr(o, prop_name) is not None
                and re.fullmatch(validations["pattern"], getattr(o, prop_name)) is None
            ):
                return "Property {} must match regex {}".format(prop_name, validations["pattern"])

        for prop_name, types in o._types_map.items():
            # Validate all properties with their respective types
            if "type" in types and getattr(o, prop_name) is not None:
                result = isinstance(getattr(o, prop_name), types["type"])
                if not result:
                    return "Property {} is invalid because it must be of type {}".format(
                        prop_name, types["type"].__name__
                    )
                if types["type"] == list and "subtype" in types:
                    for i, v in enumerate(getattr(o, prop_name)):
                        result = isinstance(v, types["subtype"])
                        if not result:
                            return "Property {}[{}] is invalid because it must be of type {}".format(
                                prop_name, i, types["subtype"].__name__
                            )

        return False

    @staticmethod
    def raise_on_error_response(response):
        if response.status == ResponseStatusCode.Success:
            return
        elif response.status == ResponseStatusCode.InvalidRequest:
            raise InvalidRequestException(response.error_message, response.status, response.request_id)
        elif response.status == ResponseStatusCode.RequestPayloadTooLarge:
            raise RequestPayloadTooLargeException(response.error_message, response.status, response.request_id)
        elif response.status == ResponseStatusCode.ResourceNotFound:
            raise ResourceNotFoundException(response.error_message, response.status, response.request_id)
        elif response.status == ResponseStatusCode.ResponsePayloadTooLarge:
            raise ResponsePayloadTooLargeException(response.error_message, response.status, response.request_id)
        elif response.status == ResponseStatusCode.ServerTimeout:
            raise ServerTimeoutException(response.error_message, response.status, response.request_id)
        elif response.status == ResponseStatusCode.Unauthorized:
            raise UnauthorizedException(response.error_message, response.status, response.request_id)
        elif response.status == ResponseStatusCode.UnknownFailure:
            raise UnknownFailureException(response.error_message, response.status, response.request_id)
        elif response.status == ResponseStatusCode.NotEnoughMessages:
            raise NotEnoughMessagesException(response.error_message, response.status, response.request_id)
        elif response.status == ResponseStatusCode.MessageStoreReadError:
            raise MessageStoreReadErrorException(response.error_message, response.status, response.request_id)
        elif response.status == ResponseStatusCode.OutOfMemoryError:
            raise ServerOutOfMemoryException(response.error_message, response.status, response.request_id)
        elif response.status == ResponseStatusCode.UpdateFailed:
            raise UpdateFailedException(response.error_message, response.status, response.request_id)
        elif response.status == ResponseStatusCode.UpdateNotAllowed:
            raise UpdateNotAllowedException(response.error_message, response.status, response.request_id)
        elif response.status == ResponseStatusCode.UnknownOperation:
            raise UnknownOperationException(response.error_message, response.status, response.request_id)
        else:
            raise StreamManagerException(
                "Client is not able to understand this server response status code", "Unrecognized", response.request_id
            )
