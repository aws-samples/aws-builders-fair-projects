from reprlib import repr as limitedRepr


import enum
from typing import List


class VersionInfo(enum.Enum):
    """
    (Internal Only) Version information.
    """

    PROTOCOL_VERSION = "1.1.0"

    @staticmethod
    def from_dict(d):
        return VersionInfo(d)

    def as_dict(self):
        return self.value

    def __repr__(self):
        return "<Enum VersionInfo. {}: {}>".format(
            limitedRepr(self.name), limitedRepr(self.value)
        )


class ConnectRequest:
    """
    (Internal Only) Request object to connect to the service.
    """

    __slots__ = [
        "__request_id",
        "__protocol_version",
        "__other_supported_protocol_versions",
        "__sdk_version",
        "__auth_token",
    ]

    _types_map = {
        "request_id": {"type": str, "subtype": None},
        "protocol_version": {"type": str, "subtype": None},
        "other_supported_protocol_versions": {"type": list, "subtype": str},
        "sdk_version": {"type": str, "subtype": None},
        "auth_token": {"type": str, "subtype": None},
    }
    _formats_map = {}
    _validations_map = {
        "request_id": {"required": True, "minLength": 1, "pattern": "^[\w ,.\-_]*$",},
        "protocol_version": {"required": True,},
        "other_supported_protocol_versions": {"required": False,},
        "sdk_version": {"required": False,},
        "auth_token": {"required": False,},
    }

    def __init__(
        self,
        request_id: str = None,
        protocol_version: str = None,
        other_supported_protocol_versions: List[str] = None,
        sdk_version: str = None,
        auth_token: str = None,
    ):
        pass
        self.__request_id = request_id
        self.__protocol_version = protocol_version
        self.__other_supported_protocol_versions = other_supported_protocol_versions
        self.__sdk_version = sdk_version
        self.__auth_token = auth_token

    def _get_request_id(self):
        return self.__request_id

    def _set_request_id(self, value):
        if not isinstance(value, str):
            raise TypeError("request_id must be str")

        self.__request_id = value

    request_id = property(_get_request_id, _set_request_id)

    def _get_protocol_version(self):
        return self.__protocol_version

    def _set_protocol_version(self, value):
        if not isinstance(value, str):
            raise TypeError("protocol_version must be str")

        self.__protocol_version = value

    protocol_version = property(_get_protocol_version, _set_protocol_version)

    def _get_other_supported_protocol_versions(self):
        return self.__other_supported_protocol_versions

    def _set_other_supported_protocol_versions(self, value):
        if value is not None and not isinstance(value, list):
            raise TypeError("other_supported_protocol_versions must be list")
        if value is not None and not all(isinstance(i, str) for i in value):
            raise TypeError("other_supported_protocol_versions list values must be str")

        self.__other_supported_protocol_versions = value

    other_supported_protocol_versions = property(
        _get_other_supported_protocol_versions, _set_other_supported_protocol_versions
    )

    def _get_sdk_version(self):
        return self.__sdk_version

    def _set_sdk_version(self, value):
        if value is not None and not isinstance(value, str):
            raise TypeError("sdk_version must be str")

        self.__sdk_version = value

    sdk_version = property(_get_sdk_version, _set_sdk_version)

    def _get_auth_token(self):
        return self.__auth_token

    def _set_auth_token(self, value):
        if value is not None and not isinstance(value, str):
            raise TypeError("auth_token must be str")

        self.__auth_token = value

    auth_token = property(_get_auth_token, _set_auth_token)

    @staticmethod
    def from_dict(d):
        v = {}
        if "requestId" in d:
            v["request_id"] = (
                str.from_dict(d["requestId"])
                if hasattr(str, "from_dict")
                else d["requestId"]
            )
        if "protocolVersion" in d:
            v["protocol_version"] = (
                str.from_dict(d["protocolVersion"])
                if hasattr(str, "from_dict")
                else d["protocolVersion"]
            )
        if "otherSupportedProtocolVersions" in d:
            v["other_supported_protocol_versions"] = [
                str.from_dict(p) if hasattr(str, "from_dict") else p
                for p in d["otherSupportedProtocolVersions"]
            ]
        if "sdkVersion" in d:
            v["sdk_version"] = (
                str.from_dict(d["sdkVersion"])
                if hasattr(str, "from_dict")
                else d["sdkVersion"]
            )
        if "authToken" in d:
            v["auth_token"] = (
                str.from_dict(d["authToken"])
                if hasattr(str, "from_dict")
                else d["authToken"]
            )
        return ConnectRequest(**v)

    def as_dict(self):
        d = {}
        if self.__request_id is not None:
            d["requestId"] = (
                self.__request_id.as_dict()
                if hasattr(self.__request_id, "as_dict")
                else self.__request_id
            )
        if self.__protocol_version is not None:
            d["protocolVersion"] = (
                self.__protocol_version.as_dict()
                if hasattr(self.__protocol_version, "as_dict")
                else self.__protocol_version
            )
        if self.__other_supported_protocol_versions is not None:
            d["otherSupportedProtocolVersions"] = [
                p.as_dict() if hasattr(p, "as_dict") else p
                for p in self.__other_supported_protocol_versions
            ]
        if self.__sdk_version is not None:
            d["sdkVersion"] = (
                self.__sdk_version.as_dict()
                if hasattr(self.__sdk_version, "as_dict")
                else self.__sdk_version
            )
        if self.__auth_token is not None:
            d["authToken"] = (
                self.__auth_token.as_dict()
                if hasattr(self.__auth_token, "as_dict")
                else self.__auth_token
            )
        return d

    def __repr__(self):
        return "<Class ConnectRequest. request_id: {}, protocol_version: {}, other_supported_protocol_versions: {}, sdk_version: {}, auth_token: {}>".format(
            limitedRepr(
                self.__request_id[:20]
                if isinstance(self.__request_id, bytes)
                else self.__request_id
            ),
            limitedRepr(
                self.__protocol_version[:20]
                if isinstance(self.__protocol_version, bytes)
                else self.__protocol_version
            ),
            limitedRepr(
                self.__other_supported_protocol_versions[:20]
                if isinstance(self.__other_supported_protocol_versions, bytes)
                else self.__other_supported_protocol_versions
            ),
            limitedRepr(
                self.__sdk_version[:20]
                if isinstance(self.__sdk_version, bytes)
                else self.__sdk_version
            ),
            limitedRepr(
                self.__auth_token[:20]
                if isinstance(self.__auth_token, bytes)
                else self.__auth_token
            ),
        )


class ResponseStatusCode(enum.Enum):
    """
    (Internal Only) Enum defining possible response status codes from StreamManager server.
    Success: Request succeeded.
    UnknownFailure: Encountered unknown StreamManager server failure.
    Unauthorized: Client is not authorized to perform this request.
    InvalidRequest: Client request is invalid.
    RequestPayloadTooLarge: Request payload is too large.
    ResourceNotFound: The requested resource does not exist.
    ServerTimeout: Server took too long and timed out.
    ResponsePayloadTooLarge: Server response exceeded the max allowed response payload size by the protocol.
    UnsupportedConnectVersion: Server does not support the Connect version presented by the Client.
    UnexpectedOperation: Operation presented was not expected by the Server.
    UnsupportedProtocolVersion: Protocol version presented by the Client is not compatible with the Server.
    InvalidProtocolVersion: Protocol version presented by the Client is not valid.
    FailedToConnect: Client failed to connect to the Server.
    NotEnoughMessages: There is not enough messages to return.
    MessageStoreReadError: Read messages encountered an error.
    OutOfMemoryError: Server ran out of memory.
    UpdateFailed: Update operation failed.
    UpdateNotAllowed: One or more fields are not allowed to be updated.
    UnknownOperation: Client request is not recognized by the server.
    """

    Success = 0
    UnknownFailure = 1
    Unauthorized = 2
    InvalidRequest = 3
    RequestPayloadTooLarge = 4
    ResourceNotFound = 5
    ServerTimeout = 6
    ResponsePayloadTooLarge = 7
    UnsupportedConnectVersion = 8
    UnexpectedOperation = 9
    UnsupportedProtocolVersion = 10
    InvalidProtocolVersion = 11
    FailedToConnect = 12
    NotEnoughMessages = 13
    MessageStoreReadError = 14
    OutOfMemoryError = 15
    UpdateFailed = 16
    UpdateNotAllowed = 17
    UnknownOperation = 18

    @staticmethod
    def from_dict(d):
        return ResponseStatusCode(d)

    def as_dict(self):
        return self.value

    def __repr__(self):
        return "<Enum ResponseStatusCode. {}: {}>".format(
            limitedRepr(self.name), limitedRepr(self.value)
        )


class ConnectResponse:
    """
    Internal Only.
    """

    __slots__ = [
        "__request_id",
        "__status",
        "__error_message",
        "__protocol_version",
        "__supported_protocol_versions",
        "__server_version",
        "__client_identifier",
    ]

    _types_map = {
        "request_id": {"type": str, "subtype": None},
        "status": {"type": ResponseStatusCode, "subtype": None},
        "error_message": {"type": str, "subtype": None},
        "protocol_version": {"type": str, "subtype": None},
        "supported_protocol_versions": {"type": list, "subtype": str},
        "server_version": {"type": str, "subtype": None},
        "client_identifier": {"type": str, "subtype": None},
    }
    _formats_map = {}
    _validations_map = {
        "request_id": {"required": False, "minLength": 1, "pattern": "^[\w ,.\-_]*$",},
        "status": {"required": True,},
        "error_message": {"required": False,},
        "protocol_version": {"required": False,},
        "supported_protocol_versions": {"required": False,},
        "server_version": {"required": False,},
        "client_identifier": {"required": False,},
    }

    def __init__(
        self,
        request_id: str = None,
        status: ResponseStatusCode = None,
        error_message: str = None,
        protocol_version: str = None,
        supported_protocol_versions: List[str] = None,
        server_version: str = None,
        client_identifier: str = None,
    ):
        pass
        self.__request_id = request_id
        self.__status = status
        self.__error_message = error_message
        self.__protocol_version = protocol_version
        self.__supported_protocol_versions = supported_protocol_versions
        self.__server_version = server_version
        self.__client_identifier = client_identifier

    def _get_request_id(self):
        return self.__request_id

    def _set_request_id(self, value):
        if value is not None and not isinstance(value, str):
            raise TypeError("request_id must be str")

        self.__request_id = value

    request_id = property(_get_request_id, _set_request_id)

    def _get_status(self):
        return self.__status

    def _set_status(self, value):
        if not isinstance(value, ResponseStatusCode):
            raise TypeError("status must be ResponseStatusCode")

        self.__status = value

    status = property(_get_status, _set_status)

    def _get_error_message(self):
        return self.__error_message

    def _set_error_message(self, value):
        if value is not None and not isinstance(value, str):
            raise TypeError("error_message must be str")

        self.__error_message = value

    error_message = property(_get_error_message, _set_error_message)

    def _get_protocol_version(self):
        return self.__protocol_version

    def _set_protocol_version(self, value):
        if value is not None and not isinstance(value, str):
            raise TypeError("protocol_version must be str")

        self.__protocol_version = value

    protocol_version = property(_get_protocol_version, _set_protocol_version)

    def _get_supported_protocol_versions(self):
        return self.__supported_protocol_versions

    def _set_supported_protocol_versions(self, value):
        if value is not None and not isinstance(value, list):
            raise TypeError("supported_protocol_versions must be list")
        if value is not None and not all(isinstance(i, str) for i in value):
            raise TypeError("supported_protocol_versions list values must be str")

        self.__supported_protocol_versions = value

    supported_protocol_versions = property(
        _get_supported_protocol_versions, _set_supported_protocol_versions
    )

    def _get_server_version(self):
        return self.__server_version

    def _set_server_version(self, value):
        if value is not None and not isinstance(value, str):
            raise TypeError("server_version must be str")

        self.__server_version = value

    server_version = property(_get_server_version, _set_server_version)

    def _get_client_identifier(self):
        return self.__client_identifier

    def _set_client_identifier(self, value):
        if value is not None and not isinstance(value, str):
            raise TypeError("client_identifier must be str")

        self.__client_identifier = value

    client_identifier = property(_get_client_identifier, _set_client_identifier)

    @staticmethod
    def from_dict(d):
        v = {}
        if "requestId" in d:
            v["request_id"] = (
                str.from_dict(d["requestId"])
                if hasattr(str, "from_dict")
                else d["requestId"]
            )
        if "status" in d:
            v["status"] = (
                ResponseStatusCode.from_dict(d["status"])
                if hasattr(ResponseStatusCode, "from_dict")
                else d["status"]
            )
        if "errorMessage" in d:
            v["error_message"] = (
                str.from_dict(d["errorMessage"])
                if hasattr(str, "from_dict")
                else d["errorMessage"]
            )
        if "protocolVersion" in d:
            v["protocol_version"] = (
                str.from_dict(d["protocolVersion"])
                if hasattr(str, "from_dict")
                else d["protocolVersion"]
            )
        if "supportedProtocolVersions" in d:
            v["supported_protocol_versions"] = [
                str.from_dict(p) if hasattr(str, "from_dict") else p
                for p in d["supportedProtocolVersions"]
            ]
        if "serverVersion" in d:
            v["server_version"] = (
                str.from_dict(d["serverVersion"])
                if hasattr(str, "from_dict")
                else d["serverVersion"]
            )
        if "clientIdentifier" in d:
            v["client_identifier"] = (
                str.from_dict(d["clientIdentifier"])
                if hasattr(str, "from_dict")
                else d["clientIdentifier"]
            )
        return ConnectResponse(**v)

    def as_dict(self):
        d = {}
        if self.__request_id is not None:
            d["requestId"] = (
                self.__request_id.as_dict()
                if hasattr(self.__request_id, "as_dict")
                else self.__request_id
            )
        if self.__status is not None:
            d["status"] = (
                self.__status.as_dict()
                if hasattr(self.__status, "as_dict")
                else self.__status
            )
        if self.__error_message is not None:
            d["errorMessage"] = (
                self.__error_message.as_dict()
                if hasattr(self.__error_message, "as_dict")
                else self.__error_message
            )
        if self.__protocol_version is not None:
            d["protocolVersion"] = (
                self.__protocol_version.as_dict()
                if hasattr(self.__protocol_version, "as_dict")
                else self.__protocol_version
            )
        if self.__supported_protocol_versions is not None:
            d["supportedProtocolVersions"] = [
                p.as_dict() if hasattr(p, "as_dict") else p
                for p in self.__supported_protocol_versions
            ]
        if self.__server_version is not None:
            d["serverVersion"] = (
                self.__server_version.as_dict()
                if hasattr(self.__server_version, "as_dict")
                else self.__server_version
            )
        if self.__client_identifier is not None:
            d["clientIdentifier"] = (
                self.__client_identifier.as_dict()
                if hasattr(self.__client_identifier, "as_dict")
                else self.__client_identifier
            )
        return d

    def __repr__(self):
        return "<Class ConnectResponse. request_id: {}, status: {}, error_message: {}, protocol_version: {}, supported_protocol_versions: {}, server_version: {}, client_identifier: {}>".format(
            limitedRepr(
                self.__request_id[:20]
                if isinstance(self.__request_id, bytes)
                else self.__request_id
            ),
            limitedRepr(
                self.__status[:20]
                if isinstance(self.__status, bytes)
                else self.__status
            ),
            limitedRepr(
                self.__error_message[:20]
                if isinstance(self.__error_message, bytes)
                else self.__error_message
            ),
            limitedRepr(
                self.__protocol_version[:20]
                if isinstance(self.__protocol_version, bytes)
                else self.__protocol_version
            ),
            limitedRepr(
                self.__supported_protocol_versions[:20]
                if isinstance(self.__supported_protocol_versions, bytes)
                else self.__supported_protocol_versions
            ),
            limitedRepr(
                self.__server_version[:20]
                if isinstance(self.__server_version, bytes)
                else self.__server_version
            ),
            limitedRepr(
                self.__client_identifier[:20]
                if isinstance(self.__client_identifier, bytes)
                else self.__client_identifier
            ),
        )


class Operation(enum.Enum):
    """
    Internal Only.
    """

    Unknown = 0
    Connect = 1
    CreateMessageStream = 2
    DeleteMessageStream = 3
    AppendMessage = 4
    ReadMessages = 5
    ConnectResponse = 6
    CreateMessageStreamResponse = 7
    DeleteMessageStreamResponse = 8
    AppendMessageResponse = 9
    ReadMessagesResponse = 10
    ListStreams = 11
    ListStreamsResponse = 12
    DescribeMessageStream = 13
    DescribeMessageStreamResponse = 14
    UpdateMessageStream = 15
    UpdateMessageStreamResponse = 16
    UnknownOperationError = 17

    @staticmethod
    def from_dict(d):
        return Operation(d)

    def as_dict(self):
        return self.value

    def __repr__(self):
        return "<Enum Operation. {}: {}>".format(
            limitedRepr(self.name), limitedRepr(self.value)
        )


class MessageFrame:
    """
    Internal Only.
    """

    __slots__ = [
        "__operation",
        "__payload",
    ]

    _types_map = {
        "operation": {"type": Operation, "subtype": None},
        "payload": {"type": bytes, "subtype": None},
    }
    _formats_map = {}
    _validations_map = {
        "operation": {"required": True,},
        "payload": {"required": True,},
    }

    def __init__(self, operation: Operation = None, payload: bytes = None):
        pass
        self.__operation = operation
        self.__payload = payload

    def _get_operation(self):
        return self.__operation

    def _set_operation(self, value):
        if not isinstance(value, Operation):
            raise TypeError("operation must be Operation")

        self.__operation = value

    operation = property(_get_operation, _set_operation)

    def _get_payload(self):
        return self.__payload

    def _set_payload(self, value):
        if not isinstance(value, bytes):
            raise TypeError("payload must be bytes")

        self.__payload = value

    payload = property(_get_payload, _set_payload)

    @staticmethod
    def from_dict(d):
        v = {}
        if "operation" in d:
            v["operation"] = (
                Operation.from_dict(d["operation"])
                if hasattr(Operation, "from_dict")
                else d["operation"]
            )
        if "payload" in d:
            v["payload"] = (
                bytes.from_dict(d["payload"])
                if hasattr(bytes, "from_dict")
                else d["payload"]
            )
        return MessageFrame(**v)

    def as_dict(self):
        d = {}
        if self.__operation is not None:
            d["operation"] = (
                self.__operation.as_dict()
                if hasattr(self.__operation, "as_dict")
                else self.__operation
            )
        if self.__payload is not None:
            d["payload"] = (
                self.__payload.as_dict()
                if hasattr(self.__payload, "as_dict")
                else self.__payload
            )
        return d

    def __repr__(self):
        return "<Class MessageFrame. operation: {}, payload: {}>".format(
            limitedRepr(
                self.__operation[:20]
                if isinstance(self.__operation, bytes)
                else self.__operation
            ),
            limitedRepr(
                self.__payload[:20]
                if isinstance(self.__payload, bytes)
                else self.__payload
            ),
        )


class S3ExportTaskDefinition:
    """
    S3 Task definition containing all the information necessary to export the data to S3. This will contain the S3 bucket and key as well as the file's URL where the data is stored.
    """

    __slots__ = [
        "__input_url",
        "__bucket",
        "__key",
        "__user_metadata",
    ]

    _types_map = {
        "input_url": {"type": str, "subtype": None},
        "bucket": {"type": str, "subtype": None},
        "key": {"type": str, "subtype": None},
        "user_metadata": {"type": dict, "subtype": None},
    }
    _formats_map = {}
    _validations_map = {
        "input_url": {"required": True,},
        "bucket": {
            "required": True,
            "minLength": 3,
            "maxLength": 63,
            "pattern": "(?=^.{3,63}$)(?!^(\d+\.)+\d+$)(^(([a-z0-9]|[a-z0-9][a-z0-9\-]*[a-z0-9])\.)*([a-z0-9]|[a-z0-9][a-z0-9\-]*[a-z0-9])$)",
        },
        "key": {
            "required": True,
            "minLength": 1,
            "maxLength": 1024,
            "pattern": "^([^\\\{ \}%\`\[\]\"'\>\<\~\#\^\?\|]|!\{[a-zA-Z]+:[a-zA-Z\/]+\})*$",
        },
        "user_metadata": {"required": False,},
    }

    def __init__(
        self,
        input_url: str = None,
        bucket: str = None,
        key: str = None,
        user_metadata: dict = None,
    ):
        """
        :param input_url: The URL of the file that contains the data to upload. The file should be local on the disk.
        :param bucket: The name of the S3 bucket that this file should be uploaded to.
        :param key: The key for the S3 object that this file should be uploaded to.
            The string can have placeholder expressions which are resolved at upload time. Valid expressions are strings that are valid Java DateTimeFormatter strings. See https://docs.oracle.com/javase/8/docs/api/java/time/format/DateTimeFormatter.html
            Example: myKeyNamePrefix/!{timestamp:yyyy/MM/dd}/myKeyNameSuffix.
        :param user_metadata: User metadata. For key of a user metadata, callers should not include the internal "x-amz-meta-" prefix. Keys are case insensitive and will appear as lowercase strings on S3, even if they were originally specified with uppercase strings. Reserved key names start with "$aws-gg-" prefix.
        """
        pass
        self.__input_url = input_url
        self.__bucket = bucket
        self.__key = key
        self.__user_metadata = user_metadata

    def _get_input_url(self):
        return self.__input_url

    def _set_input_url(self, value):
        if not isinstance(value, str):
            raise TypeError("input_url must be str")

        self.__input_url = value

    input_url = property(_get_input_url, _set_input_url)
    """
    The URL of the file that contains the data to upload. The file should be local on the disk.
    """

    def _get_bucket(self):
        return self.__bucket

    def _set_bucket(self, value):
        if not isinstance(value, str):
            raise TypeError("bucket must be str")

        self.__bucket = value

    bucket = property(_get_bucket, _set_bucket)
    """
    The name of the S3 bucket that this file should be uploaded to.
    """

    def _get_key(self):
        return self.__key

    def _set_key(self, value):
        if not isinstance(value, str):
            raise TypeError("key must be str")

        self.__key = value

    key = property(_get_key, _set_key)
    """
    The key for the S3 object that this file should be uploaded to.
    The string can have placeholder expressions which are resolved at upload time. Valid expressions are strings that are valid Java DateTimeFormatter strings. See https://docs.oracle.com/javase/8/docs/api/java/time/format/DateTimeFormatter.html
    Example: myKeyNamePrefix/!{timestamp:yyyy/MM/dd}/myKeyNameSuffix.
    """

    def _get_user_metadata(self):
        return self.__user_metadata

    def _set_user_metadata(self, value):
        if value is not None and not isinstance(value, dict):
            raise TypeError("user_metadata must be dict")

        self.__user_metadata = value

    user_metadata = property(_get_user_metadata, _set_user_metadata)
    """
    User metadata. For key of a user metadata, callers should not include the internal "x-amz-meta-" prefix. Keys are case insensitive and will appear as lowercase strings on S3, even if they were originally specified with uppercase strings. Reserved key names start with "$aws-gg-" prefix.
    """

    @staticmethod
    def from_dict(d):
        v = {}
        if "inputUrl" in d:
            v["input_url"] = (
                str.from_dict(d["inputUrl"])
                if hasattr(str, "from_dict")
                else d["inputUrl"]
            )
        if "bucket" in d:
            v["bucket"] = (
                str.from_dict(d["bucket"]) if hasattr(str, "from_dict") else d["bucket"]
            )
        if "key" in d:
            v["key"] = (
                str.from_dict(d["key"]) if hasattr(str, "from_dict") else d["key"]
            )
        if "userMetadata" in d:
            v["user_metadata"] = (
                dict.from_dict(d["userMetadata"])
                if hasattr(dict, "from_dict")
                else d["userMetadata"]
            )
        return S3ExportTaskDefinition(**v)

    def as_dict(self):
        d = {}
        if self.__input_url is not None:
            d["inputUrl"] = (
                self.__input_url.as_dict()
                if hasattr(self.__input_url, "as_dict")
                else self.__input_url
            )
        if self.__bucket is not None:
            d["bucket"] = (
                self.__bucket.as_dict()
                if hasattr(self.__bucket, "as_dict")
                else self.__bucket
            )
        if self.__key is not None:
            d["key"] = (
                self.__key.as_dict() if hasattr(self.__key, "as_dict") else self.__key
            )
        if self.__user_metadata is not None:
            d["userMetadata"] = (
                self.__user_metadata.as_dict()
                if hasattr(self.__user_metadata, "as_dict")
                else self.__user_metadata
            )
        return d

    def __repr__(self):
        return "<Class S3ExportTaskDefinition. input_url: {}, bucket: {}, key: {}, user_metadata: {}>".format(
            limitedRepr(
                self.__input_url[:20]
                if isinstance(self.__input_url, bytes)
                else self.__input_url
            ),
            limitedRepr(
                self.__bucket[:20]
                if isinstance(self.__bucket, bytes)
                else self.__bucket
            ),
            limitedRepr(
                self.__key[:20] if isinstance(self.__key, bytes) else self.__key
            ),
            limitedRepr(
                self.__user_metadata[:20]
                if isinstance(self.__user_metadata, bytes)
                else self.__user_metadata
            ),
        )


