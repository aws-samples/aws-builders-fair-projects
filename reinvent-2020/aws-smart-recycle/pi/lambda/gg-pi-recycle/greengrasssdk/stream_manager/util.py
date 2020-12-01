import json

from .exceptions import ValidationException
from .utilinternal import UtilInternal


"""
Util functions exposed to the customers
"""


class Util:
    """
    Validate And Serialize an instance of class to Json bytes.
    :param data: an instance object
    :return: a byte array.
    :raises: :ValidationException
    """

    @staticmethod
    def validate_and_serialize_to_json_bytes(data):
        validation = UtilInternal.is_invalid(data)
        if validation:
            raise ValidationException(validation)
        return UtilInternal.serialize_to_json_with_empty_array_as_null(data)

    """
    Deserialize the json byte array to an object
    :param :bytes byte array of data
    :param :type instance class type
    :return: an object.
    """

    @staticmethod
    def deserialize_json_bytes_to_obj(bytes, type):
        return type.from_dict(json.loads(bytes))