class StatusContext:
    """
    Context associated with a status message. Describes which stream, export config, message, the status is associated with.
    """

    __slots__ = [
        "__s3_export_task_definition",
        "__export_identifier",
        "__stream_name",
        "__sequence_number",
    ]

    _types_map = {
        "s3_export_task_definition": {"type": S3ExportTaskDefinition, "subtype": None},
        "export_identifier": {"type": str, "subtype": None},
        "stream_name": {"type": str, "subtype": None},
        "sequence_number": {"type": int, "subtype": None},
    }
    _formats_map = {}
    _validations_map = {
        "s3_export_task_definition": {"required": False,},
        "export_identifier": {"required": False,},
        "stream_name": {"required": False,},
        "sequence_number": {"required": False,},
    }

    def __init__(
        self,
        s3_export_task_definition: S3ExportTaskDefinition = None,
        export_identifier: str = None,
        stream_name: str = None,
        sequence_number: int = None,
    ):
        """
        :param s3_export_task_definition: The task definition of an S3 upload task if the status is associated with it, ie, if the eventType = S3Task.
        :param export_identifier: The export identifier the status is associated with.
        :param stream_name: The name of the stream the status is associated with.
        :param sequence_number: The sequence number of the message the status is associated with.
        """
        pass
        self.__s3_export_task_definition = s3_export_task_definition
        self.__export_identifier = export_identifier
        self.__stream_name = stream_name
        self.__sequence_number = sequence_number

    def _get_s3_export_task_definition(self):
        return self.__s3_export_task_definition

    def _set_s3_export_task_definition(self, value):
        if value is not None and not isinstance(value, S3ExportTaskDefinition):
            raise TypeError("s3_export_task_definition must be S3ExportTaskDefinition")

        self.__s3_export_task_definition = value

    s3_export_task_definition = property(
        _get_s3_export_task_definition, _set_s3_export_task_definition
    )
    """
    The task definition of an S3 upload task if the status is associated with it, ie, if the eventType = S3Task.
    """

    def _get_export_identifier(self):
        return self.__export_identifier

    def _set_export_identifier(self, value):
        if value is not None and not isinstance(value, str):
            raise TypeError("export_identifier must be str")

        self.__export_identifier = value

    export_identifier = property(_get_export_identifier, _set_export_identifier)
    """
    The export identifier the status is associated with.
    """

    def _get_stream_name(self):
        return self.__stream_name

    def _set_stream_name(self, value):
        if value is not None and not isinstance(value, str):
            raise TypeError("stream_name must be str")

        self.__stream_name = value

    stream_name = property(_get_stream_name, _set_stream_name)
    """
    The name of the stream the status is associated with.
    """

    def _get_sequence_number(self):
        return self.__sequence_number

    def _set_sequence_number(self, value):
        if value is not None and not isinstance(value, int):
            raise TypeError("sequence_number must be int")

        self.__sequence_number = value

    sequence_number = property(_get_sequence_number, _set_sequence_number)
    """
    The sequence number of the message the status is associated with.
    """

    @staticmethod
    def from_dict(d):
        v = {}
        if "s3ExportTaskDefinition" in d:
            v["s3_export_task_definition"] = (
                S3ExportTaskDefinition.from_dict(d["s3ExportTaskDefinition"])
                if hasattr(S3ExportTaskDefinition, "from_dict")
                else d["s3ExportTaskDefinition"]
            )
        if "exportIdentifier" in d:
            v["export_identifier"] = (
                str.from_dict(d["exportIdentifier"])
                if hasattr(str, "from_dict")
                else d["exportIdentifier"]
            )
        if "streamName" in d:
            v["stream_name"] = (
                str.from_dict(d["streamName"])
                if hasattr(str, "from_dict")
                else d["streamName"]
            )
        if "sequenceNumber" in d:
            v["sequence_number"] = (
                int.from_dict(d["sequenceNumber"])
                if hasattr(int, "from_dict")
                else d["sequenceNumber"]
            )
        return StatusContext(**v)

    def as_dict(self):
        d = {}
        if self.__s3_export_task_definition is not None:
            d["s3ExportTaskDefinition"] = (
                self.__s3_export_task_definition.as_dict()
                if hasattr(self.__s3_export_task_definition, "as_dict")
                else self.__s3_export_task_definition
            )
        if self.__export_identifier is not None:
            d["exportIdentifier"] = (
                self.__export_identifier.as_dict()
                if hasattr(self.__export_identifier, "as_dict")
                else self.__export_identifier
            )
        if self.__stream_name is not None:
            d["streamName"] = (
                self.__stream_name.as_dict()
                if hasattr(self.__stream_name, "as_dict")
                else self.__stream_name
            )
        if self.__sequence_number is not None:
            d["sequenceNumber"] = (
                self.__sequence_number.as_dict()
                if hasattr(self.__sequence_number, "as_dict")
                else self.__sequence_number
            )
        return d

    def __repr__(self):
        return "<Class StatusContext. s3_export_task_definition: {}, export_identifier: {}, stream_name: {}, sequence_number: {}>".format(
            limitedRepr(
                self.__s3_export_task_definition[:20]
                if isinstance(self.__s3_export_task_definition, bytes)
                else self.__s3_export_task_definition
            ),
            limitedRepr(
                self.__export_identifier[:20]
                if isinstance(self.__export_identifier, bytes)
                else self.__export_identifier
            ),
            limitedRepr(
                self.__stream_name[:20]
                if isinstance(self.__stream_name, bytes)
                else self.__stream_name
            ),
            limitedRepr(
                self.__sequence_number[:20]
                if isinstance(self.__sequence_number, bytes)
                else self.__sequence_number
            ),
        )


class EventType(enum.Enum):
    """
    The type of event, which determines how to interpret the status payload.
    """

    S3Task = 0

    @staticmethod
    def from_dict(d):
        return EventType(d)

    def as_dict(self):
        return self.value

    def __repr__(self):
        return "<Enum EventType. {}: {}>".format(
            limitedRepr(self.name), limitedRepr(self.value)
        )


class Status(enum.Enum):
    """
    The status of the event.
    """

    Success = 0
    Failure = 1
    InProgress = 2
    Warning = 3
    Canceled = 4

    @staticmethod
    def from_dict(d):
        return Status(d)

    def as_dict(self):
        return self.value

    def __repr__(self):
        return "<Enum Status. {}: {}>".format(
            limitedRepr(self.name), limitedRepr(self.value)
        )


class StatusLevel(enum.Enum):
    """
    Defines the verbosity of status messages in a status-stream.
    """

    ERROR = 0
    WARN = 1
    INFO = 2
    DEBUG = 3
    TRACE = 4

    @staticmethod
    def from_dict(d):
        return StatusLevel(d)

    def as_dict(self):
        return self.value

    def __repr__(self):
        return "<Enum StatusLevel. {}: {}>".format(
            limitedRepr(self.name), limitedRepr(self.value)
        )


class StatusMessage:
    """
    Status object appended to a status-stream.
    """

    __slots__ = [
        "__event_type",
        "__status_level",
        "__status",
        "__status_context",
        "__message",
        "__timestamp_epoch_ms",
    ]

    _types_map = {
        "event_type": {"type": EventType, "subtype": None},
        "status_level": {"type": StatusLevel, "subtype": None},
        "status": {"type": Status, "subtype": None},
        "status_context": {"type": StatusContext, "subtype": None},
        "message": {"type": str, "subtype": None},
        "timestamp_epoch_ms": {"type": int, "subtype": None},
    }
    _formats_map = {}
    _validations_map = {
        "event_type": {"required": True,},
        "status_level": {"required": False,},
        "status": {"required": True,},
        "status_context": {"required": False,},
        "message": {"required": False,},
        "timestamp_epoch_ms": {"required": False,},
    }

    def __init__(
        self,
        event_type: EventType = None,
        status_level: StatusLevel = None,
        status: Status = None,
        status_context: StatusContext = None,
        message: str = None,
        timestamp_epoch_ms: int = None,
    ):
        """
        :param message: String describing the status message.
        :param timestamp_epoch_ms: The time this status was added to the status-stream (in milliseconds since epoch).
        """
        pass
        self.__event_type = event_type
        self.__status_level = status_level
        self.__status = status
        self.__status_context = status_context
        self.__message = message
        self.__timestamp_epoch_ms = timestamp_epoch_ms

    def _get_event_type(self):
        return self.__event_type

    def _set_event_type(self, value):
        if not isinstance(value, EventType):
            raise TypeError("event_type must be EventType")

        self.__event_type = value

    event_type = property(_get_event_type, _set_event_type)

    def _get_status_level(self):
        return self.__status_level

    def _set_status_level(self, value):
        if value is not None and not isinstance(value, StatusLevel):
            raise TypeError("status_level must be StatusLevel")

        self.__status_level = value

    status_level = property(_get_status_level, _set_status_level)

    def _get_status(self):
        return self.__status

    def _set_status(self, value):
        if not isinstance(value, Status):
            raise TypeError("status must be Status")

        self.__status = value

    status = property(_get_status, _set_status)

    def _get_status_context(self):
        return self.__status_context

    def _set_status_context(self, value):
        if value is not None and not isinstance(value, StatusContext):
            raise TypeError("status_context must be StatusContext")

        self.__status_context = value

    status_context = property(_get_status_context, _set_status_context)

    def _get_message(self):
        return self.__message

    def _set_message(self, value):
        if value is not None and not isinstance(value, str):
            raise TypeError("message must be str")

        self.__message = value

    message = property(_get_message, _set_message)
    """
    String describing the status message.
    """

    def _get_timestamp_epoch_ms(self):
        return self.__timestamp_epoch_ms

    def _set_timestamp_epoch_ms(self, value):
        if value is not None and not isinstance(value, int):
            raise TypeError("timestamp_epoch_ms must be int")

        self.__timestamp_epoch_ms = value

    timestamp_epoch_ms = property(_get_timestamp_epoch_ms, _set_timestamp_epoch_ms)
    """
    The time this status was added to the status-stream (in milliseconds since epoch).
    """

    @staticmethod
    def from_dict(d):
        v = {}
        if "eventType" in d:
            v["event_type"] = (
                EventType.from_dict(d["eventType"])
                if hasattr(EventType, "from_dict")
                else d["eventType"]
            )
        if "statusLevel" in d:
            v["status_level"] = (
                StatusLevel.from_dict(d["statusLevel"])
                if hasattr(StatusLevel, "from_dict")
                else d["statusLevel"]
            )
        if "status" in d:
            v["status"] = (
                Status.from_dict(d["status"])
                if hasattr(Status, "from_dict")
                else d["status"]
            )
        if "statusContext" in d:
            v["status_context"] = (
                StatusContext.from_dict(d["statusContext"])
                if hasattr(StatusContext, "from_dict")
                else d["statusContext"]
            )
        if "message" in d:
            v["message"] = (
                str.from_dict(d["message"])
                if hasattr(str, "from_dict")
                else d["message"]
            )
        if "timestampEpochMs" in d:
            v["timestamp_epoch_ms"] = (
                int.from_dict(d["timestampEpochMs"])
                if hasattr(int, "from_dict")
                else d["timestampEpochMs"]
            )
        return StatusMessage(**v)

    def as_dict(self):
        d = {}
        if self.__event_type is not None:
            d["eventType"] = (
                self.__event_type.as_dict()
                if hasattr(self.__event_type, "as_dict")
                else self.__event_type
            )
        if self.__status_level is not None:
            d["statusLevel"] = (
                self.__status_level.as_dict()
                if hasattr(self.__status_level, "as_dict")
                else self.__status_level
            )
        if self.__status is not None:
            d["status"] = (
                self.__status.as_dict()
                if hasattr(self.__status, "as_dict")
                else self.__status
            )
        if self.__status_context is not None:
            d["statusContext"] = (
                self.__status_context.as_dict()
                if hasattr(self.__status_context, "as_dict")
                else self.__status_context
            )
        if self.__message is not None:
            d["message"] = (
                self.__message.as_dict()
                if hasattr(self.__message, "as_dict")
                else self.__message
            )
        if self.__timestamp_epoch_ms is not None:
            d["timestampEpochMs"] = (
                self.__timestamp_epoch_ms.as_dict()
                if hasattr(self.__timestamp_epoch_ms, "as_dict")
                else self.__timestamp_epoch_ms
            )
        return d

    def __repr__(self):
        return "<Class StatusMessage. event_type: {}, status_level: {}, status: {}, status_context: {}, message: {}, timestamp_epoch_ms: {}>".format(
            limitedRepr(
                self.__event_type[:20]
                if isinstance(self.__event_type, bytes)
                else self.__event_type
            ),
            limitedRepr(
                self.__status_level[:20]
                if isinstance(self.__status_level, bytes)
                else self.__status_level
            ),
            limitedRepr(
                self.__status[:20]
                if isinstance(self.__status, bytes)
                else self.__status
            ),
            limitedRepr(
                self.__status_context[:20]
                if isinstance(self.__status_context, bytes)
                else self.__status_context
            ),
            limitedRepr(
                self.__message[:20]
                if isinstance(self.__message, bytes)
                else self.__message
            ),
            limitedRepr(
                self.__timestamp_epoch_ms[:20]
                if isinstance(self.__timestamp_epoch_ms, bytes)
                else self.__timestamp_epoch_ms
            ),
        )


class TraceableRequest:
    """
    (Internal Only) TraceableRequest that contains only requestId.
    """

    __slots__ = [
        "__request_id",
    ]

    _types_map = {
        "request_id": {"type": str, "subtype": None},
    }
    _formats_map = {}
    _validations_map = {
        "request_id": {"required": True, "minLength": 1, "pattern": "^[\w ,.\-_]*$",},
    }

    def __init__(self, request_id: str = None):
        pass
        self.__request_id = request_id

    def _get_request_id(self):
        return self.__request_id

    def _set_request_id(self, value):
        if not isinstance(value, str):
            raise TypeError("request_id must be str")

        self.__request_id = value

    request_id = property(_get_request_id, _set_request_id)

    @staticmethod
    def from_dict(d):
        v = {}
        if "requestId" in d:
            v["request_id"] = (
                str.from_dict(d["requestId"])
                if hasattr(str, "from_dict")
                else d["requestId"]
            )
        return TraceableRequest(**v)

    def as_dict(self):
        d = {}
        if self.__request_id is not None:
            d["requestId"] = (
                self.__request_id.as_dict()
                if hasattr(self.__request_id, "as_dict")
                else self.__request_id
            )
        return d

    def __repr__(self):
        return "<Class TraceableRequest. request_id: {}>".format(
            limitedRepr(
                self.__request_id[:20]
                if isinstance(self.__request_id, bytes)
                else self.__request_id
            )
        )


class UnknownOperationError:
    """
    (Internal Only) Response for UnknownOperationError.
    """

    __slots__ = [
        "__request_id",
        "__status",
        "__error_message",
    ]

    _types_map = {
        "request_id": {"type": str, "subtype": None},
        "status": {"type": ResponseStatusCode, "subtype": None},
        "error_message": {"type": str, "subtype": None},
    }
    _formats_map = {}
    _validations_map = {
        "request_id": {"required": True, "minLength": 1, "pattern": "^[\w ,.\-_]*$",},
        "status": {"required": True,},
        "error_message": {"required": False,},
    }

    def __init__(
        self,
        request_id: str = None,
        status: ResponseStatusCode = None,
        error_message: str = None,
    ):
        pass
        self.__request_id = request_id
        self.__status = status
        self.__error_message = error_message

    def _get_request_id(self):
        return self.__request_id

    def _set_request_id(self, value):
        if not isinstance(value, str):
            raise TypeError("request_id must be str")

        self.__request_id = value

    request_id = property(_get_request_id, _set_request_id)

    def _get_status(self):
        return self.__status

    def _set_status(self, value):
        if not isinstance(value, ResponseStatusCode):
            raise TypeError("status must be ResponseStatusCode")

        self.__status = value

    status = property(_get_status, _set_status)

    def _get_error_message(self):
        return self.__error_message

    def _set_error_message(self, value):
        if value is not None and not isinstance(value, str):
            raise TypeError("error_message must be str")

        self.__error_message = value

    error_message = property(_get_error_message, _set_error_message)

    @staticmethod
    def from_dict(d):
        v = {}
        if "requestId" in d:
            v["request_id"] = (
                str.from_dict(d["requestId"])
                if hasattr(str, "from_dict")
                else d["requestId"]
            )
        if "status" in d:
            v["status"] = (
                ResponseStatusCode.from_dict(d["status"])
                if hasattr(ResponseStatusCode, "from_dict")
                else d["status"]
            )
        if "errorMessage" in d:
            v["error_message"] = (
                str.from_dict(d["errorMessage"])
                if hasattr(str, "from_dict")
                else d["errorMessage"]
            )
        return UnknownOperationError(**v)

    def as_dict(self):
        d = {}
        if self.__request_id is not None:
            d["requestId"] = (
                self.__request_id.as_dict()
                if hasattr(self.__request_id, "as_dict")
                else self.__request_id
            )
        if self.__status is not None:
            d["status"] = (
                self.__status.as_dict()
                if hasattr(self.__status, "as_dict")
                else self.__status
            )
        if self.__error_message is not None:
            d["errorMessage"] = (
                self.__error_message.as_dict()
                if hasattr(self.__error_message, "as_dict")
                else self.__error_message
            )
        return d

    def __repr__(self):
        return "<Class UnknownOperationError. request_id: {}, status: {}, error_message: {}>".format(
            limitedRepr(
                self.__request_id[:20]
                if isinstance(self.__request_id, bytes)
                else self.__request_id
            ),
            limitedRepr(
                self.__status[:20]
                if isinstance(self.__status, bytes)
                else self.__status
            ),
            limitedRepr(
                self.__error_message[:20]
                if isinstance(self.__error_message, bytes)
                else self.__error_message
            ),
        )


class KinesisConfig:
    """
    Configuration object for Kinesis data streams export destination.
    """

    __slots__ = [
        "__identifier",
        "__kinesis_stream_name",
        "__batch_size",
        "__batch_interval_millis",
        "__priority",
        "__start_sequence_number",
        "__disabled",
    ]

    _types_map = {
        "identifier": {"type": str, "subtype": None},
        "kinesis_stream_name": {"type": str, "subtype": None},
        "batch_size": {"type": int, "subtype": None},
        "batch_interval_millis": {"type": int, "subtype": None},
        "priority": {"type": int, "subtype": None},
        "start_sequence_number": {"type": int, "subtype": None},
        "disabled": {"type": bool, "subtype": None},
    }
    _formats_map = {}
    _validations_map = {
        "identifier": {
            "required": True,
            "minLength": 1,
            "maxLength": 255,
            "pattern": "^[\w ,.\-_]*$",
        },
        "kinesis_stream_name": {"required": True, "minLength": 1,},
        "batch_size": {"required": False, "maximum": 500, "minimum": 1,},
        "batch_interval_millis": {
            "required": False,
            "maximum": 9223372036854,
            "minimum": 60000,
        },
        "priority": {"required": False, "maximum": 10, "minimum": 1,},
        "start_sequence_number": {
            "required": False,
            "maximum": 9223372036854775807,
            "minimum": 0,
        },
        "disabled": {"required": False,},
    }

    def __init__(
        self,
        identifier: str = None,
        kinesis_stream_name: str = None,
        batch_size: int = None,
        batch_interval_millis: int = None,
        priority: int = None,
        start_sequence_number: int = None,
        disabled: bool = None,
    ):
        """
        :param identifier: A unique identifier to identify this individual upload stream.
            Must be an alphanumeric string including spaces, commas, periods, hyphens, and underscores with length between 1 and 255.
        :param kinesis_stream_name: The name of the Kinesis data stream that this exporter should upload to.
        :param batch_size: The maximum size of a batch to send to Kinesis. Messages will be queued until the batch size is reached, after which they will then be uploaded. If unspecified the default will be 500.
            If both batchSize and batchIntervalMillis are specified, then messages will be eligible for upload when either condition is met.
            The batch size must be between 1 and 500.
        :param batch_interval_millis: The time in milliseconds between the earliest un-uploaded message and the current time. If this time is exceeded, messages will be uploaded in the next batch. If unspecified messages will be eligible for upload immediately.
            If both batchSize and batchIntervalMillis are specified, then messages will be eligible for upload when either condition is met.
            The minimum value is 60000 milliseconds and the maximum is 9223372036854 milliseconds.
        :param priority: Priority for this upload stream. Lower values are higher priority. If not specified it will have the lowest priority.
        :param start_sequence_number: The sequence number of the message to use as the starting message in the export. Default is 0. The sequence number provided should be less than the newest sequence number in the stream, i.e., sequence number of the last messaged appended. To find the newest sequence number, describe the stream and then check the storage status of the returned MessageStreamInfo object.
        :param disabled: Enable or disable this export. Default is false.
        """
        pass
        self.__identifier = identifier
        self.__kinesis_stream_name = kinesis_stream_name
        self.__batch_size = batch_size
        self.__batch_interval_millis = batch_interval_millis
        self.__priority = priority
        self.__start_sequence_number = start_sequence_number
        self.__disabled = disabled

    def _get_identifier(self):
        return self.__identifier

    def _set_identifier(self, value):
        if not isinstance(value, str):
            raise TypeError("identifier must be str")

        self.__identifier = value

    identifier = property(_get_identifier, _set_identifier)
    """
    A unique identifier to identify this individual upload stream.
    Must be an alphanumeric string including spaces, commas, periods, hyphens, and underscores with length between 1 and 255.
    """

    def _get_kinesis_stream_name(self):
        return self.__kinesis_stream_name

    def _set_kinesis_stream_name(self, value):
        if not isinstance(value, str):
            raise TypeError("kinesis_stream_name must be str")

        self.__kinesis_stream_name = value

    kinesis_stream_name = property(_get_kinesis_stream_name, _set_kinesis_stream_name)
    """
    The name of the Kinesis data stream that this exporter should upload to.
    """

    def _get_batch_size(self):
        return self.__batch_size

    def _set_batch_size(self, value):
        if value is not None and not isinstance(value, int):
            raise TypeError("batch_size must be int")

        self.__batch_size = value

    batch_size = property(_get_batch_size, _set_batch_size)
    """
    The maximum size of a batch to send to Kinesis. Messages will be queued until the batch size is reached, after which they will then be uploaded. If unspecified the default will be 500.
    If both batchSize and batchIntervalMillis are specified, then messages will be eligible for upload when either condition is met.
    The batch size must be between 1 and 500.
    """

    def _get_batch_interval_millis(self):
        return self.__batch_interval_millis

    def _set_batch_interval_millis(self, value):
        if value is not None and not isinstance(value, int):
            raise TypeError("batch_interval_millis must be int")

        self.__batch_interval_millis = value

    batch_interval_millis = property(
        _get_batch_interval_millis, _set_batch_interval_millis
    )
    """
    The time in milliseconds between the earliest un-uploaded message and the current time. If this time is exceeded, messages will be uploaded in the next batch. If unspecified messages will be eligible for upload immediately.
    If both batchSize and batchIntervalMillis are specified, then messages will be eligible for upload when either condition is met.
    The minimum value is 60000 milliseconds and the maximum is 9223372036854 milliseconds.
    """

    def _get_priority(self):
        return self.__priority

    def _set_priority(self, value):
        if value is not None and not isinstance(value, int):
            raise TypeError("priority must be int")

        self.__priority = value

    priority = property(_get_priority, _set_priority)
    """
    Priority for this upload stream. Lower values are higher priority. If not specified it will have the lowest priority.
    """

    def _get_start_sequence_number(self):
        return self.__start_sequence_number

    def _set_start_sequence_number(self, value):
        if value is not None and not isinstance(value, int):
            raise TypeError("start_sequence_number must be int")

        self.__start_sequence_number = value

    start_sequence_number = property(
        _get_start_sequence_number, _set_start_sequence_number
    )
    """
    The sequence number of the message to use as the starting message in the export. Default is 0. The sequence number provided should be less than the newest sequence number in the stream, i.e., sequence number of the last messaged appended. To find the newest sequence number, describe the stream and then check the storage status of the returned MessageStreamInfo object.
    """

    def _get_disabled(self):
        return self.__disabled

    def _set_disabled(self, value):
        if value is not None and not isinstance(value, bool):
            raise TypeError("disabled must be bool")

        self.__disabled = value

    disabled = property(_get_disabled, _set_disabled)
    """
    Enable or disable this export. Default is false.
    """

    @staticmethod
    def from_dict(d):
        v = {}
        if "identifier" in d:
            v["identifier"] = (
                str.from_dict(d["identifier"])
                if hasattr(str, "from_dict")
                else d["identifier"]
            )
        if "kinesisStreamName" in d:
            v["kinesis_stream_name"] = (
                str.from_dict(d["kinesisStreamName"])
                if hasattr(str, "from_dict")
                else d["kinesisStreamName"]
            )
        if "batchSize" in d:
            v["batch_size"] = (
                int.from_dict(d["batchSize"])
                if hasattr(int, "from_dict")
                else d["batchSize"]
            )
        if "batchIntervalMillis" in d:
            v["batch_interval_millis"] = (
                int.from_dict(d["batchIntervalMillis"])
                if hasattr(int, "from_dict")
                else d["batchIntervalMillis"]
            )
        if "priority" in d:
            v["priority"] = (
                int.from_dict(d["priority"])
                if hasattr(int, "from_dict")
                else d["priority"]
            )
        if "startSequenceNumber" in d:
            v["start_sequence_number"] = (
                int.from_dict(d["startSequenceNumber"])
                if hasattr(int, "from_dict")
                else d["startSequenceNumber"]
            )
        if "disabled" in d:
            v["disabled"] = (
                bool.from_dict(d["disabled"])
                if hasattr(bool, "from_dict")
                else d["disabled"]
            )
        return KinesisConfig(**v)

    def as_dict(self):
        d = {}
        if self.__identifier is not None:
            d["identifier"] = (
                self.__identifier.as_dict()
                if hasattr(self.__identifier, "as_dict")
                else self.__identifier
            )
        if self.__kinesis_stream_name is not None:
            d["kinesisStreamName"] = (
                self.__kinesis_stream_name.as_dict()
                if hasattr(self.__kinesis_stream_name, "as_dict")
                else self.__kinesis_stream_name
            )
        if self.__batch_size is not None:
            d["batchSize"] = (
                self.__batch_size.as_dict()
                if hasattr(self.__batch_size, "as_dict")
                else self.__batch_size
            )
        if self.__batch_interval_millis is not None:
            d["batchIntervalMillis"] = (
                self.__batch_interval_millis.as_dict()
                if hasattr(self.__batch_interval_millis, "as_dict")
                else self.__batch_interval_millis
            )
        if self.__priority is not None:
            d["priority"] = (
                self.__priority.as_dict()
                if hasattr(self.__priority, "as_dict")
                else self.__priority
            )
        if self.__start_sequence_number is not None:
            d["startSequenceNumber"] = (
                self.__start_sequence_number.as_dict()
                if hasattr(self.__start_sequence_number, "as_dict")
                else self.__start_sequence_number
            )
        if self.__disabled is not None:
            d["disabled"] = (
                self.__disabled.as_dict()
                if hasattr(self.__disabled, "as_dict")
                else self.__disabled
            )
        return d

    def __repr__(self):
        return "<Class KinesisConfig. identifier: {}, kinesis_stream_name: {}, batch_size: {}, batch_interval_millis: {}, priority: {}, start_sequence_number: {}, disabled: {}>".format(
            limitedRepr(
                self.__identifier[:20]
                if isinstance(self.__identifier, bytes)
                else self.__identifier
            ),
            limitedRepr(
                self.__kinesis_stream_name[:20]
                if isinstance(self.__kinesis_stream_name, bytes)
                else self.__kinesis_stream_name
            ),
            limitedRepr(
                self.__batch_size[:20]
                if isinstance(self.__batch_size, bytes)
                else self.__batch_size
            ),
            limitedRepr(
                self.__batch_interval_millis[:20]
                if isinstance(self.__batch_interval_millis, bytes)
                else self.__batch_interval_millis
            ),
            limitedRepr(
                self.__priority[:20]
                if isinstance(self.__priority, bytes)
                else self.__priority
            ),
            limitedRepr(
                self.__start_sequence_number[:20]
                if isinstance(self.__start_sequence_number, bytes)
                else self.__start_sequence_number
            ),
            limitedRepr(
                self.__disabled[:20]
                if isinstance(self.__disabled, bytes)
                else self.__disabled
            ),
        )


class StatusConfig:
    """
    Configuration for status in a status-stream.
    """

    __slots__ = [
        "__status_level",
        "__status_stream_name",
    ]

    _types_map = {
        "status_level": {"type": StatusLevel, "subtype": None},
        "status_stream_name": {"type": str, "subtype": None},
    }
    _formats_map = {}
    _validations_map = {
        "status_level": {"required": False,},
        "status_stream_name": {
            "required": False,
            "minLength": 1,
            "maxLength": 255,
            "pattern": "^[\w ,.\-_]*$",
        },
    }

    def __init__(
        self, status_level: StatusLevel = None, status_stream_name: str = None
    ):
        """
        :param status_level: Defines the verbosity of status messages in a status-stream.
        :param status_stream_name: The name of the stream to which status messages are appended.
            The status-stream should be created before associating it with another stream.
        """
        pass
        self.__status_level = status_level
        self.__status_stream_name = status_stream_name

    def _get_status_level(self):
        return self.__status_level

    def _set_status_level(self, value):
        if value is not None and not isinstance(value, StatusLevel):
            raise TypeError("status_level must be StatusLevel")

        self.__status_level = value

    status_level = property(_get_status_level, _set_status_level)
    """
    Defines the verbosity of status messages in a status-stream.
    """

    def _get_status_stream_name(self):
        return self.__status_stream_name

    def _set_status_stream_name(self, value):
        if value is not None and not isinstance(value, str):
            raise TypeError("status_stream_name must be str")

        self.__status_stream_name = value

    status_stream_name = property(_get_status_stream_name, _set_status_stream_name)
    """
    The name of the stream to which status messages are appended.
    The status-stream should be created before associating it with another stream.
    """

    @staticmethod
    def from_dict(d):
        v = {}
        if "statusLevel" in d:
            v["status_level"] = (
                StatusLevel.from_dict(d["statusLevel"])
                if hasattr(StatusLevel, "from_dict")
                else d["statusLevel"]
            )
        if "statusStreamName" in d:
            v["status_stream_name"] = (
                str.from_dict(d["statusStreamName"])
                if hasattr(str, "from_dict")
                else d["statusStreamName"]
            )
        return StatusConfig(**v)

    def as_dict(self):
        d = {}
        if self.__status_level is not None:
            d["statusLevel"] = (
                self.__status_level.as_dict()
                if hasattr(self.__status_level, "as_dict")
                else self.__status_level
            )
        if self.__status_stream_name is not None:
            d["statusStreamName"] = (
                self.__status_stream_name.as_dict()
                if hasattr(self.__status_stream_name, "as_dict")
                else self.__status_stream_name
            )
        return d

    def __repr__(self):
        return "<Class StatusConfig. status_level: {}, status_stream_name: {}>".format(
            limitedRepr(
                self.__status_level[:20]
                if isinstance(self.__status_level, bytes)
                else self.__status_level
            ),
            limitedRepr(
                self.__status_stream_name[:20]
                if isinstance(self.__status_stream_name, bytes)
                else self.__status_stream_name
            ),
        )


class S3ExportTaskExecutorConfig:
    """
    Configuration object for S3 export tasks executor.  Minimum version requirements: StreamManager server version 1.1 (or AWS IoT Greengrass Core 1.11.0)
    """

    __slots__ = [
        "__identifier",
        "__size_threshold_for_multipart_upload_bytes",
        "__priority",
        "__disabled",
        "__status_config",
    ]

    _types_map = {
        "identifier": {"type": str, "subtype": None},
        "size_threshold_for_multipart_upload_bytes": {"type": int, "subtype": None},
        "priority": {"type": int, "subtype": None},
        "disabled": {"type": bool, "subtype": None},
        "status_config": {"type": StatusConfig, "subtype": None},
    }
    _formats_map = {}
    _validations_map = {
        "identifier": {
            "required": True,
            "minLength": 1,
            "maxLength": 255,
            "pattern": "^[\w ,.\-_]*$",
        },
        "size_threshold_for_multipart_upload_bytes": {
            "required": False,
            "minimum": 5242880,
        },
        "priority": {"required": False, "maximum": 10, "minimum": 1,},
        "disabled": {"required": False,},
        "status_config": {"required": False,},
    }

    def __init__(
        self,
        identifier: str = None,
        size_threshold_for_multipart_upload_bytes: int = None,
        priority: int = None,
        disabled: bool = None,
        status_config: StatusConfig = None,
    ):
        """
        :param identifier: A unique identifier to identify this individual upload task.
            Must be an alphanumeric string including spaces, commas, periods, hyphens, and underscores with length between 1 and 255.
        :param size_threshold_for_multipart_upload_bytes: The size threshold in bytes for when to use multipart uploads. Uploads over this size will automatically use a multipart upload strategy, while uploads equal or smaller than this threshold will use a single connection to upload the whole object.
        :param priority: Priority for this upload task. Lower values are higher priority. If not specified it will have the lowest priority.
        :param disabled: Enable or disable this export. Default is false.
        :param status_config: Event status configuration that specifies the target status stream and verbosity.
        """
        pass
        self.__identifier = identifier
        self.__size_threshold_for_multipart_upload_bytes = (
            size_threshold_for_multipart_upload_bytes
        )
        self.__priority = priority
        self.__disabled = disabled
        self.__status_config = status_config

    def _get_identifier(self):
        return self.__identifier

    def _set_identifier(self, value):
        if not isinstance(value, str):
            raise TypeError("identifier must be str")

        self.__identifier = value

    identifier = property(_get_identifier, _set_identifier)
    """
    A unique identifier to identify this individual upload task.
    Must be an alphanumeric string including spaces, commas, periods, hyphens, and underscores with length between 1 and 255.
    """

    def _get_size_threshold_for_multipart_upload_bytes(self):
        return self.__size_threshold_for_multipart_upload_bytes

    def _set_size_threshold_for_multipart_upload_bytes(self, value):
        if value is not None and not isinstance(value, int):
            raise TypeError("size_threshold_for_multipart_upload_bytes must be int")

        self.__size_threshold_for_multipart_upload_bytes = value

    size_threshold_for_multipart_upload_bytes = property(
        _get_size_threshold_for_multipart_upload_bytes,
        _set_size_threshold_for_multipart_upload_bytes,
    )
    """
    The size threshold in bytes for when to use multipart uploads. Uploads over this size will automatically use a multipart upload strategy, while uploads equal or smaller than this threshold will use a single connection to upload the whole object.
    """

    def _get_priority(self):
        return self.__priority

    def _set_priority(self, value):
        if value is not None and not isinstance(value, int):
            raise TypeError("priority must be int")

        self.__priority = value

    priority = property(_get_priority, _set_priority)
    """
    Priority for this upload task. Lower values are higher priority. If not specified it will have the lowest priority.
    """

    def _get_disabled(self):
        return self.__disabled

    def _set_disabled(self, value):
        if value is not None and not isinstance(value, bool):
            raise TypeError("disabled must be bool")

        self.__disabled = value

    disabled = property(_get_disabled, _set_disabled)
    """
    Enable or disable this export. Default is false.
    """

    def _get_status_config(self):
        return self.__status_config

    def _set_status_config(self, value):
        if value is not None and not isinstance(value, StatusConfig):
            raise TypeError("status_config must be StatusConfig")

        self.__status_config = value

    status_config = property(_get_status_config, _set_status_config)
    """
    Event status configuration that specifies the target status stream and verbosity.
    """

    @staticmethod
    def from_dict(d):
        v = {}
        if "identifier" in d:
            v["identifier"] = (
                str.from_dict(d["identifier"])
                if hasattr(str, "from_dict")
                else d["identifier"]
            )
        if "sizeThresholdForMultipartUploadBytes" in d:
            v["size_threshold_for_multipart_upload_bytes"] = (
                int.from_dict(d["sizeThresholdForMultipartUploadBytes"])
                if hasattr(int, "from_dict")
                else d["sizeThresholdForMultipartUploadBytes"]
            )
        if "priority" in d:
            v["priority"] = (
                int.from_dict(d["priority"])
                if hasattr(int, "from_dict")
                else d["priority"]
            )
        if "disabled" in d:
            v["disabled"] = (
                bool.from_dict(d["disabled"])
                if hasattr(bool, "from_dict")
                else d["disabled"]
            )
        if "statusConfig" in d:
            v["status_config"] = (
                StatusConfig.from_dict(d["statusConfig"])
                if hasattr(StatusConfig, "from_dict")
                else d["statusConfig"]
            )
        return S3ExportTaskExecutorConfig(**v)

    def as_dict(self):
        d = {}
        if self.__identifier is not None:
            d["identifier"] = (
                self.__identifier.as_dict()
                if hasattr(self.__identifier, "as_dict")
                else self.__identifier
            )
        if self.__size_threshold_for_multipart_upload_bytes is not None:
            d["sizeThresholdForMultipartUploadBytes"] = (
                self.__size_threshold_for_multipart_upload_bytes.as_dict()
                if hasattr(self.__size_threshold_for_multipart_upload_bytes, "as_dict")
                else self.__size_threshold_for_multipart_upload_bytes
            )
        if self.__priority is not None:
            d["priority"] = (
                self.__priority.as_dict()
                if hasattr(self.__priority, "as_dict")
                else self.__priority
            )
        if self.__disabled is not None:
            d["disabled"] = (
                self.__disabled.as_dict()
                if hasattr(self.__disabled, "as_dict")
                else self.__disabled
            )
        if self.__status_config is not None:
            d["statusConfig"] = (
                self.__status_config.as_dict()
                if hasattr(self.__status_config, "as_dict")
                else self.__status_config
            )
        return d

    def __repr__(self):
        return "<Class S3ExportTaskExecutorConfig. identifier: {}, size_threshold_for_multipart_upload_bytes: {}, priority: {}, disabled: {}, status_config: {}>".format(
            limitedRepr(
                self.__identifier[:20]
                if isinstance(self.__identifier, bytes)
                else self.__identifier
            ),
            limitedRepr(
                self.__size_threshold_for_multipart_upload_bytes[:20]
                if isinstance(self.__size_threshold_for_multipart_upload_bytes, bytes)
                else self.__size_threshold_for_multipart_upload_bytes
            ),
            limitedRepr(
                self.__priority[:20]
                if isinstance(self.__priority, bytes)
                else self.__priority
            ),
            limitedRepr(
                self.__disabled[:20]
                if isinstance(self.__disabled, bytes)
                else self.__disabled
            ),
            limitedRepr(
                self.__status_config[:20]
                if isinstance(self.__status_config, bytes)
                else self.__status_config
            ),
        )


class ExportFormat(enum.Enum):
    """
    ExportFormat is used to define how messages are batched and formatted in the export payload.
    RAW_NOT_BATCHED: Each message in a batch will be sent as an individual HTTP POST with the payload as the body (even if batchSize is set).
    JSON_BATCHED: Each batch of messages will be sent as a JSON list of Message objects as the body.
    """

    RAW_NOT_BATCHED = 0
    JSON_BATCHED = 1

    @staticmethod
    def from_dict(d):
        return ExportFormat(d)

    def as_dict(self):
        return self.value

    def __repr__(self):
        return "<Enum ExportFormat. {}: {}>".format(
            limitedRepr(self.name), limitedRepr(self.value)
        )


class HTTPConfig:
    """
    This export destination is not supported! The interface may change at any time without notice and should not be relied on for any production use.
    There are no guarantees around its correctness.
    This configures an HTTP endpoint which sends a POST request to the provided URI. Each request contains a single message in the body of the request.
    """

    __slots__ = [
        "__identifier",
        "__uri",
        "__batch_size",
        "__batch_interval_millis",
        "__priority",
        "__start_sequence_number",
        "__disabled",
        "__export_format",
    ]

    _types_map = {
        "identifier": {"type": str, "subtype": None},
        "uri": {"type": str, "subtype": None},
        "batch_size": {"type": int, "subtype": None},
        "batch_interval_millis": {"type": int, "subtype": None},
        "priority": {"type": int, "subtype": None},
        "start_sequence_number": {"type": int, "subtype": None},
        "disabled": {"type": bool, "subtype": None},
        "export_format": {"type": ExportFormat, "subtype": None},
    }
    _formats_map = {}
    _validations_map = {
        "identifier": {
            "required": True,
            "minLength": 1,
            "maxLength": 255,
            "pattern": "^[\w ,.\-_]*$",
        },
        "uri": {"required": True, "minLength": 1,},
        "batch_size": {"required": False, "maximum": 500, "minimum": 1,},
        "batch_interval_millis": {
            "required": False,
            "maximum": 9223372036854,
            "minimum": 60000,
        },
        "priority": {"required": False, "maximum": 10, "minimum": 1,},
        "start_sequence_number": {
            "required": False,
            "maximum": 9223372036854775807,
            "minimum": 0,
        },
        "disabled": {"required": False,},
        "export_format": {"required": False,},
    }

    def __init__(
        self,
        identifier: str = None,
        uri: str = None,
        batch_size: int = None,
        batch_interval_millis: int = None,
        priority: int = None,
        start_sequence_number: int = None,
        disabled: bool = None,
        export_format: ExportFormat = None,
    ):
        """
        :param identifier: A unique identifier to identify this individual upload stream.
            Must be an alphanumeric string including spaces, commas, periods, hyphens, and underscores with length between 1 and 255.
        :param uri: URL for HTTP endpoint which should receive the POST requests for export.
        :param batch_size: The maximum size of a batch to send to the destination. Messages will be queued until the batch size is reached, after which they will then be uploaded. If unspecified the default will be 500.
            If both batchSize and batchIntervalMillis are specified, then messages will be eligible for upload when either condition is met.
            The minimum batch size is 1 and the maximum is 500.
        :param batch_interval_millis: The time in milliseconds between the earliest un-uploaded message and the current time. If this time is exceeded, messages will be uploaded in the next batch. If unspecified messages will be eligible for upload immediately.
            If both batchSize and batchIntervalMillis are specified, then messages will be eligible for upload when either condition is met.
            The minimum value is 60000 milliseconds and the maximum is 9223372036854 milliseconds.
        :param priority: Priority for this upload stream. Lower values are higher priority. If not specified it will have the lowest priority.
        :param start_sequence_number: The sequence number of the message to use as the starting message in the export. Default is 0. The sequence number provided should be less than the newest sequence number in the stream, i.e., sequence number of the last messaged appended. To find the newest sequence number, describe the stream and then check the storage status of the returned MessageStreamInfo object.
        :param disabled: Enable or disable this export. Default is false.
        :param export_format: Defines how messages are batched and formatted in the export payload.
        """
        pass
        self.__identifier = identifier
        self.__uri = uri
        self.__batch_size = batch_size
        self.__batch_interval_millis = batch_interval_millis
        self.__priority = priority
        self.__start_sequence_number = start_sequence_number
        self.__disabled = disabled
        self.__export_format = export_format

    def _get_identifier(self):
        return self.__identifier

    def _set_identifier(self, value):
        if not isinstance(value, str):
            raise TypeError("identifier must be str")

        self.__identifier = value

    identifier = property(_get_identifier, _set_identifier)
    """
    A unique identifier to identify this individual upload stream.
    Must be an alphanumeric string including spaces, commas, periods, hyphens, and underscores with length between 1 and 255.
    """

    def _get_uri(self):
        return self.__uri

    def _set_uri(self, value):
        if not isinstance(value, str):
            raise TypeError("uri must be str")

        self.__uri = value

    uri = property(_get_uri, _set_uri)
    """
    URL for HTTP endpoint which should receive the POST requests for export.
    """

    def _get_batch_size(self):
        return self.__batch_size

    def _set_batch_size(self, value):
        if value is not None and not isinstance(value, int):
            raise TypeError("batch_size must be int")

        self.__batch_size = value

    batch_size = property(_get_batch_size, _set_batch_size)
    """
    The maximum size of a batch to send to the destination. Messages will be queued until the batch size is reached, after which they will then be uploaded. If unspecified the default will be 500.
    If both batchSize and batchIntervalMillis are specified, then messages will be eligible for upload when either condition is met.
    The minimum batch size is 1 and the maximum is 500.
    """

    def _get_batch_interval_millis(self):
        return self.__batch_interval_millis

    def _set_batch_interval_millis(self, value):
        if value is not None and not isinstance(value, int):
            raise TypeError("batch_interval_millis must be int")

        self.__batch_interval_millis = value

    batch_interval_millis = property(
        _get_batch_interval_millis, _set_batch_interval_millis
    )
    """
    The time in milliseconds between the earliest un-uploaded message and the current time. If this time is exceeded, messages will be uploaded in the next batch. If unspecified messages will be eligible for upload immediately.
    If both batchSize and batchIntervalMillis are specified, then messages will be eligible for upload when either condition is met.
    The minimum value is 60000 milliseconds and the maximum is 9223372036854 milliseconds.
    """

    def _get_priority(self):
        return self.__priority

    def _set_priority(self, value):
        if value is not None and not isinstance(value, int):
            raise TypeError("priority must be int")

        self.__priority = value

    priority = property(_get_priority, _set_priority)
    """
    Priority for this upload stream. Lower values are higher priority. If not specified it will have the lowest priority.
    """

    def _get_start_sequence_number(self):
        return self.__start_sequence_number

    def _set_start_sequence_number(self, value):
        if value is not None and not isinstance(value, int):
            raise TypeError("start_sequence_number must be int")

        self.__start_sequence_number = value

    start_sequence_number = property(
        _get_start_sequence_number, _set_start_sequence_number
    )
    """
    The sequence number of the message to use as the starting message in the export. Default is 0. The sequence number provided should be less than the newest sequence number in the stream, i.e., sequence number of the last messaged appended. To find the newest sequence number, describe the stream and then check the storage status of the returned MessageStreamInfo object.
    """

    def _get_disabled(self):
        return self.__disabled

    def _set_disabled(self, value):
        if value is not None and not isinstance(value, bool):
            raise TypeError("disabled must be bool")

        self.__disabled = value

    disabled = property(_get_disabled, _set_disabled)
    """
    Enable or disable this export. Default is false.
    """

    def _get_export_format(self):
        return self.__export_format

    def _set_export_format(self, value):
        if value is not None and not isinstance(value, ExportFormat):
            raise TypeError("export_format must be ExportFormat")

        self.__export_format = value

    export_format = property(_get_export_format, _set_export_format)
    """
    Defines how messages are batched and formatted in the export payload.
    """

    @staticmethod
    def from_dict(d):
        v = {}
        if "identifier" in d:
            v["identifier"] = (
                str.from_dict(d["identifier"])
                if hasattr(str, "from_dict")
                else d["identifier"]
            )
        if "uri" in d:
            v["uri"] = (
                str.from_dict(d["uri"]) if hasattr(str, "from_dict") else d["uri"]
            )
        if "batchSize" in d:
            v["batch_size"] = (
                int.from_dict(d["batchSize"])
                if hasattr(int, "from_dict")
                else d["batchSize"]
            )
        if "batchIntervalMillis" in d:
            v["batch_interval_millis"] = (
                int.from_dict(d["batchIntervalMillis"])
                if hasattr(int, "from_dict")
                else d["batchIntervalMillis"]
            )
        if "priority" in d:
            v["priority"] = (
                int.from_dict(d["priority"])
                if hasattr(int, "from_dict")
                else d["priority"]
            )
        if "startSequenceNumber" in d:
            v["start_sequence_number"] = (
                int.from_dict(d["startSequenceNumber"])
                if hasattr(int, "from_dict")
                else d["startSequenceNumber"]
            )
        if "disabled" in d:
            v["disabled"] = (
                bool.from_dict(d["disabled"])
                if hasattr(bool, "from_dict")
                else d["disabled"]
            )
        if "exportFormat" in d:
            v["export_format"] = (
                ExportFormat.from_dict(d["exportFormat"])
                if hasattr(ExportFormat, "from_dict")
                else d["exportFormat"]
            )
        return HTTPConfig(**v)

    def as_dict(self):
        d = {}
        if self.__identifier is not None:
            d["identifier"] = (
                self.__identifier.as_dict()
                if hasattr(self.__identifier, "as_dict")
                else self.__identifier
            )
        if self.__uri is not None:
            d["uri"] = (
                self.__uri.as_dict() if hasattr(self.__uri, "as_dict") else self.__uri
            )
        if self.__batch_size is not None:
            d["batchSize"] = (
                self.__batch_size.as_dict()
                if hasattr(self.__batch_size, "as_dict")
                else self.__batch_size
            )
        if self.__batch_interval_millis is not None:
            d["batchIntervalMillis"] = (
                self.__batch_interval_millis.as_dict()
                if hasattr(self.__batch_interval_millis, "as_dict")
                else self.__batch_interval_millis
            )
        if self.__priority is not None:
            d["priority"] = (
                self.__priority.as_dict()
                if hasattr(self.__priority, "as_dict")
                else self.__priority
            )
        if self.__start_sequence_number is not None:
            d["startSequenceNumber"] = (
                self.__start_sequence_number.as_dict()
                if hasattr(self.__start_sequence_number, "as_dict")
                else self.__start_sequence_number
            )
        if self.__disabled is not None:
            d["disabled"] = (
                self.__disabled.as_dict()
                if hasattr(self.__disabled, "as_dict")
                else self.__disabled
            )
        if self.__export_format is not None:
            d["exportFormat"] = (
                self.__export_format.as_dict()
                if hasattr(self.__export_format, "as_dict")
                else self.__export_format
            )
        return d

    def __repr__(self):
        return "<Class HTTPConfig. identifier: {}, uri: {}, batch_size: {}, batch_interval_millis: {}, priority: {}, start_sequence_number: {}, disabled: {}, export_format: {}>".format(
            limitedRepr(
                self.__identifier[:20]
                if isinstance(self.__identifier, bytes)
                else self.__identifier
            ),
            limitedRepr(
                self.__uri[:20] if isinstance(self.__uri, bytes) else self.__uri
            ),
            limitedRepr(
                self.__batch_size[:20]
                if isinstance(self.__batch_size, bytes)
                else self.__batch_size
            ),
            limitedRepr(
                self.__batch_interval_millis[:20]
                if isinstance(self.__batch_interval_millis, bytes)
                else self.__batch_interval_millis
            ),
            limitedRepr(
                self.__priority[:20]
                if isinstance(self.__priority, bytes)
                else self.__priority
            ),
            limitedRepr(
                self.__start_sequence_number[:20]
                if isinstance(self.__start_sequence_number, bytes)
                else self.__start_sequence_number
            ),
            limitedRepr(
                self.__disabled[:20]
                if isinstance(self.__disabled, bytes)
                else self.__disabled
            ),
            limitedRepr(
                self.__export_format[:20]
                if isinstance(self.__export_format, bytes)
                else self.__export_format
            ),
        )


class IoTAnalyticsConfig:
    """
    Configuration object for IoT Analytics export destination.
    """

    __slots__ = [
        "__identifier",
        "__iot_channel",
        "__iot_msg_id_prefix",
        "__batch_size",
        "__batch_interval_millis",
        "__priority",
        "__start_sequence_number",
        "__disabled",
    ]

    _types_map = {
        "identifier": {"type": str, "subtype": None},
        "iot_channel": {"type": str, "subtype": None},
        "iot_msg_id_prefix": {"type": str, "subtype": None},
        "batch_size": {"type": int, "subtype": None},
        "batch_interval_millis": {"type": int, "subtype": None},
        "priority": {"type": int, "subtype": None},
        "start_sequence_number": {"type": int, "subtype": None},
        "disabled": {"type": bool, "subtype": None},
    }
    _formats_map = {}
    _validations_map = {
        "identifier": {
            "required": True,
            "minLength": 1,
            "maxLength": 255,
            "pattern": "^[\w ,.\-_]*$",
        },
        "iot_channel": {"required": True, "minLength": 1,},
        "iot_msg_id_prefix": {"required": False, "maxLength": 32,},
        "batch_size": {"required": False, "maximum": 100, "minimum": 1,},
        "batch_interval_millis": {
            "required": False,
            "maximum": 9223372036854,
            "minimum": 60000,
        },
        "priority": {"required": False, "maximum": 10, "minimum": 1,},
        "start_sequence_number": {
            "required": False,
            "maximum": 9223372036854775807,
            "minimum": 0,
        },
        "disabled": {"required": False,},
    }

    def __init__(
        self,
        identifier: str = None,
        iot_channel: str = None,
        iot_msg_id_prefix: str = None,
        batch_size: int = None,
        batch_interval_millis: int = None,
        priority: int = None,
        start_sequence_number: int = None,
        disabled: bool = None,
    ):
        """
        :param identifier: A unique identifier to identify this individual upload stream.
            Must be an alphanumeric string including spaces, commas, periods, hyphens, and underscores with length between 1 and 255.
        :param iot_channel: The name of the IoT Analytics Channel that this exporter should upload to.
        :param iot_msg_id_prefix: A string prefixed to each unique message id. After this prefix, StreamManager may append more data to make the message ID unique.
            This prefix must be less than 32 characters.
        :param batch_size: The maximum size of a batch to send to IoT Analytics. Messages will be queued until the batch size is reached, after which they will then be uploaded. If unspecified the default will be 100.
            If both batchSize and batchIntervalMillis are specified, then messages will be eligible for upload when either condition is met.
            The batch size must be between 1 and 100.
        :param batch_interval_millis: The time in milliseconds between the earliest un-uploaded message and the current time. If this time is exceeded, messages will be uploaded in the next batch. If unspecified messages will be eligible for upload immediately.
            If both batchSize and batchIntervalMillis are specified, then messages will be eligible for upload when either condition is met.
            The minimum value is 60000 milliseconds and the maximum is 9223372036854 milliseconds.
        :param priority: Priority for this upload stream. Lower values are higher priority. If not specified it will have the lowest priority.
        :param start_sequence_number: The sequence number of the message to use as the starting message in the export. Default is 0. The sequence number provided should be less than the newest sequence number in the stream, i.e., sequence number of the last messaged appended. To find the newest sequence number, describe the stream and then check the storage status of the returned MessageStreamInfo object.
        :param disabled: Enable or disable this export. Default is false.
        """
        pass
        self.__identifier = identifier
        self.__iot_channel = iot_channel
        self.__iot_msg_id_prefix = iot_msg_id_prefix
        self.__batch_size = batch_size
        self.__batch_interval_millis = batch_interval_millis
        self.__priority = priority
        self.__start_sequence_number = start_sequence_number
        self.__disabled = disabled

    def _get_identifier(self):
        return self.__identifier

    def _set_identifier(self, value):
        if not isinstance(value, str):
            raise TypeError("identifier must be str")

        self.__identifier = value

    identifier = property(_get_identifier, _set_identifier)
    """
    A unique identifier to identify this individual upload stream.
    Must be an alphanumeric string including spaces, commas, periods, hyphens, and underscores with length between 1 and 255.
    """

    def _get_iot_channel(self):
        return self.__iot_channel

    def _set_iot_channel(self, value):
        if not isinstance(value, str):
            raise TypeError("iot_channel must be str")

        self.__iot_channel = value

    iot_channel = property(_get_iot_channel, _set_iot_channel)
    """
    The name of the IoT Analytics Channel that this exporter should upload to.
    """

    def _get_iot_msg_id_prefix(self):
        return self.__iot_msg_id_prefix

    def _set_iot_msg_id_prefix(self, value):
        if value is not None and not isinstance(value, str):
            raise TypeError("iot_msg_id_prefix must be str")

        self.__iot_msg_id_prefix = value

    iot_msg_id_prefix = property(_get_iot_msg_id_prefix, _set_iot_msg_id_prefix)
    """
    A string prefixed to each unique message id. After this prefix, StreamManager may append more data to make the message ID unique.
    This prefix must be less than 32 characters.
    """

    def _get_batch_size(self):
        return self.__batch_size

    def _set_batch_size(self, value):
        if value is not None and not isinstance(value, int):
            raise TypeError("batch_size must be int")

        self.__batch_size = value

    batch_size = property(_get_batch_size, _set_batch_size)
    """
    The maximum size of a batch to send to IoT Analytics. Messages will be queued until the batch size is reached, after which they will then be uploaded. If unspecified the default will be 100.
    If both batchSize and batchIntervalMillis are specified, then messages will be eligible for upload when either condition is met.
    The batch size must be between 1 and 100.
    """

    def _get_batch_interval_millis(self):
        return self.__batch_interval_millis

    def _set_batch_interval_millis(self, value):
        if value is not None and not isinstance(value, int):
            raise TypeError("batch_interval_millis must be int")

        self.__batch_interval_millis = value

    batch_interval_millis = property(
        _get_batch_interval_millis, _set_batch_interval_millis
    )
    """
    The time in milliseconds between the earliest un-uploaded message and the current time. If this time is exceeded, messages will be uploaded in the next batch. If unspecified messages will be eligible for upload immediately.
    If both batchSize and batchIntervalMillis are specified, then messages will be eligible for upload when either condition is met.
    The minimum value is 60000 milliseconds and the maximum is 9223372036854 milliseconds.
    """

    def _get_priority(self):
        return self.__priority

    def _set_priority(self, value):
        if value is not None and not isinstance(value, int):
            raise TypeError("priority must be int")

        self.__priority = value

    priority = property(_get_priority, _set_priority)
    """
    Priority for this upload stream. Lower values are higher priority. If not specified it will have the lowest priority.
    """

    def _get_start_sequence_number(self):
        return self.__start_sequence_number

    def _set_start_sequence_number(self, value):
        if value is not None and not isinstance(value, int):
            raise TypeError("start_sequence_number must be int")

        self.__start_sequence_number = value

    start_sequence_number = property(
        _get_start_sequence_number, _set_start_sequence_number
    )
    """
    The sequence number of the message to use as the starting message in the export. Default is 0. The sequence number provided should be less than the newest sequence number in the stream, i.e., sequence number of the last messaged appended. To find the newest sequence number, describe the stream and then check the storage status of the returned MessageStreamInfo object.
    """

    def _get_disabled(self):
        return self.__disabled

    def _set_disabled(self, value):
        if value is not None and not isinstance(value, bool):
            raise TypeError("disabled must be bool")

        self.__disabled = value

    disabled = property(_get_disabled, _set_disabled)
    """
    Enable or disable this export. Default is false.
    """

    @staticmethod
    def from_dict(d):
        v = {}
        if "identifier" in d:
            v["identifier"] = (
                str.from_dict(d["identifier"])
                if hasattr(str, "from_dict")
                else d["identifier"]
            )
        if "iotChannel" in d:
            v["iot_channel"] = (
                str.from_dict(d["iotChannel"])
                if hasattr(str, "from_dict")
                else d["iotChannel"]
            )
        if "iotMsgIdPrefix" in d:
            v["iot_msg_id_prefix"] = (
                str.from_dict(d["iotMsgIdPrefix"])
                if hasattr(str, "from_dict")
                else d["iotMsgIdPrefix"]
            )
        if "batchSize" in d:
            v["batch_size"] = (
                int.from_dict(d["batchSize"])
                if hasattr(int, "from_dict")
                else d["batchSize"]
            )
        if "batchIntervalMillis" in d:
            v["batch_interval_millis"] = (
                int.from_dict(d["batchIntervalMillis"])
                if hasattr(int, "from_dict")
                else d["batchIntervalMillis"]
            )
        if "priority" in d:
            v["priority"] = (
                int.from_dict(d["priority"])
                if hasattr(int, "from_dict")
                else d["priority"]
            )
        if "startSequenceNumber" in d:
            v["start_sequence_number"] = (
                int.from_dict(d["startSequenceNumber"])
                if hasattr(int, "from_dict")
                else d["startSequenceNumber"]
            )
        if "disabled" in d:
            v["disabled"] = (
                bool.from_dict(d["disabled"])
                if hasattr(bool, "from_dict")
                else d["disabled"]
            )
        return IoTAnalyticsConfig(**v)

    def as_dict(self):
        d = {}
        if self.__identifier is not None:
            d["identifier"] = (
                self.__identifier.as_dict()
                if hasattr(self.__identifier, "as_dict")
                else self.__identifier
            )
        if self.__iot_channel is not None:
            d["iotChannel"] = (
                self.__iot_channel.as_dict()
                if hasattr(self.__iot_channel, "as_dict")
                else self.__iot_channel
            )
        if self.__iot_msg_id_prefix is not None:
            d["iotMsgIdPrefix"] = (
                self.__iot_msg_id_prefix.as_dict()
                if hasattr(self.__iot_msg_id_prefix, "as_dict")
                else self.__iot_msg_id_prefix
            )
        if self.__batch_size is not None:
            d["batchSize"] = (
                self.__batch_size.as_dict()
                if hasattr(self.__batch_size, "as_dict")
                else self.__batch_size
            )
        if self.__batch_interval_millis is not None:
            d["batchIntervalMillis"] = (
                self.__batch_interval_millis.as_dict()
                if hasattr(self.__batch_interval_millis, "as_dict")
                else self.__batch_interval_millis
            )
        if self.__priority is not None:
            d["priority"] = (
                self.__priority.as_dict()
                if hasattr(self.__priority, "as_dict")
                else self.__priority
            )
        if self.__start_sequence_number is not None:
            d["startSequenceNumber"] = (
                self.__start_sequence_number.as_dict()
                if hasattr(self.__start_sequence_number, "as_dict")
                else self.__start_sequence_number
            )
        if self.__disabled is not None:
            d["disabled"] = (
                self.__disabled.as_dict()
                if hasattr(self.__disabled, "as_dict")
                else self.__disabled
            )
        return d

    def __repr__(self):
        return "<Class IoTAnalyticsConfig. identifier: {}, iot_channel: {}, iot_msg_id_prefix: {}, batch_size: {}, batch_interval_millis: {}, priority: {}, start_sequence_number: {}, disabled: {}>".format(
            limitedRepr(
                self.__identifier[:20]
                if isinstance(self.__identifier, bytes)
                else self.__identifier
            ),
            limitedRepr(
                self.__iot_channel[:20]
                if isinstance(self.__iot_channel, bytes)
                else self.__iot_channel
            ),
            limitedRepr(
                self.__iot_msg_id_prefix[:20]
                if isinstance(self.__iot_msg_id_prefix, bytes)
                else self.__iot_msg_id_prefix
            ),
            limitedRepr(
                self.__batch_size[:20]
                if isinstance(self.__batch_size, bytes)
                else self.__batch_size
            ),
            limitedRepr(
                self.__batch_interval_millis[:20]
                if isinstance(self.__batch_interval_millis, bytes)
                else self.__batch_interval_millis
            ),
            limitedRepr(
                self.__priority[:20]
                if isinstance(self.__priority, bytes)
                else self.__priority
            ),
            limitedRepr(
                self.__start_sequence_number[:20]
                if isinstance(self.__start_sequence_number, bytes)
                else self.__start_sequence_number
            ),
            limitedRepr(
                self.__disabled[:20]
                if isinstance(self.__disabled, bytes)
                else self.__disabled
            ),
        )


class IoTSiteWiseConfig:
    """
    Configuration object for IotSiteWise data streams export destination. Minimum version requirements: StreamManager server version 1.1 (or AWS IoT Greengrass Core 1.11.0)
    """

    __slots__ = [
        "__identifier",
        "__batch_size",
        "__batch_interval_millis",
        "__priority",
        "__start_sequence_number",
        "__disabled",
    ]

    _types_map = {
        "identifier": {"type": str, "subtype": None},
        "batch_size": {"type": int, "subtype": None},
        "batch_interval_millis": {"type": int, "subtype": None},
        "priority": {"type": int, "subtype": None},
        "start_sequence_number": {"type": int, "subtype": None},
        "disabled": {"type": bool, "subtype": None},
    }
    _formats_map = {}
    _validations_map = {
        "identifier": {
            "required": True,
            "minLength": 1,
            "maxLength": 255,
            "pattern": "^[\w ,.\-_]*$",
        },
        "batch_size": {"required": False, "maximum": 10, "minimum": 1,},
        "batch_interval_millis": {
            "required": False,
            "maximum": 9223372036854,
            "minimum": 60000,
        },
        "priority": {"required": False, "maximum": 10, "minimum": 1,},
        "start_sequence_number": {
            "required": False,
            "maximum": 9223372036854775807,
            "minimum": 0,
        },
        "disabled": {"required": False,},
    }

    def __init__(
        self,
        identifier: str = None,
        batch_size: int = None,
        batch_interval_millis: int = None,
        priority: int = None,
        start_sequence_number: int = None,
        disabled: bool = None,
    ):
        """
        :param identifier: A unique identifier to identify this individual upload stream.
            Must be an alphanumeric string including spaces, commas, periods, hyphens, and underscores with length between 1 and 255.
        :param batch_size: The maximum size of a batch to send to the destination. Messages will be queued until the batch size is reached, after which they will then be uploaded. If unspecified the default will be 10.
            If both batchSize and batchIntervalMillis are specified, then messages will be eligible for upload when either condition is met.
            The minimum batch size is 1 and the maximum is 10.
        :param batch_interval_millis: The time in milliseconds between the earliest un-uploaded message and the current time. If this time is exceeded, messages will be uploaded in the next batch. If unspecified messages will be eligible for upload immediately.
            If both batchSize and batchIntervalMillis are specified, then messages will be eligible for upload when either condition is met.
            The minimum value is 60000 milliseconds and the maximum is 9223372036854 milliseconds.
        :param priority: Priority for this upload stream. Lower values are higher priority. If not specified it will have the lowest priority.
        :param start_sequence_number: The sequence number of the message to use as the starting message in the export. Default is 0. The sequence number provided should be less than the newest sequence number in the stream, i.e., sequence number of the last messaged appended. To find the newest sequence number, describe the stream and then check the storage status of the returned MessageStreamInfo object.
        :param disabled: Enable or disable this export. Default is false.
        """
        pass
        self.__identifier = identifier
        self.__batch_size = batch_size
        self.__batch_interval_millis = batch_interval_millis
        self.__priority = priority
        self.__start_sequence_number = start_sequence_number
        self.__disabled = disabled

    def _get_identifier(self):
        return self.__identifier

    def _set_identifier(self, value):
        if not isinstance(value, str):
            raise TypeError("identifier must be str")

        self.__identifier = value

    identifier = property(_get_identifier, _set_identifier)
    """
    A unique identifier to identify this individual upload stream.
    Must be an alphanumeric string including spaces, commas, periods, hyphens, and underscores with length between 1 and 255.
    """

    def _get_batch_size(self):
        return self.__batch_size

    def _set_batch_size(self, value):
        if value is not None and not isinstance(value, int):
            raise TypeError("batch_size must be int")

        self.__batch_size = value

    batch_size = property(_get_batch_size, _set_batch_size)
    """
    The maximum size of a batch to send to the destination. Messages will be queued until the batch size is reached, after which they will then be uploaded. If unspecified the default will be 10.
    If both batchSize and batchIntervalMillis are specified, then messages will be eligible for upload when either condition is met.
    The minimum batch size is 1 and the maximum is 10.
    """

    def _get_batch_interval_millis(self):
        return self.__batch_interval_millis

    def _set_batch_interval_millis(self, value):
        if value is not None and not isinstance(value, int):
            raise TypeError("batch_interval_millis must be int")

        self.__batch_interval_millis = value

    batch_interval_millis = property(
        _get_batch_interval_millis, _set_batch_interval_millis
    )
    """
    The time in milliseconds between the earliest un-uploaded message and the current time. If this time is exceeded, messages will be uploaded in the next batch. If unspecified messages will be eligible for upload immediately.
    If both batchSize and batchIntervalMillis are specified, then messages will be eligible for upload when either condition is met.
    The minimum value is 60000 milliseconds and the maximum is 9223372036854 milliseconds.
    """

    def _get_priority(self):
        return self.__priority

    def _set_priority(self, value):
        if value is not None and not isinstance(value, int):
            raise TypeError("priority must be int")

        self.__priority = value

    priority = property(_get_priority, _set_priority)
    """
    Priority for this upload stream. Lower values are higher priority. If not specified it will have the lowest priority.
    """

    def _get_start_sequence_number(self):
        return self.__start_sequence_number

    def _set_start_sequence_number(self, value):
        if value is not None and not isinstance(value, int):
            raise TypeError("start_sequence_number must be int")

        self.__start_sequence_number = value

    start_sequence_number = property(
        _get_start_sequence_number, _set_start_sequence_number
    )
    """
    The sequence number of the message to use as the starting message in the export. Default is 0. The sequence number provided should be less than the newest sequence number in the stream, i.e., sequence number of the last messaged appended. To find the newest sequence number, describe the stream and then check the storage status of the returned MessageStreamInfo object.
    """

    def _get_disabled(self):
        return self.__disabled

    def _set_disabled(self, value):
        if value is not None and not isinstance(value, bool):
            raise TypeError("disabled must be bool")

        self.__disabled = value

    disabled = property(_get_disabled, _set_disabled)
    """
    Enable or disable this export. Default is false.
    """

    @staticmethod
    def from_dict(d):
        v = {}
        if "identifier" in d:
            v["identifier"] = (
                str.from_dict(d["identifier"])
                if hasattr(str, "from_dict")
                else d["identifier"]
            )
        if "batchSize" in d:
            v["batch_size"] = (
                int.from_dict(d["batchSize"])
                if hasattr(int, "from_dict")
                else d["batchSize"]
            )
        if "batchIntervalMillis" in d:
            v["batch_interval_millis"] = (
                int.from_dict(d["batchIntervalMillis"])
                if hasattr(int, "from_dict")
                else d["batchIntervalMillis"]
            )
        if "priority" in d:
            v["priority"] = (
                int.from_dict(d["priority"])
                if hasattr(int, "from_dict")
                else d["priority"]
            )
        if "startSequenceNumber" in d:
            v["start_sequence_number"] = (
                int.from_dict(d["startSequenceNumber"])
                if hasattr(int, "from_dict")
                else d["startSequenceNumber"]
            )
        if "disabled" in d:
            v["disabled"] = (
                bool.from_dict(d["disabled"])
                if hasattr(bool, "from_dict")
                else d["disabled"]
            )
        return IoTSiteWiseConfig(**v)

    def as_dict(self):
        d = {}
        if self.__identifier is not None:
            d["identifier"] = (
                self.__identifier.as_dict()
                if hasattr(self.__identifier, "as_dict")
                else self.__identifier
            )
        if self.__batch_size is not None:
            d["batchSize"] = (
                self.__batch_size.as_dict()
                if hasattr(self.__batch_size, "as_dict")
                else self.__batch_size
            )
        if self.__batch_interval_millis is not None:
            d["batchIntervalMillis"] = (
                self.__batch_interval_millis.as_dict()
                if hasattr(self.__batch_interval_millis, "as_dict")
                else self.__batch_interval_millis
            )
        if self.__priority is not None:
            d["priority"] = (
                self.__priority.as_dict()
                if hasattr(self.__priority, "as_dict")
                else self.__priority
            )
        if self.__start_sequence_number is not None:
            d["startSequenceNumber"] = (
                self.__start_sequence_number.as_dict()
                if hasattr(self.__start_sequence_number, "as_dict")
                else self.__start_sequence_number
            )
        if self.__disabled is not None:
            d["disabled"] = (
                self.__disabled.as_dict()
                if hasattr(self.__disabled, "as_dict")
                else self.__disabled
            )
        return d

    def __repr__(self):
        return "<Class IoTSiteWiseConfig. identifier: {}, batch_size: {}, batch_interval_millis: {}, priority: {}, start_sequence_number: {}, disabled: {}>".format(
            limitedRepr(
                self.__identifier[:20]
                if isinstance(self.__identifier, bytes)
                else self.__identifier
            ),
            limitedRepr(
                self.__batch_size[:20]
                if isinstance(self.__batch_size, bytes)
                else self.__batch_size
            ),
            limitedRepr(
                self.__batch_interval_millis[:20]
                if isinstance(self.__batch_interval_millis, bytes)
                else self.__batch_interval_millis
            ),
            limitedRepr(
                self.__priority[:20]
                if isinstance(self.__priority, bytes)
                else self.__priority
            ),
            limitedRepr(
                self.__start_sequence_number[:20]
                if isinstance(self.__start_sequence_number, bytes)
                else self.__start_sequence_number
            ),
            limitedRepr(
                self.__disabled[:20]
                if isinstance(self.__disabled, bytes)
                else self.__disabled
            ),
        )


class ExportDefinition:
    """
    Defines how and where the stream is uploaded.
    """

    __slots__ = [
        "__http",
        "__iot_analytics",
        "__kinesis",
        "__iot_sitewise",
        "__s3_task_executor",
    ]

    _types_map = {
        "http": {"type": list, "subtype": HTTPConfig},
        "iot_analytics": {"type": list, "subtype": IoTAnalyticsConfig},
        "kinesis": {"type": list, "subtype": KinesisConfig},
        "iot_sitewise": {"type": list, "subtype": IoTSiteWiseConfig},
        "s3_task_executor": {"type": list, "subtype": S3ExportTaskExecutorConfig},
    }
    _formats_map = {}
    _validations_map = {
        "http": {"required": False,},
        "iot_analytics": {"required": False,},
        "kinesis": {"required": False,},
        "iot_sitewise": {"required": False,},
        "s3_task_executor": {"required": False,},
    }

    def __init__(
        self,
        http: List[HTTPConfig] = None,
        iot_analytics: List[IoTAnalyticsConfig] = None,
        kinesis: List[KinesisConfig] = None,
        iot_sitewise: List[IoTSiteWiseConfig] = None,
        s3_task_executor: List[S3ExportTaskExecutorConfig] = None,
    ):
        """
        :param http: Defines how the stream is uploaded to an HTTP endpoint.
        :param iot_analytics: Defines how the stream is uploaded to IoT Analytics.
        :param kinesis: Defines how the stream is uploaded to Kinesis.
        :param iot_sitewise: Defines how the stream is uploaded to IoT SiteWise.
        :param s3_task_executor: Defines the list of configs for S3 task executors.
        """
        pass
        self.__http = http
        self.__iot_analytics = iot_analytics
        self.__kinesis = kinesis
        self.__iot_sitewise = iot_sitewise
        self.__s3_task_executor = s3_task_executor

    def _get_http(self):
        return self.__http

    def _set_http(self, value):
        if value is not None and not isinstance(value, list):
            raise TypeError("http must be list")
        if value is not None and not all(isinstance(i, HTTPConfig) for i in value):
            raise TypeError("http list values must be HTTPConfig")

        self.__http = value

    http = property(_get_http, _set_http)
    """
    Defines how the stream is uploaded to an HTTP endpoint.
    """

    def _get_iot_analytics(self):
        return self.__iot_analytics

    def _set_iot_analytics(self, value):
        if value is not None and not isinstance(value, list):
            raise TypeError("iot_analytics must be list")
        if value is not None and not all(
            isinstance(i, IoTAnalyticsConfig) for i in value
        ):
            raise TypeError("iot_analytics list values must be IoTAnalyticsConfig")

        self.__iot_analytics = value

    iot_analytics = property(_get_iot_analytics, _set_iot_analytics)
    """
    Defines how the stream is uploaded to IoT Analytics.
    """

    def _get_kinesis(self):
        return self.__kinesis

    def _set_kinesis(self, value):
        if value is not None and not isinstance(value, list):
            raise TypeError("kinesis must be list")
        if value is not None and not all(isinstance(i, KinesisConfig) for i in value):
            raise TypeError("kinesis list values must be KinesisConfig")

        self.__kinesis = value

    kinesis = property(_get_kinesis, _set_kinesis)
    """
    Defines how the stream is uploaded to Kinesis.
    """

    def _get_iot_sitewise(self):
        return self.__iot_sitewise

    def _set_iot_sitewise(self, value):
        if value is not None and not isinstance(value, list):
            raise TypeError("iot_sitewise must be list")
        if value is not None and not all(
            isinstance(i, IoTSiteWiseConfig) for i in value
        ):
            raise TypeError("iot_sitewise list values must be IoTSiteWiseConfig")

        self.__iot_sitewise = value

    iot_sitewise = property(_get_iot_sitewise, _set_iot_sitewise)
    """
    Defines how the stream is uploaded to IoT SiteWise.
    """

    def _get_s3_task_executor(self):
        return self.__s3_task_executor

    def _set_s3_task_executor(self, value):
        if value is not None and not isinstance(value, list):
            raise TypeError("s3_task_executor must be list")
        if value is not None and not all(
            isinstance(i, S3ExportTaskExecutorConfig) for i in value
        ):
            raise TypeError(
                "s3_task_executor list values must be S3ExportTaskExecutorConfig"
            )

        self.__s3_task_executor = value

    s3_task_executor = property(_get_s3_task_executor, _set_s3_task_executor)
    """
    Defines the list of configs for S3 task executors.
    """

    @staticmethod
    def from_dict(d):
        v = {}
        if "http" in d:
            v["http"] = [
                HTTPConfig.from_dict(p) if hasattr(HTTPConfig, "from_dict") else p
                for p in d["http"]
            ]
        if "iotAnalytics" in d:
            v["iot_analytics"] = [
                IoTAnalyticsConfig.from_dict(p)
                if hasattr(IoTAnalyticsConfig, "from_dict")
                else p
                for p in d["iotAnalytics"]
            ]
        if "kinesis" in d:
            v["kinesis"] = [
                KinesisConfig.from_dict(p) if hasattr(KinesisConfig, "from_dict") else p
                for p in d["kinesis"]
            ]
        if "IotSitewise" in d:
            v["iot_sitewise"] = [
                IoTSiteWiseConfig.from_dict(p)
                if hasattr(IoTSiteWiseConfig, "from_dict")
                else p
                for p in d["IotSitewise"]
            ]
        if "s3TaskExecutor" in d:
            v["s3_task_executor"] = [
                S3ExportTaskExecutorConfig.from_dict(p)
                if hasattr(S3ExportTaskExecutorConfig, "from_dict")
                else p
                for p in d["s3TaskExecutor"]
            ]
        return ExportDefinition(**v)

    def as_dict(self):
        d = {}
        if self.__http is not None:
            d["http"] = [
                p.as_dict() if hasattr(p, "as_dict") else p for p in self.__http
            ]
        if self.__iot_analytics is not None:
            d["iotAnalytics"] = [
                p.as_dict() if hasattr(p, "as_dict") else p
                for p in self.__iot_analytics
            ]
        if self.__kinesis is not None:
            d["kinesis"] = [
                p.as_dict() if hasattr(p, "as_dict") else p for p in self.__kinesis
            ]
        if self.__iot_sitewise is not None:
            d["IotSitewise"] = [
                p.as_dict() if hasattr(p, "as_dict") else p for p in self.__iot_sitewise
            ]
        if self.__s3_task_executor is not None:
            d["s3TaskExecutor"] = [
                p.as_dict() if hasattr(p, "as_dict") else p
                for p in self.__s3_task_executor
            ]
        return d

    def __repr__(self):
        return "<Class ExportDefinition. http: {}, iot_analytics: {}, kinesis: {}, iot_sitewise: {}, s3_task_executor: {}>".format(
            limitedRepr(
                self.__http[:20] if isinstance(self.__http, bytes) else self.__http
            ),
            limitedRepr(
                self.__iot_analytics[:20]
                if isinstance(self.__iot_analytics, bytes)
                else self.__iot_analytics
            ),
            limitedRepr(
                self.__kinesis[:20]
                if isinstance(self.__kinesis, bytes)
                else self.__kinesis
            ),
            limitedRepr(
                self.__iot_sitewise[:20]
                if isinstance(self.__iot_sitewise, bytes)
                else self.__iot_sitewise
            ),
            limitedRepr(
                self.__s3_task_executor[:20]
                if isinstance(self.__s3_task_executor, bytes)
                else self.__s3_task_executor
            ),
        )


class StrategyOnFull(enum.Enum):
    """
    StrategyOnFull is used in the MessageStreamDefinition when creating a stream.
    It defines the behavior when the stream has reached the maximum size.
    RejectNewData: any append message request after the stream is full will be rejected with an exception.
    OverwriteOldestData: the oldest stream segments will be deleted until there is room for the new message.
    """

    RejectNewData = 0
    OverwriteOldestData = 1

    @staticmethod
    def from_dict(d):
        return StrategyOnFull(d)

    def as_dict(self):
        return self.value

    def __repr__(self):
        return "<Enum StrategyOnFull. {}: {}>".format(
            limitedRepr(self.name), limitedRepr(self.value)
        )


class Persistence(enum.Enum):
    """
    Stream persistence. If set to File, the file system will be used to persist messages long-term and is resilient to restarts.
    Memory should be used when performance matters more than durability as it only stores the stream in memory and never writes to the disk.
    """

    File = 0
    Memory = 1

    @staticmethod
    def from_dict(d):
        return Persistence(d)

    def as_dict(self):
        return self.value

    def __repr__(self):
        return "<Enum Persistence. {}: {}>".format(
            limitedRepr(self.name), limitedRepr(self.value)
        )


class MessageStreamDefinition:
    """
    Object defining a message stream used in the CreateMessageStream and UpdateMessageStream API.
    """

    __slots__ = [
        "__name",
        "__max_size",
        "__stream_segment_size",
        "__time_to_live_millis",
        "__strategy_on_full",
        "__persistence",
        "__flush_on_write",
        "__export_definition",
    ]

    _types_map = {
        "name": {"type": str, "subtype": None},
        "max_size": {"type": int, "subtype": None},
        "stream_segment_size": {"type": int, "subtype": None},
        "time_to_live_millis": {"type": int, "subtype": None},
        "strategy_on_full": {"type": StrategyOnFull, "subtype": None},
        "persistence": {"type": Persistence, "subtype": None},
        "flush_on_write": {"type": bool, "subtype": None},
        "export_definition": {"type": ExportDefinition, "subtype": None},
    }
    _formats_map = {}
    _validations_map = {
        "name": {
            "required": True,
            "minLength": 1,
            "maxLength": 255,
            "pattern": "^[\w ,.\-_]*$",
        },
        "max_size": {
            "required": False,
            "maximum": 9223372036854775807,
            "minimum": 1024,
        },
        "stream_segment_size": {
            "required": False,
            "maximum": 2147483647,
            "minimum": 1024,
        },
        "time_to_live_millis": {
            "required": False,
            "maximum": 9223372036854,
            "minimum": 60000,
        },
        "strategy_on_full": {"required": True,},
        "persistence": {"required": False,},
        "flush_on_write": {"required": False,},
        "export_definition": {"required": False,},
    }

    def __init__(
        self,
        name: str = None,
        max_size: int = 268435456,
        stream_segment_size: int = 16777216,
        time_to_live_millis: int = None,
        strategy_on_full: StrategyOnFull = None,
        persistence: Persistence = None,
        flush_on_write: bool = None,
        export_definition: ExportDefinition = None,
    ):
        """
        :param name: The unique name of the stream.
            Must be an alphanumeric string including spaces, commas, periods, hyphens, and underscores with length between 1 and 255.
        :param max_size: The maximum size in bytes for the entire stream. Set to 256MB by default with a minimum of 1KB and a maximum of 8192PB.
        :param stream_segment_size: The size of each segment of the stream. Set to 16MB by default with a minimum of 1KB and a maximum of 2GB.
            Data is only deleted segment by segment, so the segment size is the smallest amount of data which can be deleted.
        :param time_to_live_millis: Time to live for each message in milliseconds. Data may be deleted at any time after the TTL expires; deletion is not guaranteed to occur immediately when the TTL expires.
            The minimum value is 60000 milliseconds and the maximum is 9223372036854 milliseconds.
        :param strategy_on_full: What to do when the maximum size of the stream is reached.
            RejectNewData: any append message request after the stream is full will be rejected with an exception.
            OverwriteOldestData: the oldest stream segments will be deleted until there is room for the new message.
        :param persistence: Stream persistence. If set to File, the file system will be used to persist messages long-term and is resilient to restarts.
            Memory should be used when performance matters more than durability as it only stores the stream in memory and never writes to the disk.
        :param flush_on_write: This only applies when Persistence is set to File mode.
            Waits for the filesystem to complete the write for every message. This is safer, but slower. Default is false.
        :param export_definition: Defines how and where the stream is uploaded. See the definition of the ExportDefinition object for more detail.
        """
        pass
        self.__name = name
        self.__max_size = max_size
        self.__stream_segment_size = stream_segment_size
        self.__time_to_live_millis = time_to_live_millis
        self.__strategy_on_full = strategy_on_full
        self.__persistence = persistence
        self.__flush_on_write = flush_on_write
        self.__export_definition = export_definition

    def _get_name(self):
        return self.__name

    def _set_name(self, value):
        if not isinstance(value, str):
            raise TypeError("name must be str")

        self.__name = value

    name = property(_get_name, _set_name)
    """
    The unique name of the stream.
    Must be an alphanumeric string including spaces, commas, periods, hyphens, and underscores with length between 1 and 255.
    """

    def _get_max_size(self):
        return self.__max_size

    def _set_max_size(self, value):
        if value is not None and not isinstance(value, int):
            raise TypeError("max_size must be int")

        self.__max_size = value

    max_size = property(_get_max_size, _set_max_size)
    """
    The maximum size in bytes for the entire stream. Set to 256MB by default with a minimum of 1KB and a maximum of 8192PB.
    """

    def _get_stream_segment_size(self):
        return self.__stream_segment_size

    def _set_stream_segment_size(self, value):
        if value is not None and not isinstance(value, int):
            raise TypeError("stream_segment_size must be int")

        self.__stream_segment_size = value

    stream_segment_size = property(_get_stream_segment_size, _set_stream_segment_size)
    """
    The size of each segment of the stream. Set to 16MB by default with a minimum of 1KB and a maximum of 2GB.
    Data is only deleted segment by segment, so the segment size is the smallest amount of data which can be deleted.
    """

    def _get_time_to_live_millis(self):
        return self.__time_to_live_millis

    def _set_time_to_live_millis(self, value):
        if value is not None and not isinstance(value, int):
            raise TypeError("time_to_live_millis must be int")

        self.__time_to_live_millis = value

    time_to_live_millis = property(_get_time_to_live_millis, _set_time_to_live_millis)
    """
    Time to live for each message in milliseconds. Data may be deleted at any time after the TTL expires; deletion is not guaranteed to occur immediately when the TTL expires.
    The minimum value is 60000 milliseconds and the maximum is 9223372036854 milliseconds.
    """

    def _get_strategy_on_full(self):
        return self.__strategy_on_full

    def _set_strategy_on_full(self, value):
        if not isinstance(value, StrategyOnFull):
            raise TypeError("strategy_on_full must be StrategyOnFull")

        self.__strategy_on_full = value

    strategy_on_full = property(_get_strategy_on_full, _set_strategy_on_full)
    """
    What to do when the maximum size of the stream is reached.
    RejectNewData: any append message request after the stream is full will be rejected with an exception.
    OverwriteOldestData: the oldest stream segments will be deleted until there is room for the new message.
    """

    def _get_persistence(self):
        return self.__persistence

    def _set_persistence(self, value):
        if value is not None and not isinstance(value, Persistence):
            raise TypeError("persistence must be Persistence")

        self.__persistence = value

    persistence = property(_get_persistence, _set_persistence)
    """
    Stream persistence. If set to File, the file system will be used to persist messages long-term and is resilient to restarts.
    Memory should be used when performance matters more than durability as it only stores the stream in memory and never writes to the disk.
    """

    def _get_flush_on_write(self):
        return self.__flush_on_write

    def _set_flush_on_write(self, value):
        if value is not None and not isinstance(value, bool):
            raise TypeError("flush_on_write must be bool")

        self.__flush_on_write = value

    flush_on_write = property(_get_flush_on_write, _set_flush_on_write)
    """
    This only applies when Persistence is set to File mode.
    Waits for the filesystem to complete the write for every message. This is safer, but slower. Default is false.
    """

    def _get_export_definition(self):
        return self.__export_definition

    def _set_export_definition(self, value):
        if value is not None and not isinstance(value, ExportDefinition):
            raise TypeError("export_definition must be ExportDefinition")

        self.__export_definition = value

    export_definition = property(_get_export_definition, _set_export_definition)
    """
    Defines how and where the stream is uploaded. See the definition of the ExportDefinition object for more detail.
    """

    @staticmethod
    def from_dict(d):
        v = {}
        if "name" in d:
            v["name"] = (
                str.from_dict(d["name"]) if hasattr(str, "from_dict") else d["name"]
            )
        if "maxSize" in d:
            v["max_size"] = (
                int.from_dict(d["maxSize"])
                if hasattr(int, "from_dict")
                else d["maxSize"]
            )
        if "streamSegmentSize" in d:
            v["stream_segment_size"] = (
                int.from_dict(d["streamSegmentSize"])
                if hasattr(int, "from_dict")
                else d["streamSegmentSize"]
            )
        if "timeToLiveMillis" in d:
            v["time_to_live_millis"] = (
                int.from_dict(d["timeToLiveMillis"])
                if hasattr(int, "from_dict")
                else d["timeToLiveMillis"]
            )
        if "strategyOnFull" in d:
            v["strategy_on_full"] = (
                StrategyOnFull.from_dict(d["strategyOnFull"])
                if hasattr(StrategyOnFull, "from_dict")
                else d["strategyOnFull"]
            )
        if "persistence" in d:
            v["persistence"] = (
                Persistence.from_dict(d["persistence"])
                if hasattr(Persistence, "from_dict")
                else d["persistence"]
            )
        if "flushOnWrite" in d:
            v["flush_on_write"] = (
                bool.from_dict(d["flushOnWrite"])
                if hasattr(bool, "from_dict")
                else d["flushOnWrite"]
            )
        if "exportDefinition" in d:
            v["export_definition"] = (
                ExportDefinition.from_dict(d["exportDefinition"])
                if hasattr(ExportDefinition, "from_dict")
                else d["exportDefinition"]
            )
        return MessageStreamDefinition(**v)

    def as_dict(self):
        d = {}
        if self.__name is not None:
            d["name"] = (
                self.__name.as_dict()
                if hasattr(self.__name, "as_dict")
                else self.__name
            )
        if self.__max_size is not None:
            d["maxSize"] = (
                self.__max_size.as_dict()
                if hasattr(self.__max_size, "as_dict")
                else self.__max_size
            )
        if self.__stream_segment_size is not None:
            d["streamSegmentSize"] = (
                self.__stream_segment_size.as_dict()
                if hasattr(self.__stream_segment_size, "as_dict")
                else self.__stream_segment_size
            )
        if self.__time_to_live_millis is not None:
            d["timeToLiveMillis"] = (
                self.__time_to_live_millis.as_dict()
                if hasattr(self.__time_to_live_millis, "as_dict")
                else self.__time_to_live_millis
            )
        if self.__strategy_on_full is not None:
            d["strategyOnFull"] = (
                self.__strategy_on_full.as_dict()
                if hasattr(self.__strategy_on_full, "as_dict")
                else self.__strategy_on_full
            )
        if self.__persistence is not None:
            d["persistence"] = (
                self.__persistence.as_dict()
                if hasattr(self.__persistence, "as_dict")
                else self.__persistence
            )
        if self.__flush_on_write is not None:
            d["flushOnWrite"] = (
                self.__flush_on_write.as_dict()
                if hasattr(self.__flush_on_write, "as_dict")
                else self.__flush_on_write
            )
        if self.__export_definition is not None:
            d["exportDefinition"] = (
                self.__export_definition.as_dict()
                if hasattr(self.__export_definition, "as_dict")
                else self.__export_definition
            )
        return d

    def __repr__(self):
        return "<Class MessageStreamDefinition. name: {}, max_size: {}, stream_segment_size: {}, time_to_live_millis: {}, strategy_on_full: {}, persistence: {}, flush_on_write: {}, export_definition: {}>".format(
            limitedRepr(
                self.__name[:20] if isinstance(self.__name, bytes) else self.__name
            ),
            limitedRepr(
                self.__max_size[:20]
                if isinstance(self.__max_size, bytes)
                else self.__max_size
            ),
            limitedRepr(
                self.__stream_segment_size[:20]
                if isinstance(self.__stream_segment_size, bytes)
                else self.__stream_segment_size
            ),
            limitedRepr(
                self.__time_to_live_millis[:20]
                if isinstance(self.__time_to_live_millis, bytes)
                else self.__time_to_live_millis
            ),
            limitedRepr(
                self.__strategy_on_full[:20]
                if isinstance(self.__strategy_on_full, bytes)
                else self.__strategy_on_full
            ),
            limitedRepr(
                self.__persistence[:20]
                if isinstance(self.__persistence, bytes)
                else self.__persistence
            ),
            limitedRepr(
                self.__flush_on_write[:20]
                if isinstance(self.__flush_on_write, bytes)
                else self.__flush_on_write
            ),
            limitedRepr(
                self.__export_definition[:20]
                if isinstance(self.__export_definition, bytes)
                else self.__export_definition
            ),
        )


class CreateMessageStreamRequest:
    """
    (Internal Only) Request object for creating a message stream.
    """

    __slots__ = [
        "__request_id",
        "__definition",
    ]

    _types_map = {
        "request_id": {"type": str, "subtype": None},
        "definition": {"type": MessageStreamDefinition, "subtype": None},
    }
    _formats_map = {}
    _validations_map = {
        "request_id": {"required": True, "minLength": 1, "pattern": "^[\w ,.\-_]*$",},
        "definition": {"required": True,},
    }

    def __init__(
        self, request_id: str = None, definition: MessageStreamDefinition = None
    ):
        pass
        self.__request_id = request_id
        self.__definition = definition

    def _get_request_id(self):
        return self.__request_id

    def _set_request_id(self, value):
        if not isinstance(value, str):
            raise TypeError("request_id must be str")

        self.__request_id = value

    request_id = property(_get_request_id, _set_request_id)

    def _get_definition(self):
        return self.__definition

    def _set_definition(self, value):
        if not isinstance(value, MessageStreamDefinition):
            raise TypeError("definition must be MessageStreamDefinition")

        self.__definition = value

    definition = property(_get_definition, _set_definition)

    @staticmethod
    def from_dict(d):
        v = {}
        if "requestId" in d:
            v["request_id"] = (
                str.from_dict(d["requestId"])
                if hasattr(str, "from_dict")
                else d["requestId"]
            )
        if "definition" in d:
            v["definition"] = (
                MessageStreamDefinition.from_dict(d["definition"])
                if hasattr(MessageStreamDefinition, "from_dict")
                else d["definition"]
            )
        return CreateMessageStreamRequest(**v)

    def as_dict(self):
        d = {}
        if self.__request_id is not None:
            d["requestId"] = (
                self.__request_id.as_dict()
                if hasattr(self.__request_id, "as_dict")
                else self.__request_id
            )
        if self.__definition is not None:
            d["definition"] = (
                self.__definition.as_dict()
                if hasattr(self.__definition, "as_dict")
                else self.__definition
            )
        return d

    def __repr__(self):
        return "<Class CreateMessageStreamRequest. request_id: {}, definition: {}>".format(
            limitedRepr(
                self.__request_id[:20]
                if isinstance(self.__request_id, bytes)
                else self.__request_id
            ),
            limitedRepr(
                self.__definition[:20]
                if isinstance(self.__definition, bytes)
                else self.__definition
            ),
        )


class CreateMessageStreamResponse:
    """
    Internal Only.
    """

    __slots__ = [
        "__request_id",
        "__status",
        "__error_message",
    ]

    _types_map = {
        "request_id": {"type": str, "subtype": None},
        "status": {"type": ResponseStatusCode, "subtype": None},
        "error_message": {"type": str, "subtype": None},
    }
    _formats_map = {}
    _validations_map = {
        "request_id": {"required": True, "minLength": 1, "pattern": "^[\w ,.\-_]*$",},
        "status": {"required": True,},
        "error_message": {"required": False,},
    }

    def __init__(
        self,
        request_id: str = None,
        status: ResponseStatusCode = None,
        error_message: str = None,
    ):
        pass
        self.__request_id = request_id
        self.__status = status
        self.__error_message = error_message

    def _get_request_id(self):
        return self.__request_id

    def _set_request_id(self, value):
        if not isinstance(value, str):
            raise TypeError("request_id must be str")

        self.__request_id = value

    request_id = property(_get_request_id, _set_request_id)

    def _get_status(self):
        return self.__status

    def _set_status(self, value):
        if not isinstance(value, ResponseStatusCode):
            raise TypeError("status must be ResponseStatusCode")

        self.__status = value

    status = property(_get_status, _set_status)

    def _get_error_message(self):
        return self.__error_message

    def _set_error_message(self, value):
        if value is not None and not isinstance(value, str):
            raise TypeError("error_message must be str")

        self.__error_message = value

    error_message = property(_get_error_message, _set_error_message)

    @staticmethod
    def from_dict(d):
        v = {}
        if "requestId" in d:
            v["request_id"] = (
                str.from_dict(d["requestId"])
                if hasattr(str, "from_dict")
                else d["requestId"]
            )
        if "status" in d:
            v["status"] = (
                ResponseStatusCode.from_dict(d["status"])
                if hasattr(ResponseStatusCode, "from_dict")
                else d["status"]
            )
        if "errorMessage" in d:
            v["error_message"] = (
                str.from_dict(d["errorMessage"])
                if hasattr(str, "from_dict")
                else d["errorMessage"]
            )
        return CreateMessageStreamResponse(**v)

    def as_dict(self):
        d = {}
        if self.__request_id is not None:
            d["requestId"] = (
                self.__request_id.as_dict()
                if hasattr(self.__request_id, "as_dict")
                else self.__request_id
            )
        if self.__status is not None:
            d["status"] = (
                self.__status.as_dict()
                if hasattr(self.__status, "as_dict")
                else self.__status
            )
        if self.__error_message is not None:
            d["errorMessage"] = (
                self.__error_message.as_dict()
                if hasattr(self.__error_message, "as_dict")
                else self.__error_message
            )
        return d

    def __repr__(self):
        return "<Class CreateMessageStreamResponse. request_id: {}, status: {}, error_message: {}>".format(
            limitedRepr(
                self.__request_id[:20]
                if isinstance(self.__request_id, bytes)
                else self.__request_id
            ),
            limitedRepr(
                self.__status[:20]
                if isinstance(self.__status, bytes)
                else self.__status
            ),
            limitedRepr(
                self.__error_message[:20]
                if isinstance(self.__error_message, bytes)
                else self.__error_message
            ),
        )


class UpdateMessageStreamRequest:
    """
    (Internal Only) Request object for updating a message stream.
    """

    __slots__ = [
        "__request_id",
        "__definition",
    ]

    _types_map = {
        "request_id": {"type": str, "subtype": None},
        "definition": {"type": MessageStreamDefinition, "subtype": None},
    }
    _formats_map = {}
    _validations_map = {
        "request_id": {"required": True, "minLength": 1, "pattern": "^[\w ,.\-_]*$",},
        "definition": {"required": True,},
    }

    def __init__(
        self, request_id: str = None, definition: MessageStreamDefinition = None
    ):
        pass
        self.__request_id = request_id
        self.__definition = definition

    def _get_request_id(self):
        return self.__request_id

    def _set_request_id(self, value):
        if not isinstance(value, str):
            raise TypeError("request_id must be str")

        self.__request_id = value

    request_id = property(_get_request_id, _set_request_id)

    def _get_definition(self):
        return self.__definition

    def _set_definition(self, value):
        if not isinstance(value, MessageStreamDefinition):
            raise TypeError("definition must be MessageStreamDefinition")

        self.__definition = value

    definition = property(_get_definition, _set_definition)

    @staticmethod
    def from_dict(d):
        v = {}
        if "requestId" in d:
            v["request_id"] = (
                str.from_dict(d["requestId"])
                if hasattr(str, "from_dict")
                else d["requestId"]
            )
        if "definition" in d:
            v["definition"] = (
                MessageStreamDefinition.from_dict(d["definition"])
                if hasattr(MessageStreamDefinition, "from_dict")
                else d["definition"]
            )
        return UpdateMessageStreamRequest(**v)

    def as_dict(self):
        d = {}
        if self.__request_id is not None:
            d["requestId"] = (
                self.__request_id.as_dict()
                if hasattr(self.__request_id, "as_dict")
                else self.__request_id
            )
        if self.__definition is not None:
            d["definition"] = (
                self.__definition.as_dict()
                if hasattr(self.__definition, "as_dict")
                else self.__definition
            )
        return d

    def __repr__(self):
        return "<Class UpdateMessageStreamRequest. request_id: {}, definition: {}>".format(
            limitedRepr(
                self.__request_id[:20]
                if isinstance(self.__request_id, bytes)
                else self.__request_id
            ),
            limitedRepr(
                self.__definition[:20]
                if isinstance(self.__definition, bytes)
                else self.__definition
            ),
        )


class UpdateMessageStreamResponse:
    """
    (Internal Only) Response for UpdateMessageStreamRequest.
    """

    __slots__ = [
        "__request_id",
        "__status",
        "__error_message",
    ]

    _types_map = {
        "request_id": {"type": str, "subtype": None},
        "status": {"type": ResponseStatusCode, "subtype": None},
        "error_message": {"type": str, "subtype": None},
    }
    _formats_map = {}
    _validations_map = {
        "request_id": {"required": True, "minLength": 1, "pattern": "^[\w ,.\-_]*$",},
        "status": {"required": True,},
        "error_message": {"required": False,},
    }

    def __init__(
        self,
        request_id: str = None,
        status: ResponseStatusCode = None,
        error_message: str = None,
    ):
        pass
        self.__request_id = request_id
        self.__status = status
        self.__error_message = error_message

    def _get_request_id(self):
        return self.__request_id

    def _set_request_id(self, value):
        if not isinstance(value, str):
            raise TypeError("request_id must be str")

        self.__request_id = value

    request_id = property(_get_request_id, _set_request_id)

    def _get_status(self):
        return self.__status

    def _set_status(self, value):
        if not isinstance(value, ResponseStatusCode):
            raise TypeError("status must be ResponseStatusCode")

        self.__status = value

    status = property(_get_status, _set_status)

    def _get_error_message(self):
        return self.__error_message

    def _set_error_message(self, value):
        if value is not None and not isinstance(value, str):
            raise TypeError("error_message must be str")

        self.__error_message = value

    error_message = property(_get_error_message, _set_error_message)

    @staticmethod
    def from_dict(d):
        v = {}
        if "requestId" in d:
            v["request_id"] = (
                str.from_dict(d["requestId"])
                if hasattr(str, "from_dict")
                else d["requestId"]
            )
        if "status" in d:
            v["status"] = (
                ResponseStatusCode.from_dict(d["status"])
                if hasattr(ResponseStatusCode, "from_dict")
                else d["status"]
            )
        if "errorMessage" in d:
            v["error_message"] = (
                str.from_dict(d["errorMessage"])
                if hasattr(str, "from_dict")
                else d["errorMessage"]
            )
        return UpdateMessageStreamResponse(**v)

    def as_dict(self):
        d = {}
        if self.__request_id is not None:
            d["requestId"] = (
                self.__request_id.as_dict()
                if hasattr(self.__request_id, "as_dict")
                else self.__request_id
            )
        if self.__status is not None:
            d["status"] = (
                self.__status.as_dict()
                if hasattr(self.__status, "as_dict")
                else self.__status
            )
        if self.__error_message is not None:
            d["errorMessage"] = (
                self.__error_message.as_dict()
                if hasattr(self.__error_message, "as_dict")
                else self.__error_message
            )
        return d

    def __repr__(self):
        return "<Class UpdateMessageStreamResponse. request_id: {}, status: {}, error_message: {}>".format(
            limitedRepr(
                self.__request_id[:20]
                if isinstance(self.__request_id, bytes)
                else self.__request_id
            ),
            limitedRepr(
                self.__status[:20]
                if isinstance(self.__status, bytes)
                else self.__status
            ),
            limitedRepr(
                self.__error_message[:20]
                if isinstance(self.__error_message, bytes)
                else self.__error_message
            ),
        )


class DeleteMessageStreamRequest:
    """
    (Internal Only) Request object for deleting a message stream.
    """

    __slots__ = [
        "__request_id",
        "__name",
    ]

    _types_map = {
        "request_id": {"type": str, "subtype": None},
        "name": {"type": str, "subtype": None},
    }
    _formats_map = {}
    _validations_map = {
        "request_id": {"required": True, "minLength": 1, "pattern": "^[\w ,.\-_]*$",},
        "name": {
            "required": True,
            "minLength": 1,
            "maxLength": 255,
            "pattern": "^[\w ,.\-_]*$",
        },
    }

    def __init__(self, request_id: str = None, name: str = None):
        pass
        self.__request_id = request_id
        self.__name = name

    def _get_request_id(self):
        return self.__request_id

    def _set_request_id(self, value):
        if not isinstance(value, str):
            raise TypeError("request_id must be str")

        self.__request_id = value

    request_id = property(_get_request_id, _set_request_id)

    def _get_name(self):
        return self.__name

    def _set_name(self, value):
        if not isinstance(value, str):
            raise TypeError("name must be str")

        self.__name = value

    name = property(_get_name, _set_name)

    @staticmethod
    def from_dict(d):
        v = {}
        if "requestId" in d:
            v["request_id"] = (
                str.from_dict(d["requestId"])
                if hasattr(str, "from_dict")
                else d["requestId"]
            )
        if "name" in d:
            v["name"] = (
                str.from_dict(d["name"]) if hasattr(str, "from_dict") else d["name"]
            )
        return DeleteMessageStreamRequest(**v)

    def as_dict(self):
        d = {}
        if self.__request_id is not None:
            d["requestId"] = (
                self.__request_id.as_dict()
                if hasattr(self.__request_id, "as_dict")
                else self.__request_id
            )
        if self.__name is not None:
            d["name"] = (
                self.__name.as_dict()
                if hasattr(self.__name, "as_dict")
                else self.__name
            )
        return d

    def __repr__(self):
        return "<Class DeleteMessageStreamRequest. request_id: {}, name: {}>".format(
            limitedRepr(
                self.__request_id[:20]
                if isinstance(self.__request_id, bytes)
                else self.__request_id
            ),
            limitedRepr(
                self.__name[:20] if isinstance(self.__name, bytes) else self.__name
            ),
        )


class DeleteMessageStreamResponse:
    """
    Internal Only.
    """

    __slots__ = [
        "__request_id",
        "__status",
        "__error_message",
    ]

    _types_map = {
        "request_id": {"type": str, "subtype": None},
        "status": {"type": ResponseStatusCode, "subtype": None},
        "error_message": {"type": str, "subtype": None},
    }
    _formats_map = {}
    _validations_map = {
        "request_id": {"required": True, "minLength": 1, "pattern": "^[\w ,.\-_]*$",},
        "status": {"required": True,},
        "error_message": {"required": False,},
    }

    def __init__(
        self,
        request_id: str = None,
        status: ResponseStatusCode = None,
        error_message: str = None,
    ):
        pass
        self.__request_id = request_id
        self.__status = status
        self.__error_message = error_message

    def _get_request_id(self):
        return self.__request_id

    def _set_request_id(self, value):
        if not isinstance(value, str):
            raise TypeError("request_id must be str")

        self.__request_id = value

    request_id = property(_get_request_id, _set_request_id)

    def _get_status(self):
        return self.__status

    def _set_status(self, value):
        if not isinstance(value, ResponseStatusCode):
            raise TypeError("status must be ResponseStatusCode")

        self.__status = value

    status = property(_get_status, _set_status)

    def _get_error_message(self):
        return self.__error_message

    def _set_error_message(self, value):
        if value is not None and not isinstance(value, str):
            raise TypeError("error_message must be str")

        self.__error_message = value

    error_message = property(_get_error_message, _set_error_message)

    @staticmethod
    def from_dict(d):
        v = {}
        if "requestId" in d:
            v["request_id"] = (
                str.from_dict(d["requestId"])
                if hasattr(str, "from_dict")
                else d["requestId"]
            )
        if "status" in d:
            v["status"] = (
                ResponseStatusCode.from_dict(d["status"])
                if hasattr(ResponseStatusCode, "from_dict")
                else d["status"]
            )
        if "errorMessage" in d:
            v["error_message"] = (
                str.from_dict(d["errorMessage"])
                if hasattr(str, "from_dict")
                else d["errorMessage"]
            )
        return DeleteMessageStreamResponse(**v)

    def as_dict(self):
        d = {}
        if self.__request_id is not None:
            d["requestId"] = (
                self.__request_id.as_dict()
                if hasattr(self.__request_id, "as_dict")
                else self.__request_id
            )
        if self.__status is not None:
            d["status"] = (
                self.__status.as_dict()
                if hasattr(self.__status, "as_dict")
                else self.__status
            )
        if self.__error_message is not None:
            d["errorMessage"] = (
                self.__error_message.as_dict()
                if hasattr(self.__error_message, "as_dict")
                else self.__error_message
            )
        return d

    def __repr__(self):
        return "<Class DeleteMessageStreamResponse. request_id: {}, status: {}, error_message: {}>".format(
            limitedRepr(
                self.__request_id[:20]
                if isinstance(self.__request_id, bytes)
                else self.__request_id
            ),
            limitedRepr(
                self.__status[:20]
                if isinstance(self.__status, bytes)
                else self.__status
            ),
            limitedRepr(
                self.__error_message[:20]
                if isinstance(self.__error_message, bytes)
                else self.__error_message
            ),
        )


class DescribeMessageStreamRequest:
    """
    (Internal Only) Request object for describing a message stream.
    """

    __slots__ = [
        "__request_id",
        "__name",
    ]

    _types_map = {
        "request_id": {"type": str, "subtype": None},
        "name": {"type": str, "subtype": None},
    }
    _formats_map = {}
    _validations_map = {
        "request_id": {"required": True, "minLength": 1, "pattern": "^[\w ,.\-_]*$",},
        "name": {
            "required": True,
            "minLength": 1,
            "maxLength": 255,
            "pattern": "^[\w ,.\-_]*$",
        },
    }

    def __init__(self, request_id: str = None, name: str = None):
        pass
        self.__request_id = request_id
        self.__name = name

    def _get_request_id(self):
        return self.__request_id

    def _set_request_id(self, value):
        if not isinstance(value, str):
            raise TypeError("request_id must be str")

        self.__request_id = value

    request_id = property(_get_request_id, _set_request_id)

    def _get_name(self):
        return self.__name

    def _set_name(self, value):
        if not isinstance(value, str):
            raise TypeError("name must be str")

        self.__name = value

    name = property(_get_name, _set_name)

    @staticmethod
    def from_dict(d):
        v = {}
        if "requestId" in d:
            v["request_id"] = (
                str.from_dict(d["requestId"])
                if hasattr(str, "from_dict")
                else d["requestId"]
            )
        if "name" in d:
            v["name"] = (
                str.from_dict(d["name"]) if hasattr(str, "from_dict") else d["name"]
            )
        return DescribeMessageStreamRequest(**v)

    def as_dict(self):
        d = {}
        if self.__request_id is not None:
            d["requestId"] = (
                self.__request_id.as_dict()
                if hasattr(self.__request_id, "as_dict")
                else self.__request_id
            )
        if self.__name is not None:
            d["name"] = (
                self.__name.as_dict()
                if hasattr(self.__name, "as_dict")
                else self.__name
            )
        return d

    def __repr__(self):
        return "<Class DescribeMessageStreamRequest. request_id: {}, name: {}>".format(
            limitedRepr(
                self.__request_id[:20]
                if isinstance(self.__request_id, bytes)
                else self.__request_id
            ),
            limitedRepr(
                self.__name[:20] if isinstance(self.__name, bytes) else self.__name
            ),
        )


class MessageStreamInfo:
    """
    Message stream information including its definition, storage status and export status.
    """

    class storageStatus:
        """
            Stream status including oldest/newest sequence number and total bytes.
            """

        __slots__ = [
            "__oldest_sequence_number",
            "__newest_sequence_number",
            "__total_bytes",
        ]

        _types_map = {
            "oldest_sequence_number": {"type": int, "subtype": None},
            "newest_sequence_number": {"type": int, "subtype": None},
            "total_bytes": {"type": int, "subtype": None},
        }
        _formats_map = {}
        _validations_map = {
            "oldest_sequence_number": {"required": False,},
            "newest_sequence_number": {"required": False,},
            "total_bytes": {"required": False,},
        }

        def __init__(
            self,
            oldest_sequence_number: int = None,
            newest_sequence_number: int = None,
            total_bytes: int = None,
        ):
            """
                :param oldest_sequence_number: The sequence number of the first message which is still accessible in the stream.
                :param newest_sequence_number: The sequence number of the last appended message.
                :param total_bytes: The current total size of the stream in bytes.
                """
            pass
            self.__oldest_sequence_number = oldest_sequence_number
            self.__newest_sequence_number = newest_sequence_number
            self.__total_bytes = total_bytes

        def _get_oldest_sequence_number(self):
            return self.__oldest_sequence_number

        def _set_oldest_sequence_number(self, value):
            if value is not None and not isinstance(value, int):
                raise TypeError("oldest_sequence_number must be int")

            self.__oldest_sequence_number = value

        oldest_sequence_number = property(
            _get_oldest_sequence_number, _set_oldest_sequence_number
        )
        """
            The sequence number of the first message which is still accessible in the stream.
            """

        def _get_newest_sequence_number(self):
            return self.__newest_sequence_number

        def _set_newest_sequence_number(self, value):
            if value is not None and not isinstance(value, int):
                raise TypeError("newest_sequence_number must be int")

            self.__newest_sequence_number = value

        newest_sequence_number = property(
            _get_newest_sequence_number, _set_newest_sequence_number
        )
        """
            The sequence number of the last appended message.
            """

        def _get_total_bytes(self):
            return self.__total_bytes

        def _set_total_bytes(self, value):
            if value is not None and not isinstance(value, int):
                raise TypeError("total_bytes must be int")

            self.__total_bytes = value

        total_bytes = property(_get_total_bytes, _set_total_bytes)
        """
            The current total size of the stream in bytes.
            """

        @staticmethod
        def from_dict(d):
            v = {}
            if "oldestSequenceNumber" in d:
                v["oldest_sequence_number"] = (
                    int.from_dict(d["oldestSequenceNumber"])
                    if hasattr(int, "from_dict")
                    else d["oldestSequenceNumber"]
                )
            if "newestSequenceNumber" in d:
                v["newest_sequence_number"] = (
                    int.from_dict(d["newestSequenceNumber"])
                    if hasattr(int, "from_dict")
                    else d["newestSequenceNumber"]
                )
            if "totalBytes" in d:
                v["total_bytes"] = (
                    int.from_dict(d["totalBytes"])
                    if hasattr(int, "from_dict")
                    else d["totalBytes"]
                )
            return MessageStreamInfo.storageStatus(**v)

        def as_dict(self):
            d = {}
            if self.__oldest_sequence_number is not None:
                d["oldestSequenceNumber"] = (
                    self.__oldest_sequence_number.as_dict()
                    if hasattr(self.__oldest_sequence_number, "as_dict")
                    else self.__oldest_sequence_number
                )
            if self.__newest_sequence_number is not None:
                d["newestSequenceNumber"] = (
                    self.__newest_sequence_number.as_dict()
                    if hasattr(self.__newest_sequence_number, "as_dict")
                    else self.__newest_sequence_number
                )
            if self.__total_bytes is not None:
                d["totalBytes"] = (
                    self.__total_bytes.as_dict()
                    if hasattr(self.__total_bytes, "as_dict")
                    else self.__total_bytes
                )
            return d

        def __repr__(self):
            return "<Class storageStatus. oldest_sequence_number: {}, newest_sequence_number: {}, total_bytes: {}>".format(
                limitedRepr(
                    self.__oldest_sequence_number[:20]
                    if isinstance(self.__oldest_sequence_number, bytes)
                    else self.__oldest_sequence_number
                ),
                limitedRepr(
                    self.__newest_sequence_number[:20]
                    if isinstance(self.__newest_sequence_number, bytes)
                    else self.__newest_sequence_number
                ),
                limitedRepr(
                    self.__total_bytes[:20]
                    if isinstance(self.__total_bytes, bytes)
                    else self.__total_bytes
                ),
            )

    class exportStatuses:
        """
            Export status including the export identifier and the last exported sequence number for that export task.
            """

        __slots__ = [
            "__export_config_identifier",
            "__last_exported_sequence_number",
            "__last_export_time",
            "__error_message",
            "__exported_bytes_from_stream",
            "__exported_messages_count",
        ]

        _types_map = {
            "export_config_identifier": {"type": str, "subtype": None},
            "last_exported_sequence_number": {"type": int, "subtype": None},
            "last_export_time": {"type": int, "subtype": None},
            "error_message": {"type": str, "subtype": None},
            "exported_bytes_from_stream": {"type": int, "subtype": None},
            "exported_messages_count": {"type": int, "subtype": None},
        }
        _formats_map = {}
        _validations_map = {
            "export_config_identifier": {"required": False,},
            "last_exported_sequence_number": {"required": True,},
            "last_export_time": {"required": False,},
            "error_message": {"required": False,},
            "exported_bytes_from_stream": {"required": False,},
            "exported_messages_count": {"required": False,},
        }

        def __init__(
            self,
            export_config_identifier: str = None,
            last_exported_sequence_number: int = None,
            last_export_time: int = None,
            error_message: str = None,
            exported_bytes_from_stream: int = None,
            exported_messages_count: int = None,
        ):
            """
                :param export_config_identifier: The unique export identifier.
                :param last_exported_sequence_number: The sequence number of the last message which was successfully exported.
                :param last_export_time: The last time an export was attempted. Data is Unix epoch time in milliseconds.
                :param error_message: Error message from the last export attempt if it failed.
                :param exported_bytes_from_stream: Total bytes exported from the stream for this Export Config. It does not include the failed export attempts or messages which are skipped because of some non-retryable error.
                :param exported_messages_count: Total messages exported/processed.
                """
            pass
            self.__export_config_identifier = export_config_identifier
            self.__last_exported_sequence_number = last_exported_sequence_number
            self.__last_export_time = last_export_time
            self.__error_message = error_message
            self.__exported_bytes_from_stream = exported_bytes_from_stream
            self.__exported_messages_count = exported_messages_count

        def _get_export_config_identifier(self):
            return self.__export_config_identifier

        def _set_export_config_identifier(self, value):
            if value is not None and not isinstance(value, str):
                raise TypeError("export_config_identifier must be str")

            self.__export_config_identifier = value

        export_config_identifier = property(
            _get_export_config_identifier, _set_export_config_identifier
        )
        """
            The unique export identifier.
            """

        def _get_last_exported_sequence_number(self):
            return self.__last_exported_sequence_number

        def _set_last_exported_sequence_number(self, value):
            if not isinstance(value, int):
                raise TypeError("last_exported_sequence_number must be int")

            self.__last_exported_sequence_number = value

        last_exported_sequence_number = property(
            _get_last_exported_sequence_number, _set_last_exported_sequence_number
        )
        """
            The sequence number of the last message which was successfully exported.
            """

        def _get_last_export_time(self):
            return self.__last_export_time

        def _set_last_export_time(self, value):
            if value is not None and not isinstance(value, int):
                raise TypeError("last_export_time must be int")

            self.__last_export_time = value

        last_export_time = property(_get_last_export_time, _set_last_export_time)
        """
            The last time an export was attempted. Data is Unix epoch time in milliseconds.
            """

        def _get_error_message(self):
            return self.__error_message

        def _set_error_message(self, value):
            if value is not None and not isinstance(value, str):
                raise TypeError("error_message must be str")

            self.__error_message = value

        error_message = property(_get_error_message, _set_error_message)
        """
            Error message from the last export attempt if it failed.
            """

        def _get_exported_bytes_from_stream(self):
            return self.__exported_bytes_from_stream

        def _set_exported_bytes_from_stream(self, value):
            if value is not None and not isinstance(value, int):
                raise TypeError("exported_bytes_from_stream must be int")

            self.__exported_bytes_from_stream = value

        exported_bytes_from_stream = property(
            _get_exported_bytes_from_stream, _set_exported_bytes_from_stream
        )
        """
            Total bytes exported from the stream for this Export Config. It does not include the failed export attempts or messages which are skipped because of some non-retryable error.
            """

        def _get_exported_messages_count(self):
            return self.__exported_messages_count

        def _set_exported_messages_count(self, value):
            if value is not None and not isinstance(value, int):
                raise TypeError("exported_messages_count must be int")

            self.__exported_messages_count = value

        exported_messages_count = property(
            _get_exported_messages_count, _set_exported_messages_count
        )
        """
            Total messages exported/processed.
            """

        @staticmethod
        def from_dict(d):
            v = {}
            if "exportConfigIdentifier" in d:
                v["export_config_identifier"] = (
                    str.from_dict(d["exportConfigIdentifier"])
                    if hasattr(str, "from_dict")
                    else d["exportConfigIdentifier"]
                )
            if "lastExportedSequenceNumber" in d:
                v["last_exported_sequence_number"] = (
                    int.from_dict(d["lastExportedSequenceNumber"])
                    if hasattr(int, "from_dict")
                    else d["lastExportedSequenceNumber"]
                )
            if "lastExportTime" in d:
                v["last_export_time"] = (
                    int.from_dict(d["lastExportTime"])
                    if hasattr(int, "from_dict")
                    else d["lastExportTime"]
                )
            if "errorMessage" in d:
                v["error_message"] = (
                    str.from_dict(d["errorMessage"])
                    if hasattr(str, "from_dict")
                    else d["errorMessage"]
                )
            if "exportedBytesFromStream" in d:
                v["exported_bytes_from_stream"] = (
                    int.from_dict(d["exportedBytesFromStream"])
                    if hasattr(int, "from_dict")
                    else d["exportedBytesFromStream"]
                )
            if "exportedMessagesCount" in d:
                v["exported_messages_count"] = (
                    int.from_dict(d["exportedMessagesCount"])
                    if hasattr(int, "from_dict")
                    else d["exportedMessagesCount"]
                )
            return MessageStreamInfo.exportStatuses(**v)

        def as_dict(self):
            d = {}
            if self.__export_config_identifier is not None:
                d["exportConfigIdentifier"] = (
                    self.__export_config_identifier.as_dict()
                    if hasattr(self.__export_config_identifier, "as_dict")
                    else self.__export_config_identifier
                )
            if self.__last_exported_sequence_number is not None:
                d["lastExportedSequenceNumber"] = (
                    self.__last_exported_sequence_number.as_dict()
                    if hasattr(self.__last_exported_sequence_number, "as_dict")
                    else self.__last_exported_sequence_number
                )
            if self.__last_export_time is not None:
                d["lastExportTime"] = (
                    self.__last_export_time.as_dict()
                    if hasattr(self.__last_export_time, "as_dict")
                    else self.__last_export_time
                )
            if self.__error_message is not None:
                d["errorMessage"] = (
                    self.__error_message.as_dict()
                    if hasattr(self.__error_message, "as_dict")
                    else self.__error_message
                )
            if self.__exported_bytes_from_stream is not None:
                d["exportedBytesFromStream"] = (
                    self.__exported_bytes_from_stream.as_dict()
                    if hasattr(self.__exported_bytes_from_stream, "as_dict")
                    else self.__exported_bytes_from_stream
                )
            if self.__exported_messages_count is not None:
                d["exportedMessagesCount"] = (
                    self.__exported_messages_count.as_dict()
                    if hasattr(self.__exported_messages_count, "as_dict")
                    else self.__exported_messages_count
                )
            return d

        def __repr__(self):
            return "<Class exportStatuses. export_config_identifier: {}, last_exported_sequence_number: {}, last_export_time: {}, error_message: {}, exported_bytes_from_stream: {}, exported_messages_count: {}>".format(
                limitedRepr(
                    self.__export_config_identifier[:20]
                    if isinstance(self.__export_config_identifier, bytes)
                    else self.__export_config_identifier
                ),
                limitedRepr(
                    self.__last_exported_sequence_number[:20]
                    if isinstance(self.__last_exported_sequence_number, bytes)
                    else self.__last_exported_sequence_number
                ),
                limitedRepr(
                    self.__last_export_time[:20]
                    if isinstance(self.__last_export_time, bytes)
                    else self.__last_export_time
                ),
                limitedRepr(
                    self.__error_message[:20]
                    if isinstance(self.__error_message, bytes)
                    else self.__error_message
                ),
                limitedRepr(
                    self.__exported_bytes_from_stream[:20]
                    if isinstance(self.__exported_bytes_from_stream, bytes)
                    else self.__exported_bytes_from_stream
                ),
                limitedRepr(
                    self.__exported_messages_count[:20]
                    if isinstance(self.__exported_messages_count, bytes)
                    else self.__exported_messages_count
                ),
            )

    __slots__ = [
        "__definition",
        "__storage_status",
        "__export_statuses",
    ]

    _types_map = {
        "definition": {"type": MessageStreamDefinition, "subtype": None},
        "storage_status": {"type": storageStatus, "subtype": None},
        "export_statuses": {"type": list, "subtype": exportStatuses},
    }
    _formats_map = {}
    _validations_map = {
        "definition": {"required": True,},
        "storage_status": {"required": True,},
        "export_statuses": {"required": False,},
    }

    def __init__(
        self,
        definition: MessageStreamDefinition = None,
        storage_status: storageStatus = None,
        export_statuses: List[exportStatuses] = None,
    ):
        """
        :param storage_status: Stream status including oldest/newest sequence number and total bytes.
        """
        pass
        self.__definition = definition
        self.__storage_status = storage_status
        self.__export_statuses = export_statuses

    def _get_definition(self):
        return self.__definition

    def _set_definition(self, value):
        if not isinstance(value, MessageStreamDefinition):
            raise TypeError("definition must be MessageStreamDefinition")

        self.__definition = value

    definition = property(_get_definition, _set_definition)

    def _get_storage_status(self):
        return self.__storage_status

    def _set_storage_status(self, value):
        if not isinstance(value, MessageStreamInfo.storageStatus):
            raise TypeError("storage_status must be MessageStreamInfo.storageStatus")

        self.__storage_status = value

    storage_status = property(_get_storage_status, _set_storage_status)
    """
    Stream status including oldest/newest sequence number and total bytes.
    """

    def _get_export_statuses(self):
        return self.__export_statuses

    def _set_export_statuses(self, value):
        if value is not None and not isinstance(value, list):
            raise TypeError("export_statuses must be list")
        if value is not None and not all(
            isinstance(i, MessageStreamInfo.exportStatuses) for i in value
        ):
            raise TypeError(
                "export_statuses list values must be MessageStreamInfo.exportStatuses"
            )

        self.__export_statuses = value

    export_statuses = property(_get_export_statuses, _set_export_statuses)

    @staticmethod
    def from_dict(d):
        v = {}
        if "definition" in d:
            v["definition"] = (
                MessageStreamDefinition.from_dict(d["definition"])
                if hasattr(MessageStreamDefinition, "from_dict")
                else d["definition"]
            )
        if "storageStatus" in d:
            v["storage_status"] = (
                MessageStreamInfo.storageStatus.from_dict(d["storageStatus"])
                if hasattr(MessageStreamInfo.storageStatus, "from_dict")
                else d["storageStatus"]
            )
        if "exportStatuses" in d:
            v["export_statuses"] = [
                MessageStreamInfo.exportStatuses.from_dict(p)
                if hasattr(MessageStreamInfo.exportStatuses, "from_dict")
                else p
                for p in d["exportStatuses"]
            ]
        return MessageStreamInfo(**v)

    def as_dict(self):
        d = {}
        if self.__definition is not None:
            d["definition"] = (
                self.__definition.as_dict()
                if hasattr(self.__definition, "as_dict")
                else self.__definition
            )
        if self.__storage_status is not None:
            d["storageStatus"] = (
                self.__storage_status.as_dict()
                if hasattr(self.__storage_status, "as_dict")
                else self.__storage_status
            )
        if self.__export_statuses is not None:
            d["exportStatuses"] = [
                p.as_dict() if hasattr(p, "as_dict") else p
                for p in self.__export_statuses
            ]
        return d

    def __repr__(self):
        return "<Class MessageStreamInfo. definition: {}, storage_status: {}, export_statuses: {}>".format(
            limitedRepr(
                self.__definition[:20]
                if isinstance(self.__definition, bytes)
                else self.__definition
            ),
            limitedRepr(
                self.__storage_status[:20]
                if isinstance(self.__storage_status, bytes)
                else self.__storage_status
            ),
            limitedRepr(
                self.__export_statuses[:20]
                if isinstance(self.__export_statuses, bytes)
                else self.__export_statuses
            ),
        )


class DescribeMessageStreamResponse:
    """
    (Internal Only) Response object for describing a message stream.
    """

    __slots__ = [
        "__request_id",
        "__status",
        "__error_message",
        "__message_stream_info",
    ]

    _types_map = {
        "request_id": {"type": str, "subtype": None},
        "status": {"type": ResponseStatusCode, "subtype": None},
        "error_message": {"type": str, "subtype": None},
        "message_stream_info": {"type": MessageStreamInfo, "subtype": None},
    }
    _formats_map = {}
    _validations_map = {
        "request_id": {"required": True, "minLength": 1, "pattern": "^[\w ,.\-_]*$",},
        "status": {"required": True,},
        "error_message": {"required": False,},
        "message_stream_info": {"required": False,},
    }

    def __init__(
        self,
        request_id: str = None,
        status: ResponseStatusCode = None,
        error_message: str = None,
        message_stream_info: MessageStreamInfo = None,
    ):
        pass
        self.__request_id = request_id
        self.__status = status
        self.__error_message = error_message
        self.__message_stream_info = message_stream_info

    def _get_request_id(self):
        return self.__request_id

    def _set_request_id(self, value):
        if not isinstance(value, str):
            raise TypeError("request_id must be str")

        self.__request_id = value

    request_id = property(_get_request_id, _set_request_id)

    def _get_status(self):
        return self.__status

    def _set_status(self, value):
        if not isinstance(value, ResponseStatusCode):
            raise TypeError("status must be ResponseStatusCode")

        self.__status = value

    status = property(_get_status, _set_status)

    def _get_error_message(self):
        return self.__error_message

    def _set_error_message(self, value):
        if value is not None and not isinstance(value, str):
            raise TypeError("error_message must be str")

        self.__error_message = value

    error_message = property(_get_error_message, _set_error_message)

    def _get_message_stream_info(self):
        return self.__message_stream_info

    def _set_message_stream_info(self, value):
        if value is not None and not isinstance(value, MessageStreamInfo):
            raise TypeError("message_stream_info must be MessageStreamInfo")

        self.__message_stream_info = value

    message_stream_info = property(_get_message_stream_info, _set_message_stream_info)

    @staticmethod
    def from_dict(d):
        v = {}
        if "requestId" in d:
            v["request_id"] = (
                str.from_dict(d["requestId"])
                if hasattr(str, "from_dict")
                else d["requestId"]
            )
        if "status" in d:
            v["status"] = (
                ResponseStatusCode.from_dict(d["status"])
                if hasattr(ResponseStatusCode, "from_dict")
                else d["status"]
            )
        if "errorMessage" in d:
            v["error_message"] = (
                str.from_dict(d["errorMessage"])
                if hasattr(str, "from_dict")
                else d["errorMessage"]
            )
        if "messageStreamInfo" in d:
            v["message_stream_info"] = (
                MessageStreamInfo.from_dict(d["messageStreamInfo"])
                if hasattr(MessageStreamInfo, "from_dict")
                else d["messageStreamInfo"]
            )
        return DescribeMessageStreamResponse(**v)

    def as_dict(self):
        d = {}
        if self.__request_id is not None:
            d["requestId"] = (
                self.__request_id.as_dict()
                if hasattr(self.__request_id, "as_dict")
                else self.__request_id
            )
        if self.__status is not None:
            d["status"] = (
                self.__status.as_dict()
                if hasattr(self.__status, "as_dict")
                else self.__status
            )
        if self.__error_message is not None:
            d["errorMessage"] = (
                self.__error_message.as_dict()
                if hasattr(self.__error_message, "as_dict")
                else self.__error_message
            )
        if self.__message_stream_info is not None:
            d["messageStreamInfo"] = (
                self.__message_stream_info.as_dict()
                if hasattr(self.__message_stream_info, "as_dict")
                else self.__message_stream_info
            )
        return d

    def __repr__(self):
        return "<Class DescribeMessageStreamResponse. request_id: {}, status: {}, error_message: {}, message_stream_info: {}>".format(
            limitedRepr(
                self.__request_id[:20]
                if isinstance(self.__request_id, bytes)
                else self.__request_id
            ),
            limitedRepr(
                self.__status[:20]
                if isinstance(self.__status, bytes)
                else self.__status
            ),
            limitedRepr(
                self.__error_message[:20]
                if isinstance(self.__error_message, bytes)
                else self.__error_message
            ),
            limitedRepr(
                self.__message_stream_info[:20]
                if isinstance(self.__message_stream_info, bytes)
                else self.__message_stream_info
            ),
        )


class AppendMessageRequest:
    """
    (Internal Only) Request object for appending to a message stream.
    """

    __slots__ = [
        "__request_id",
        "__name",
        "__payload",
    ]

    _types_map = {
        "request_id": {"type": str, "subtype": None},
        "name": {"type": str, "subtype": None},
        "payload": {"type": bytes, "subtype": None},
    }
    _formats_map = {}
    _validations_map = {
        "request_id": {"required": True, "minLength": 1, "pattern": "^[\w ,.\-_]*$",},
        "name": {
            "required": True,
            "minLength": 1,
            "maxLength": 255,
            "pattern": "^[\w ,.\-_]*$",
        },
        "payload": {"required": True, "minLength": 1,},
    }

    def __init__(self, request_id: str = None, name: str = None, payload: bytes = None):
        pass
        self.__request_id = request_id
        self.__name = name
        self.__payload = payload

    def _get_request_id(self):
        return self.__request_id

    def _set_request_id(self, value):
        if not isinstance(value, str):
            raise TypeError("request_id must be str")

        self.__request_id = value

    request_id = property(_get_request_id, _set_request_id)

    def _get_name(self):
        return self.__name

    def _set_name(self, value):
        if not isinstance(value, str):
            raise TypeError("name must be str")

        self.__name = value

    name = property(_get_name, _set_name)

    def _get_payload(self):
        return self.__payload

    def _set_payload(self, value):
        if not isinstance(value, bytes):
            raise TypeError("payload must be bytes")

        self.__payload = value

    payload = property(_get_payload, _set_payload)

    @staticmethod
    def from_dict(d):
        v = {}
        if "requestId" in d:
            v["request_id"] = (
                str.from_dict(d["requestId"])
                if hasattr(str, "from_dict")
                else d["requestId"]
            )
        if "name" in d:
            v["name"] = (
                str.from_dict(d["name"]) if hasattr(str, "from_dict") else d["name"]
            )
        if "payload" in d:
            v["payload"] = (
                bytes.from_dict(d["payload"])
                if hasattr(bytes, "from_dict")
                else d["payload"]
            )
        return AppendMessageRequest(**v)

    def as_dict(self):
        d = {}
        if self.__request_id is not None:
            d["requestId"] = (
                self.__request_id.as_dict()
                if hasattr(self.__request_id, "as_dict")
                else self.__request_id
            )
        if self.__name is not None:
            d["name"] = (
                self.__name.as_dict()
                if hasattr(self.__name, "as_dict")
                else self.__name
            )
        if self.__payload is not None:
            d["payload"] = (
                self.__payload.as_dict()
                if hasattr(self.__payload, "as_dict")
                else self.__payload
            )
        return d

    def __repr__(self):
        return "<Class AppendMessageRequest. request_id: {}, name: {}, payload: {}>".format(
            limitedRepr(
                self.__request_id[:20]
                if isinstance(self.__request_id, bytes)
                else self.__request_id
            ),
            limitedRepr(
                self.__name[:20] if isinstance(self.__name, bytes) else self.__name
            ),
            limitedRepr(
                self.__payload[:20]
                if isinstance(self.__payload, bytes)
                else self.__payload
            ),
        )


class AppendMessageResponse:
    """
    Internal Only.
    """

    __slots__ = [
        "__request_id",
        "__status",
        "__error_message",
        "__sequence_number",
    ]

    _types_map = {
        "request_id": {"type": str, "subtype": None},
        "status": {"type": ResponseStatusCode, "subtype": None},
        "error_message": {"type": str, "subtype": None},
        "sequence_number": {"type": int, "subtype": None},
    }
    _formats_map = {}
    _validations_map = {
        "request_id": {"required": True, "minLength": 1, "pattern": "^[\w ,.\-_]*$",},
        "status": {"required": True,},
        "error_message": {"required": False,},
        "sequence_number": {"required": False,},
    }

    def __init__(
        self,
        request_id: str = None,
        status: ResponseStatusCode = None,
        error_message: str = None,
        sequence_number: int = None,
    ):
        pass
        self.__request_id = request_id
        self.__status = status
        self.__error_message = error_message
        self.__sequence_number = sequence_number

    def _get_request_id(self):
        return self.__request_id

    def _set_request_id(self, value):
        if not isinstance(value, str):
            raise TypeError("request_id must be str")

        self.__request_id = value

    request_id = property(_get_request_id, _set_request_id)

    def _get_status(self):
        return self.__status

    def _set_status(self, value):
        if not isinstance(value, ResponseStatusCode):
            raise TypeError("status must be ResponseStatusCode")

        self.__status = value

    status = property(_get_status, _set_status)

    def _get_error_message(self):
        return self.__error_message

    def _set_error_message(self, value):
        if value is not None and not isinstance(value, str):
            raise TypeError("error_message must be str")

        self.__error_message = value

    error_message = property(_get_error_message, _set_error_message)

    def _get_sequence_number(self):
        return self.__sequence_number

    def _set_sequence_number(self, value):
        if value is not None and not isinstance(value, int):
            raise TypeError("sequence_number must be int")

        self.__sequence_number = value

    sequence_number = property(_get_sequence_number, _set_sequence_number)

    @staticmethod
    def from_dict(d):
        v = {}
        if "requestId" in d:
            v["request_id"] = (
                str.from_dict(d["requestId"])
                if hasattr(str, "from_dict")
                else d["requestId"]
            )
        if "status" in d:
            v["status"] = (
                ResponseStatusCode.from_dict(d["status"])
                if hasattr(ResponseStatusCode, "from_dict")
                else d["status"]
            )
        if "errorMessage" in d:
            v["error_message"] = (
                str.from_dict(d["errorMessage"])
                if hasattr(str, "from_dict")
                else d["errorMessage"]
            )
        if "sequenceNumber" in d:
            v["sequence_number"] = (
                int.from_dict(d["sequenceNumber"])
                if hasattr(int, "from_dict")
                else d["sequenceNumber"]
            )
        return AppendMessageResponse(**v)

    def as_dict(self):
        d = {}
        if self.__request_id is not None:
            d["requestId"] = (
                self.__request_id.as_dict()
                if hasattr(self.__request_id, "as_dict")
                else self.__request_id
            )
        if self.__status is not None:
            d["status"] = (
                self.__status.as_dict()
                if hasattr(self.__status, "as_dict")
                else self.__status
            )
        if self.__error_message is not None:
            d["errorMessage"] = (
                self.__error_message.as_dict()
                if hasattr(self.__error_message, "as_dict")
                else self.__error_message
            )
        if self.__sequence_number is not None:
            d["sequenceNumber"] = (
                self.__sequence_number.as_dict()
                if hasattr(self.__sequence_number, "as_dict")
                else self.__sequence_number
            )
        return d

    def __repr__(self):
        return "<Class AppendMessageResponse. request_id: {}, status: {}, error_message: {}, sequence_number: {}>".format(
            limitedRepr(
                self.__request_id[:20]
                if isinstance(self.__request_id, bytes)
                else self.__request_id
            ),
            limitedRepr(
                self.__status[:20]
                if isinstance(self.__status, bytes)
                else self.__status
            ),
            limitedRepr(
                self.__error_message[:20]
                if isinstance(self.__error_message, bytes)
                else self.__error_message
            ),
            limitedRepr(
                self.__sequence_number[:20]
                if isinstance(self.__sequence_number, bytes)
                else self.__sequence_number
            ),
        )


class ReadMessagesOptions:
    """
    Options for the ReadMessages API. All fields are optional.
    """

    __slots__ = [
        "__desired_start_sequence_number",
        "__min_message_count",
        "__max_message_count",
        "__read_timeout_millis",
    ]

    _types_map = {
        "desired_start_sequence_number": {"type": int, "subtype": None},
        "min_message_count": {"type": int, "subtype": None},
        "max_message_count": {"type": int, "subtype": None},
        "read_timeout_millis": {"type": int, "subtype": None},
    }
    _formats_map = {}
    _validations_map = {
        "desired_start_sequence_number": {
            "required": False,
            "maximum": 9223372036854775807,
            "minimum": 0,
        },
        "min_message_count": {"required": False, "maximum": 2147483647, "minimum": 1,},
        "max_message_count": {"required": False, "maximum": 2147483647, "minimum": 1,},
        "read_timeout_millis": {
            "required": False,
            "maximum": 9223372036854,
            "minimum": 0,
        },
    }

    def __init__(
        self,
        desired_start_sequence_number: int = None,
        min_message_count: int = 1,
        max_message_count: int = None,
        read_timeout_millis: int = 0,
    ):
        """
        :param desired_start_sequence_number: The desired beginning sequence number to start reading from. If the desired sequence number is less than the current minimum of the stream, then it will instead start reading from the current minimum.
        :param min_message_count: The minimum number of messages that will be returned. If not enough messages are available for reading, then NotEnoughMessages exception will be thrown.
            The minimum values is 1 and the maximum value is 2147483647.
        :param max_message_count: The maximum number of messages that will be returned.
            The minimum values is the value of the minimum message count and the maximum value is 2147483647.
        :param read_timeout_millis: The time to wait for messages in milliseconds. Default is 0, meaning that the server will not wait for messages.
            If it can fulfill the minimum messages it will return them, but otherwise NotEnoughMessages exception will be thrown.
            If the timeout is greater than zero, then the server will wait up to that time for more messages to be appended to the stream, waiting until the minimum number of messages is reached.
            The maximum value is the value of the client timeout.
        """
        pass
        self.__desired_start_sequence_number = desired_start_sequence_number
        self.__min_message_count = min_message_count
        self.__max_message_count = max_message_count
        self.__read_timeout_millis = read_timeout_millis

    def _get_desired_start_sequence_number(self):
        return self.__desired_start_sequence_number

    def _set_desired_start_sequence_number(self, value):
        if value is not None and not isinstance(value, int):
            raise TypeError("desired_start_sequence_number must be int")

        self.__desired_start_sequence_number = value

    desired_start_sequence_number = property(
        _get_desired_start_sequence_number, _set_desired_start_sequence_number
    )
    """
    The desired beginning sequence number to start reading from. If the desired sequence number is less than the current minimum of the stream, then it will instead start reading from the current minimum.
    """

    def _get_min_message_count(self):
        return self.__min_message_count

    def _set_min_message_count(self, value):
        if value is not None and not isinstance(value, int):
            raise TypeError("min_message_count must be int")

        self.__min_message_count = value

    min_message_count = property(_get_min_message_count, _set_min_message_count)
    """
    The minimum number of messages that will be returned. If not enough messages are available for reading, then NotEnoughMessages exception will be thrown.
    The minimum values is 1 and the maximum value is 2147483647.
    """

    def _get_max_message_count(self):
        return self.__max_message_count

    def _set_max_message_count(self, value):
        if value is not None and not isinstance(value, int):
            raise TypeError("max_message_count must be int")

        self.__max_message_count = value

    max_message_count = property(_get_max_message_count, _set_max_message_count)
    """
    The maximum number of messages that will be returned.
    The minimum values is the value of the minimum message count and the maximum value is 2147483647.
    """

    def _get_read_timeout_millis(self):
        return self.__read_timeout_millis

    def _set_read_timeout_millis(self, value):
        if value is not None and not isinstance(value, int):
            raise TypeError("read_timeout_millis must be int")

        self.__read_timeout_millis = value

    read_timeout_millis = property(_get_read_timeout_millis, _set_read_timeout_millis)
    """
    The time to wait for messages in milliseconds. Default is 0, meaning that the server will not wait for messages.
    If it can fulfill the minimum messages it will return them, but otherwise NotEnoughMessages exception will be thrown.
    If the timeout is greater than zero, then the server will wait up to that time for more messages to be appended to the stream, waiting until the minimum number of messages is reached.
    The maximum value is the value of the client timeout.
    """

    @staticmethod
    def from_dict(d):
        v = {}
        if "desiredStartSequenceNumber" in d:
            v["desired_start_sequence_number"] = (
                int.from_dict(d["desiredStartSequenceNumber"])
                if hasattr(int, "from_dict")
                else d["desiredStartSequenceNumber"]
            )
        if "minMessageCount" in d:
            v["min_message_count"] = (
                int.from_dict(d["minMessageCount"])
                if hasattr(int, "from_dict")
                else d["minMessageCount"]
            )
        if "maxMessageCount" in d:
            v["max_message_count"] = (
                int.from_dict(d["maxMessageCount"])
                if hasattr(int, "from_dict")
                else d["maxMessageCount"]
            )
        if "readTimeoutMillis" in d:
            v["read_timeout_millis"] = (
                int.from_dict(d["readTimeoutMillis"])
                if hasattr(int, "from_dict")
                else d["readTimeoutMillis"]
            )
        return ReadMessagesOptions(**v)

    def as_dict(self):
        d = {}
        if self.__desired_start_sequence_number is not None:
            d["desiredStartSequenceNumber"] = (
                self.__desired_start_sequence_number.as_dict()
                if hasattr(self.__desired_start_sequence_number, "as_dict")
                else self.__desired_start_sequence_number
            )
        if self.__min_message_count is not None:
            d["minMessageCount"] = (
                self.__min_message_count.as_dict()
                if hasattr(self.__min_message_count, "as_dict")
                else self.__min_message_count
            )
        if self.__max_message_count is not None:
            d["maxMessageCount"] = (
                self.__max_message_count.as_dict()
                if hasattr(self.__max_message_count, "as_dict")
                else self.__max_message_count
            )
        if self.__read_timeout_millis is not None:
            d["readTimeoutMillis"] = (
                self.__read_timeout_millis.as_dict()
                if hasattr(self.__read_timeout_millis, "as_dict")
                else self.__read_timeout_millis
            )
        return d

    def __repr__(self):
        return "<Class ReadMessagesOptions. desired_start_sequence_number: {}, min_message_count: {}, max_message_count: {}, read_timeout_millis: {}>".format(
            limitedRepr(
                self.__desired_start_sequence_number[:20]
                if isinstance(self.__desired_start_sequence_number, bytes)
                else self.__desired_start_sequence_number
            ),
            limitedRepr(
                self.__min_message_count[:20]
                if isinstance(self.__min_message_count, bytes)
                else self.__min_message_count
            ),
            limitedRepr(
                self.__max_message_count[:20]
                if isinstance(self.__max_message_count, bytes)
                else self.__max_message_count
            ),
            limitedRepr(
                self.__read_timeout_millis[:20]
                if isinstance(self.__read_timeout_millis, bytes)
                else self.__read_timeout_millis
            ),
        )


class ReadMessagesRequest:
    """
    (Internal Only) Request object for reading from a message stream. readMessagesOptions is optional.
    """

    __slots__ = [
        "__request_id",
        "__stream_name",
        "__read_messages_options",
    ]

    _types_map = {
        "request_id": {"type": str, "subtype": None},
        "stream_name": {"type": str, "subtype": None},
        "read_messages_options": {"type": ReadMessagesOptions, "subtype": None},
    }
    _formats_map = {}
    _validations_map = {
        "request_id": {"required": True, "minLength": 1, "pattern": "^[\w ,.\-_]*$",},
        "stream_name": {
            "required": True,
            "minLength": 1,
            "maxLength": 255,
            "pattern": "^[\w ,.\-_]*$",
        },
        "read_messages_options": {"required": False,},
    }

    def __init__(
        self,
        request_id: str = None,
        stream_name: str = None,
        read_messages_options: ReadMessagesOptions = None,
    ):
        pass
        self.__request_id = request_id
        self.__stream_name = stream_name
        self.__read_messages_options = read_messages_options

    def _get_request_id(self):
        return self.__request_id

    def _set_request_id(self, value):
        if not isinstance(value, str):
            raise TypeError("request_id must be str")

        self.__request_id = value

    request_id = property(_get_request_id, _set_request_id)

    def _get_stream_name(self):
        return self.__stream_name

    def _set_stream_name(self, value):
        if not isinstance(value, str):
            raise TypeError("stream_name must be str")

        self.__stream_name = value

    stream_name = property(_get_stream_name, _set_stream_name)

    def _get_read_messages_options(self):
        return self.__read_messages_options

    def _set_read_messages_options(self, value):
        if value is not None and not isinstance(value, ReadMessagesOptions):
            raise TypeError("read_messages_options must be ReadMessagesOptions")

        self.__read_messages_options = value

    read_messages_options = property(
        _get_read_messages_options, _set_read_messages_options
    )

    @staticmethod
    def from_dict(d):
        v = {}
        if "requestId" in d:
            v["request_id"] = (
                str.from_dict(d["requestId"])
                if hasattr(str, "from_dict")
                else d["requestId"]
            )
        if "streamName" in d:
            v["stream_name"] = (
                str.from_dict(d["streamName"])
                if hasattr(str, "from_dict")
                else d["streamName"]
            )
        if "readMessagesOptions" in d:
            v["read_messages_options"] = (
                ReadMessagesOptions.from_dict(d["readMessagesOptions"])
                if hasattr(ReadMessagesOptions, "from_dict")
                else d["readMessagesOptions"]
            )
        return ReadMessagesRequest(**v)

    def as_dict(self):
        d = {}
        if self.__request_id is not None:
            d["requestId"] = (
                self.__request_id.as_dict()
                if hasattr(self.__request_id, "as_dict")
                else self.__request_id
            )
        if self.__stream_name is not None:
            d["streamName"] = (
                self.__stream_name.as_dict()
                if hasattr(self.__stream_name, "as_dict")
                else self.__stream_name
            )
        if self.__read_messages_options is not None:
            d["readMessagesOptions"] = (
                self.__read_messages_options.as_dict()
                if hasattr(self.__read_messages_options, "as_dict")
                else self.__read_messages_options
            )
        return d

    def __repr__(self):
        return "<Class ReadMessagesRequest. request_id: {}, stream_name: {}, read_messages_options: {}>".format(
            limitedRepr(
                self.__request_id[:20]
                if isinstance(self.__request_id, bytes)
                else self.__request_id
            ),
            limitedRepr(
                self.__stream_name[:20]
                if isinstance(self.__stream_name, bytes)
                else self.__stream_name
            ),
            limitedRepr(
                self.__read_messages_options[:20]
                if isinstance(self.__read_messages_options, bytes)
                else self.__read_messages_options
            ),
        )


class Message:
    """
    Message object containing metadata and the user's payload.
    """

    __slots__ = [
        "__stream_name",
        "__sequence_number",
        "__ingest_time",
        "__payload",
    ]

    _types_map = {
        "stream_name": {"type": str, "subtype": None},
        "sequence_number": {"type": int, "subtype": None},
        "ingest_time": {"type": int, "subtype": None},
        "payload": {"type": bytes, "subtype": None},
    }
    _formats_map = {}
    _validations_map = {
        "stream_name": {"required": True,},
        "sequence_number": {"required": False,},
        "ingest_time": {"required": False,},
        "payload": {"required": True,},
    }

    def __init__(
        self,
        stream_name: str = None,
        sequence_number: int = None,
        ingest_time: int = None,
        payload: bytes = None,
    ):
        """
        :param stream_name: The name of the stream which this message is in.
        :param sequence_number: The sequence number of this message within the stream.
        :param ingest_time: The time that the message was ingested to Stream Manager. Data is Unix epoch time in milliseconds.
        :param payload: The binary message data.
        """
        pass
        self.__stream_name = stream_name
        self.__sequence_number = sequence_number
        self.__ingest_time = ingest_time
        self.__payload = payload

    def _get_stream_name(self):
        return self.__stream_name

    def _set_stream_name(self, value):
        if not isinstance(value, str):
            raise TypeError("stream_name must be str")

        self.__stream_name = value

    stream_name = property(_get_stream_name, _set_stream_name)
    """
    The name of the stream which this message is in.
    """

    def _get_sequence_number(self):
        return self.__sequence_number

    def _set_sequence_number(self, value):
        if value is not None and not isinstance(value, int):
            raise TypeError("sequence_number must be int")

        self.__sequence_number = value

    sequence_number = property(_get_sequence_number, _set_sequence_number)
    """
    The sequence number of this message within the stream.
    """

    def _get_ingest_time(self):
        return self.__ingest_time

    def _set_ingest_time(self, value):
        if value is not None and not isinstance(value, int):
            raise TypeError("ingest_time must be int")

        self.__ingest_time = value

    ingest_time = property(_get_ingest_time, _set_ingest_time)
    """
    The time that the message was ingested to Stream Manager. Data is Unix epoch time in milliseconds.
    """

    def _get_payload(self):
        return self.__payload

    def _set_payload(self, value):
        if not isinstance(value, bytes):
            raise TypeError("payload must be bytes")

        self.__payload = value

    payload = property(_get_payload, _set_payload)
    """
    The binary message data.
    """

    @staticmethod
    def from_dict(d):
        v = {}
        if "streamName" in d:
            v["stream_name"] = (
                str.from_dict(d["streamName"])
                if hasattr(str, "from_dict")
                else d["streamName"]
            )
        if "sequenceNumber" in d:
            v["sequence_number"] = (
                int.from_dict(d["sequenceNumber"])
                if hasattr(int, "from_dict")
                else d["sequenceNumber"]
            )
        if "ingestTime" in d:
            v["ingest_time"] = (
                int.from_dict(d["ingestTime"])
                if hasattr(int, "from_dict")
                else d["ingestTime"]
            )
        if "payload" in d:
            v["payload"] = (
                bytes.from_dict(d["payload"])
                if hasattr(bytes, "from_dict")
                else d["payload"]
            )
        return Message(**v)

    def as_dict(self):
        d = {}
        if self.__stream_name is not None:
            d["streamName"] = (
                self.__stream_name.as_dict()
                if hasattr(self.__stream_name, "as_dict")
                else self.__stream_name
            )
        if self.__sequence_number is not None:
            d["sequenceNumber"] = (
                self.__sequence_number.as_dict()
                if hasattr(self.__sequence_number, "as_dict")
                else self.__sequence_number
            )
        if self.__ingest_time is not None:
            d["ingestTime"] = (
                self.__ingest_time.as_dict()
                if hasattr(self.__ingest_time, "as_dict")
                else self.__ingest_time
            )
        if self.__payload is not None:
            d["payload"] = (
                self.__payload.as_dict()
                if hasattr(self.__payload, "as_dict")
                else self.__payload
            )
        return d

    def __repr__(self):
        return "<Class Message. stream_name: {}, sequence_number: {}, ingest_time: {}, payload: {}>".format(
            limitedRepr(
                self.__stream_name[:20]
                if isinstance(self.__stream_name, bytes)
                else self.__stream_name
            ),
            limitedRepr(
                self.__sequence_number[:20]
                if isinstance(self.__sequence_number, bytes)
                else self.__sequence_number
            ),
            limitedRepr(
                self.__ingest_time[:20]
                if isinstance(self.__ingest_time, bytes)
                else self.__ingest_time
            ),
            limitedRepr(
                self.__payload[:20]
                if isinstance(self.__payload, bytes)
                else self.__payload
            ),
        )


class ReadMessagesResponse:
    """
    Internal Only.
    """

    __slots__ = [
        "__request_id",
        "__messages",
        "__status",
        "__error_message",
    ]

    _types_map = {
        "request_id": {"type": str, "subtype": None},
        "messages": {"type": list, "subtype": Message},
        "status": {"type": ResponseStatusCode, "subtype": None},
        "error_message": {"type": str, "subtype": None},
    }
    _formats_map = {}
    _validations_map = {
        "request_id": {"required": False, "minLength": 1, "pattern": "^[\w ,.\-_]*$",},
        "messages": {"required": False,},
        "status": {"required": False,},
        "error_message": {"required": False,},
    }

    def __init__(
        self,
        request_id: str = None,
        messages: List[Message] = None,
        status: ResponseStatusCode = None,
        error_message: str = None,
    ):
        pass
        self.__request_id = request_id
        self.__messages = messages
        self.__status = status
        self.__error_message = error_message

    def _get_request_id(self):
        return self.__request_id

    def _set_request_id(self, value):
        if value is not None and not isinstance(value, str):
            raise TypeError("request_id must be str")

        self.__request_id = value

    request_id = property(_get_request_id, _set_request_id)

    def _get_messages(self):
        return self.__messages

    def _set_messages(self, value):
        if value is not None and not isinstance(value, list):
            raise TypeError("messages must be list")
        if value is not None and not all(isinstance(i, Message) for i in value):
            raise TypeError("messages list values must be Message")

        self.__messages = value

    messages = property(_get_messages, _set_messages)

    def _get_status(self):
        return self.__status

    def _set_status(self, value):
        if value is not None and not isinstance(value, ResponseStatusCode):
            raise TypeError("status must be ResponseStatusCode")

        self.__status = value

    status = property(_get_status, _set_status)

    def _get_error_message(self):
        return self.__error_message

    def _set_error_message(self, value):
        if value is not None and not isinstance(value, str):
            raise TypeError("error_message must be str")

        self.__error_message = value

    error_message = property(_get_error_message, _set_error_message)

    @staticmethod
    def from_dict(d):
        v = {}
        if "requestId" in d:
            v["request_id"] = (
                str.from_dict(d["requestId"])
                if hasattr(str, "from_dict")
                else d["requestId"]
            )
        if "messages" in d:
            v["messages"] = [
                Message.from_dict(p) if hasattr(Message, "from_dict") else p
                for p in d["messages"]
            ]
        if "status" in d:
            v["status"] = (
                ResponseStatusCode.from_dict(d["status"])
                if hasattr(ResponseStatusCode, "from_dict")
                else d["status"]
            )
        if "errorMessage" in d:
            v["error_message"] = (
                str.from_dict(d["errorMessage"])
                if hasattr(str, "from_dict")
                else d["errorMessage"]
            )
        return ReadMessagesResponse(**v)

    def as_dict(self):
        d = {}
        if self.__request_id is not None:
            d["requestId"] = (
                self.__request_id.as_dict()
                if hasattr(self.__request_id, "as_dict")
                else self.__request_id
            )
        if self.__messages is not None:
            d["messages"] = [
                p.as_dict() if hasattr(p, "as_dict") else p for p in self.__messages
            ]
        if self.__status is not None:
            d["status"] = (
                self.__status.as_dict()
                if hasattr(self.__status, "as_dict")
                else self.__status
            )
        if self.__error_message is not None:
            d["errorMessage"] = (
                self.__error_message.as_dict()
                if hasattr(self.__error_message, "as_dict")
                else self.__error_message
            )
        return d

    def __repr__(self):
        return "<Class ReadMessagesResponse. request_id: {}, messages: {}, status: {}, error_message: {}>".format(
            limitedRepr(
                self.__request_id[:20]
                if isinstance(self.__request_id, bytes)
                else self.__request_id
            ),
            limitedRepr(
                self.__messages[:20]
                if isinstance(self.__messages, bytes)
                else self.__messages
            ),
            limitedRepr(
                self.__status[:20]
                if isinstance(self.__status, bytes)
                else self.__status
            ),
            limitedRepr(
                self.__error_message[:20]
                if isinstance(self.__error_message, bytes)
                else self.__error_message
            ),
        )


class ListStreamsRequest:
    """
    (Internal Only) Request object to list all available streams. There are no options.
    """

    __slots__ = [
        "__request_id",
    ]

    _types_map = {
        "request_id": {"type": str, "subtype": None},
    }
    _formats_map = {}
    _validations_map = {
        "request_id": {"required": True, "minLength": 1, "pattern": "^[\w ,.\-_]*$",},
    }

    def __init__(self, request_id: str = None):
        pass
        self.__request_id = request_id

    def _get_request_id(self):
        return self.__request_id

    def _set_request_id(self, value):
        if not isinstance(value, str):
            raise TypeError("request_id must be str")

        self.__request_id = value

    request_id = property(_get_request_id, _set_request_id)

    @staticmethod
    def from_dict(d):
        v = {}
        if "requestId" in d:
            v["request_id"] = (
                str.from_dict(d["requestId"])
                if hasattr(str, "from_dict")
                else d["requestId"]
            )
        return ListStreamsRequest(**v)

    def as_dict(self):
        d = {}
        if self.__request_id is not None:
            d["requestId"] = (
                self.__request_id.as_dict()
                if hasattr(self.__request_id, "as_dict")
                else self.__request_id
            )
        return d

    def __repr__(self):
        return "<Class ListStreamsRequest. request_id: {}>".format(
            limitedRepr(
                self.__request_id[:20]
                if isinstance(self.__request_id, bytes)
                else self.__request_id
            )
        )


class ListStreamsResponse:
    """
    Internal Only.
    """

    __slots__ = [
        "__request_id",
        "__status",
        "__error_message",
        "__streams",
    ]

    _types_map = {
        "request_id": {"type": str, "subtype": None},
        "status": {"type": ResponseStatusCode, "subtype": None},
        "error_message": {"type": str, "subtype": None},
        "streams": {"type": list, "subtype": str},
    }
    _formats_map = {}
    _validations_map = {
        "request_id": {"required": True, "minLength": 1, "pattern": "^[\w ,.\-_]*$",},
        "status": {"required": True,},
        "error_message": {"required": False,},
        "streams": {"required": False,},
    }

    def __init__(
        self,
        request_id: str = None,
        status: ResponseStatusCode = None,
        error_message: str = None,
        streams: List[str] = None,
    ):
        pass
        self.__request_id = request_id
        self.__status = status
        self.__error_message = error_message
        self.__streams = streams

    def _get_request_id(self):
        return self.__request_id

    def _set_request_id(self, value):
        if not isinstance(value, str):
            raise TypeError("request_id must be str")

        self.__request_id = value

    request_id = property(_get_request_id, _set_request_id)

    def _get_status(self):
        return self.__status

    def _set_status(self, value):
        if not isinstance(value, ResponseStatusCode):
            raise TypeError("status must be ResponseStatusCode")

        self.__status = value

    status = property(_get_status, _set_status)

    def _get_error_message(self):
        return self.__error_message

    def _set_error_message(self, value):
        if value is not None and not isinstance(value, str):
            raise TypeError("error_message must be str")

        self.__error_message = value

    error_message = property(_get_error_message, _set_error_message)

    def _get_streams(self):
        return self.__streams

    def _set_streams(self, value):
        if value is not None and not isinstance(value, list):
            raise TypeError("streams must be list")
        if value is not None and not all(isinstance(i, str) for i in value):
            raise TypeError("streams list values must be str")

        self.__streams = value

    streams = property(_get_streams, _set_streams)

    @staticmethod
    def from_dict(d):
        v = {}
        if "requestId" in d:
            v["request_id"] = (
                str.from_dict(d["requestId"])
                if hasattr(str, "from_dict")
                else d["requestId"]
            )
        if "status" in d:
            v["status"] = (
                ResponseStatusCode.from_dict(d["status"])
                if hasattr(ResponseStatusCode, "from_dict")
                else d["status"]
            )
        if "errorMessage" in d:
            v["error_message"] = (
                str.from_dict(d["errorMessage"])
                if hasattr(str, "from_dict")
                else d["errorMessage"]
            )
        if "streams" in d:
            v["streams"] = [
                str.from_dict(p) if hasattr(str, "from_dict") else p
                for p in d["streams"]
            ]
        return ListStreamsResponse(**v)

    def as_dict(self):
        d = {}
        if self.__request_id is not None:
            d["requestId"] = (
                self.__request_id.as_dict()
                if hasattr(self.__request_id, "as_dict")
                else self.__request_id
            )
        if self.__status is not None:
            d["status"] = (
                self.__status.as_dict()
                if hasattr(self.__status, "as_dict")
                else self.__status
            )
        if self.__error_message is not None:
            d["errorMessage"] = (
                self.__error_message.as_dict()
                if hasattr(self.__error_message, "as_dict")
                else self.__error_message
            )
        if self.__streams is not None:
            d["streams"] = [
                p.as_dict() if hasattr(p, "as_dict") else p for p in self.__streams
            ]
        return d

    def __repr__(self):
        return "<Class ListStreamsResponse. request_id: {}, status: {}, error_message: {}, streams: {}>".format(
            limitedRepr(
                self.__request_id[:20]
                if isinstance(self.__request_id, bytes)
                else self.__request_id
            ),
            limitedRepr(
                self.__status[:20]
                if isinstance(self.__status, bytes)
                else self.__status
            ),
            limitedRepr(
                self.__error_message[:20]
                if isinstance(self.__error_message, bytes)
                else self.__error_message
            ),
            limitedRepr(
                self.__streams[:20]
                if isinstance(self.__streams, bytes)
                else self.__streams
            ),
        )


class TimeInNanos:
    """
    Contains a timestamp with optional nanosecond granularity.
    """

    __slots__ = [
        "__time_in_seconds",
        "__offset_in_nanos",
    ]

    _types_map = {
        "time_in_seconds": {"type": int, "subtype": None},
        "offset_in_nanos": {"type": int, "subtype": None},
    }
    _formats_map = {}
    _validations_map = {
        "time_in_seconds": {
            "required": True,
            "maximum": 31556889864403199,
            "minimum": 1,
        },
        "offset_in_nanos": {"required": False, "maximum": 999999999, "minimum": 0,},
    }

    def __init__(self, time_in_seconds: int = None, offset_in_nanos: int = None):
        """
        :param time_in_seconds: The timestamp date, in seconds, in the Unix epoch format. Fractional nanosecond data is provided by offsetInNanos.
        :param offset_in_nanos: The nanosecond offset from timeInSeconds.
        """
        pass
        self.__time_in_seconds = time_in_seconds
        self.__offset_in_nanos = offset_in_nanos

    def _get_time_in_seconds(self):
        return self.__time_in_seconds

    def _set_time_in_seconds(self, value):
        if not isinstance(value, int):
            raise TypeError("time_in_seconds must be int")

        self.__time_in_seconds = value

    time_in_seconds = property(_get_time_in_seconds, _set_time_in_seconds)
    """
    The timestamp date, in seconds, in the Unix epoch format. Fractional nanosecond data is provided by offsetInNanos.
    """

    def _get_offset_in_nanos(self):
        return self.__offset_in_nanos

    def _set_offset_in_nanos(self, value):
        if value is not None and not isinstance(value, int):
            raise TypeError("offset_in_nanos must be int")

        self.__offset_in_nanos = value

    offset_in_nanos = property(_get_offset_in_nanos, _set_offset_in_nanos)
    """
    The nanosecond offset from timeInSeconds.
    """

    @staticmethod
    def from_dict(d):
        v = {}
        if "timeInSeconds" in d:
            v["time_in_seconds"] = (
                int.from_dict(d["timeInSeconds"])
                if hasattr(int, "from_dict")
                else d["timeInSeconds"]
            )
        if "offsetInNanos" in d:
            v["offset_in_nanos"] = (
                int.from_dict(d["offsetInNanos"])
                if hasattr(int, "from_dict")
                else d["offsetInNanos"]
            )
        return TimeInNanos(**v)

    def as_dict(self):
        d = {}
        if self.__time_in_seconds is not None:
            d["timeInSeconds"] = (
                self.__time_in_seconds.as_dict()
                if hasattr(self.__time_in_seconds, "as_dict")
                else self.__time_in_seconds
            )
        if self.__offset_in_nanos is not None:
            d["offsetInNanos"] = (
                self.__offset_in_nanos.as_dict()
                if hasattr(self.__offset_in_nanos, "as_dict")
                else self.__offset_in_nanos
            )
        return d

    def __repr__(self):
        return "<Class TimeInNanos. time_in_seconds: {}, offset_in_nanos: {}>".format(
            limitedRepr(
                self.__time_in_seconds[:20]
                if isinstance(self.__time_in_seconds, bytes)
                else self.__time_in_seconds
            ),
            limitedRepr(
                self.__offset_in_nanos[:20]
                if isinstance(self.__offset_in_nanos, bytes)
                else self.__offset_in_nanos
            ),
        )


class Variant:
    """
    Contains an asset property value (of a single type only).
    """

    __slots__ = [
        "__string_value",
        "__integer_value",
        "__double_value",
        "__boolean_value",
    ]

    _types_map = {
        "string_value": {"type": str, "subtype": None},
        "integer_value": {"type": int, "subtype": None},
        "double_value": {"type": float, "subtype": None},
        "boolean_value": {"type": bool, "subtype": None},
    }
    _formats_map = {}
    _validations_map = {
        "string_value": {
            "required": False,
            "minLength": 1,
            "maxLength": 1024,
            "pattern": "[^\u0000-\u001F\u007F]+",
        },
        "integer_value": {"required": False, "maximum": 2147483647, "minimum": 0,},
        "double_value": {"required": False,},
        "boolean_value": {"required": False,},
    }

    def __init__(
        self,
        string_value: str = None,
        integer_value: int = None,
        double_value: float = None,
        boolean_value: bool = None,
    ):
        """
        :param string_value: Asset property data of type string (sequence of characters).
        :param integer_value: Asset property data of type integer (whole number).
        :param double_value: Asset property data of type double (floating point number).
        :param boolean_value: Asset property data of type Boolean (true or false).
        """
        pass
        self.__string_value = string_value
        self.__integer_value = integer_value
        self.__double_value = double_value
        self.__boolean_value = boolean_value

    def _get_string_value(self):
        return self.__string_value

    def _set_string_value(self, value):
        if value is not None and not isinstance(value, str):
            raise TypeError("string_value must be str")

        self.__string_value = value

    string_value = property(_get_string_value, _set_string_value)
    """
    Asset property data of type string (sequence of characters).
    """

    def _get_integer_value(self):
        return self.__integer_value

    def _set_integer_value(self, value):
        if value is not None and not isinstance(value, int):
            raise TypeError("integer_value must be int")

        self.__integer_value = value

    integer_value = property(_get_integer_value, _set_integer_value)
    """
    Asset property data of type integer (whole number).
    """

    def _get_double_value(self):
        return self.__double_value

    def _set_double_value(self, value):
        if value is not None and not isinstance(value, float):
            raise TypeError("double_value must be float")

        self.__double_value = value

    double_value = property(_get_double_value, _set_double_value)
    """
    Asset property data of type double (floating point number).
    """

    def _get_boolean_value(self):
        return self.__boolean_value

    def _set_boolean_value(self, value):
        if value is not None and not isinstance(value, bool):
            raise TypeError("boolean_value must be bool")

        self.__boolean_value = value

    boolean_value = property(_get_boolean_value, _set_boolean_value)
    """
    Asset property data of type Boolean (true or false).
    """

    @staticmethod
    def from_dict(d):
        v = {}
        if "stringValue" in d:
            v["string_value"] = (
                str.from_dict(d["stringValue"])
                if hasattr(str, "from_dict")
                else d["stringValue"]
            )
        if "integerValue" in d:
            v["integer_value"] = (
                int.from_dict(d["integerValue"])
                if hasattr(int, "from_dict")
                else d["integerValue"]
            )
        if "doubleValue" in d:
            v["double_value"] = (
                float.from_dict(d["doubleValue"])
                if hasattr(float, "from_dict")
                else d["doubleValue"]
            )
        if "booleanValue" in d:
            v["boolean_value"] = (
                bool.from_dict(d["booleanValue"])
                if hasattr(bool, "from_dict")
                else d["booleanValue"]
            )
        return Variant(**v)

    def as_dict(self):
        d = {}
        if self.__string_value is not None:
            d["stringValue"] = (
                self.__string_value.as_dict()
                if hasattr(self.__string_value, "as_dict")
                else self.__string_value
            )
        if self.__integer_value is not None:
            d["integerValue"] = (
                self.__integer_value.as_dict()
                if hasattr(self.__integer_value, "as_dict")
                else self.__integer_value
            )
        if self.__double_value is not None:
            d["doubleValue"] = (
                self.__double_value.as_dict()
                if hasattr(self.__double_value, "as_dict")
                else self.__double_value
            )
        if self.__boolean_value is not None:
            d["booleanValue"] = (
                self.__boolean_value.as_dict()
                if hasattr(self.__boolean_value, "as_dict")
                else self.__boolean_value
            )
        return d

    def __repr__(self):
        return "<Class Variant. string_value: {}, integer_value: {}, double_value: {}, boolean_value: {}>".format(
            limitedRepr(
                self.__string_value[:20]
                if isinstance(self.__string_value, bytes)
                else self.__string_value
            ),
            limitedRepr(
                self.__integer_value[:20]
                if isinstance(self.__integer_value, bytes)
                else self.__integer_value
            ),
            limitedRepr(
                self.__double_value[:20]
                if isinstance(self.__double_value, bytes)
                else self.__double_value
            ),
            limitedRepr(
                self.__boolean_value[:20]
                if isinstance(self.__boolean_value, bytes)
                else self.__boolean_value
            ),
        )


class Quality(enum.Enum):

    GOOD = "GOOD"
    BAD = "BAD"
    UNCERTAIN = "UNCERTAIN"

    @staticmethod
    def from_dict(d):
        return Quality(d)

    def as_dict(self):
        return self.value

    def __repr__(self):
        return "<Enum Quality. {}: {}>".format(
            limitedRepr(self.name), limitedRepr(self.value)
        )


class AssetPropertyValue:
    """
    Contains asset property value information.
    """

    __slots__ = [
        "__value",
        "__timestamp",
        "__quality",
    ]

    _types_map = {
        "value": {"type": Variant, "subtype": None},
        "timestamp": {"type": TimeInNanos, "subtype": None},
        "quality": {"type": Quality, "subtype": None},
    }
    _formats_map = {}
    _validations_map = {
        "value": {"required": True,},
        "timestamp": {"required": True,},
        "quality": {"required": False,},
    }

    def __init__(
        self,
        value: Variant = None,
        timestamp: TimeInNanos = None,
        quality: Quality = None,
    ):
        """
        :param value: The value of the asset property.
        :param timestamp: The timestamp of the asset property value.
        :param quality: The quality of the asset property value.
        """
        pass
        self.__value = value
        self.__timestamp = timestamp
        self.__quality = quality

    def _get_value(self):
        return self.__value

    def _set_value(self, value):
        if not isinstance(value, Variant):
            raise TypeError("value must be Variant")

        self.__value = value

    value = property(_get_value, _set_value)
    """
    The value of the asset property.
    """

    def _get_timestamp(self):
        return self.__timestamp

    def _set_timestamp(self, value):
        if not isinstance(value, TimeInNanos):
            raise TypeError("timestamp must be TimeInNanos")

        self.__timestamp = value

    timestamp = property(_get_timestamp, _set_timestamp)
    """
    The timestamp of the asset property value.
    """

    def _get_quality(self):
        return self.__quality

    def _set_quality(self, value):
        if value is not None and not isinstance(value, Quality):
            raise TypeError("quality must be Quality")

        self.__quality = value

    quality = property(_get_quality, _set_quality)
    """
    The quality of the asset property value.
    """

    @staticmethod
    def from_dict(d):
        v = {}
        if "value" in d:
            v["value"] = (
                Variant.from_dict(d["value"])
                if hasattr(Variant, "from_dict")
                else d["value"]
            )
        if "timestamp" in d:
            v["timestamp"] = (
                TimeInNanos.from_dict(d["timestamp"])
                if hasattr(TimeInNanos, "from_dict")
                else d["timestamp"]
            )
        if "quality" in d:
            v["quality"] = (
                Quality.from_dict(d["quality"])
                if hasattr(Quality, "from_dict")
                else d["quality"]
            )
        return AssetPropertyValue(**v)

    def as_dict(self):
        d = {}
        if self.__value is not None:
            d["value"] = (
                self.__value.as_dict()
                if hasattr(self.__value, "as_dict")
                else self.__value
            )
        if self.__timestamp is not None:
            d["timestamp"] = (
                self.__timestamp.as_dict()
                if hasattr(self.__timestamp, "as_dict")
                else self.__timestamp
            )
        if self.__quality is not None:
            d["quality"] = (
                self.__quality.as_dict()
                if hasattr(self.__quality, "as_dict")
                else self.__quality
            )
        return d

    def __repr__(self):
        return "<Class AssetPropertyValue. value: {}, timestamp: {}, quality: {}>".format(
            limitedRepr(
                self.__value[:20] if isinstance(self.__value, bytes) else self.__value
            ),
            limitedRepr(
                self.__timestamp[:20]
                if isinstance(self.__timestamp, bytes)
                else self.__timestamp
            ),
            limitedRepr(
                self.__quality[:20]
                if isinstance(self.__quality, bytes)
                else self.__quality
            ),
        )


class PutAssetPropertyValueEntry:
    """
    Contains a list of value updates for a IoTSiteWise asset property in the list of asset entries consumed by the BatchPutAssetPropertyValue API. See https://docs.aws.amazon.com/iot-sitewise/latest/APIReference/API_BatchPutAssetPropertyValue.html.
    """

    __slots__ = [
        "__entry_id",
        "__asset_id",
        "__property_id",
        "__property_alias",
        "__property_values",
    ]

    _types_map = {
        "entry_id": {"type": str, "subtype": None},
        "asset_id": {"type": str, "subtype": None},
        "property_id": {"type": str, "subtype": None},
        "property_alias": {"type": str, "subtype": None},
        "property_values": {"type": list, "subtype": AssetPropertyValue},
    }
    _formats_map = {}
    _validations_map = {
        "entry_id": {
            "required": True,
            "minLength": 1,
            "maxLength": 64,
            "pattern": "^[a-zA-Z0-9_-]+$",
        },
        "asset_id": {"required": False,},
        "property_id": {"required": False,},
        "property_alias": {
            "required": False,
            "minLength": 1,
            "maxLength": 2048,
            "pattern": "[^\u0000-\u001F\u007F]+",
        },
        "property_values": {"required": True, "maxItems": 10, "minItems": 1,},
    }

    def __init__(
        self,
        entry_id: str = None,
        asset_id: str = None,
        property_id: str = None,
        property_alias: str = None,
        property_values: List[AssetPropertyValue] = None,
    ):
        """
        :param entry_id: The user specified ID for the entry. You can use this ID to identify which entries failed.
        :param asset_id: The ID of the asset to update.
        :param property_id: The ID of the asset property for this entry.
        :param property_alias: The property alias that identifies the property, such as an OPC-UA server data stream path (for example, /company/windfarm/3/turbine/7/temperature). For more information, see https://docs.aws.amazon.com/iot-sitewise/latest/userguide/connect-data-streams.html.
        :param property_values: The list of property values to upload. You can specify up to 10 values.
        """
        pass
        self.__entry_id = entry_id
        self.__asset_id = asset_id
        self.__property_id = property_id
        self.__property_alias = property_alias
        self.__property_values = property_values

    def _get_entry_id(self):
        return self.__entry_id

    def _set_entry_id(self, value):
        if not isinstance(value, str):
            raise TypeError("entry_id must be str")

        self.__entry_id = value

    entry_id = property(_get_entry_id, _set_entry_id)
    """
    The user specified ID for the entry. You can use this ID to identify which entries failed.
    """

    def _get_asset_id(self):
        return self.__asset_id

    def _set_asset_id(self, value):
        if value is not None and not isinstance(value, str):
            raise TypeError("asset_id must be str")

        self.__asset_id = value

    asset_id = property(_get_asset_id, _set_asset_id)
    """
    The ID of the asset to update.
    """

    def _get_property_id(self):
        return self.__property_id

    def _set_property_id(self, value):
        if value is not None and not isinstance(value, str):
            raise TypeError("property_id must be str")

        self.__property_id = value

    property_id = property(_get_property_id, _set_property_id)
    """
    The ID of the asset property for this entry.
    """

    def _get_property_alias(self):
        return self.__property_alias

    def _set_property_alias(self, value):
        if value is not None and not isinstance(value, str):
            raise TypeError("property_alias must be str")

        self.__property_alias = value

    property_alias = property(_get_property_alias, _set_property_alias)
    """
    The property alias that identifies the property, such as an OPC-UA server data stream path (for example, /company/windfarm/3/turbine/7/temperature). For more information, see https://docs.aws.amazon.com/iot-sitewise/latest/userguide/connect-data-streams.html.
    """

    def _get_property_values(self):
        return self.__property_values

    def _set_property_values(self, value):
        if not isinstance(value, list):
            raise TypeError("property_values must be list")
        if not all(isinstance(i, AssetPropertyValue) for i in value):
            raise TypeError("property_values list values must be AssetPropertyValue")

        self.__property_values = value

    property_values = property(_get_property_values, _set_property_values)
    """
    The list of property values to upload. You can specify up to 10 values.
    """

    @staticmethod
    def from_dict(d):
        v = {}
        if "entryId" in d:
            v["entry_id"] = (
                str.from_dict(d["entryId"])
                if hasattr(str, "from_dict")
                else d["entryId"]
            )
        if "assetId" in d:
            v["asset_id"] = (
                str.from_dict(d["assetId"])
                if hasattr(str, "from_dict")
                else d["assetId"]
            )
        if "propertyId" in d:
            v["property_id"] = (
                str.from_dict(d["propertyId"])
                if hasattr(str, "from_dict")
                else d["propertyId"]
            )
        if "propertyAlias" in d:
            v["property_alias"] = (
                str.from_dict(d["propertyAlias"])
                if hasattr(str, "from_dict")
                else d["propertyAlias"]
            )
        if "propertyValues" in d:
            v["property_values"] = [
                AssetPropertyValue.from_dict(p)
                if hasattr(AssetPropertyValue, "from_dict")
                else p
                for p in d["propertyValues"]
            ]
        return PutAssetPropertyValueEntry(**v)

    def as_dict(self):
        d = {}
        if self.__entry_id is not None:
            d["entryId"] = (
                self.__entry_id.as_dict()
                if hasattr(self.__entry_id, "as_dict")
                else self.__entry_id
            )
        if self.__asset_id is not None:
            d["assetId"] = (
                self.__asset_id.as_dict()
                if hasattr(self.__asset_id, "as_dict")
                else self.__asset_id
            )
        if self.__property_id is not None:
            d["propertyId"] = (
                self.__property_id.as_dict()
                if hasattr(self.__property_id, "as_dict")
                else self.__property_id
            )
        if self.__property_alias is not None:
            d["propertyAlias"] = (
                self.__property_alias.as_dict()
                if hasattr(self.__property_alias, "as_dict")
                else self.__property_alias
            )
        if self.__property_values is not None:
            d["propertyValues"] = [
                p.as_dict() if hasattr(p, "as_dict") else p
                for p in self.__property_values
            ]
        return d

    def __repr__(self):
        return "<Class PutAssetPropertyValueEntry. entry_id: {}, asset_id: {}, property_id: {}, property_alias: {}, property_values: {}>".format(
            limitedRepr(
                self.__entry_id[:20]
                if isinstance(self.__entry_id, bytes)
                else self.__entry_id
            ),
            limitedRepr(
                self.__asset_id[:20]
                if isinstance(self.__asset_id, bytes)
                else self.__asset_id
            ),
            limitedRepr(
                self.__property_id[:20]
                if isinstance(self.__property_id, bytes)
                else self.__property_id
            ),
            limitedRepr(
                self.__property_alias[:20]
                if isinstance(self.__property_alias, bytes)
                else self.__property_alias
            ),
            limitedRepr(
                self.__property_values[:20]
                if isinstance(self.__property_values, bytes)
                else self.__property_values
            ),
        )
