import asyncio
import logging
import os
from threading import Thread
from typing import List, Optional

import cbor2

from .data import (
    AppendMessageRequest,
    AppendMessageResponse,
    ConnectRequest,
    ConnectResponse,
    CreateMessageStreamRequest,
    CreateMessageStreamResponse,
    DeleteMessageStreamRequest,
    DeleteMessageStreamResponse,
    DescribeMessageStreamRequest,
    DescribeMessageStreamResponse,
    ListStreamsRequest,
    ListStreamsResponse,
    Message,
    MessageFrame,
    MessageStreamDefinition,
    MessageStreamInfo,
    Operation,
    ReadMessagesOptions,
    ReadMessagesRequest,
    ReadMessagesResponse,
    ResponseStatusCode,
    UnknownOperationError,
    UpdateMessageStreamRequest,
    UpdateMessageStreamResponse,
    VersionInfo,
)
from .exceptions import ClientException, ConnectFailedException, StreamManagerException, ValidationException
from .utilinternal import UtilInternal


class StreamManagerClient:
    """
    Creates a client for the Greengrass StreamManager. All parameters are optional.

    :param host: The host which StreamManager server is running on. Default is localhost.
    :param port: The port which StreamManager server is running on. Default is found in environment variables.
    :param connect_timeout: The timeout in seconds for connecting to the server. Default is 3 seconds.
    :param request_timeout: The timeout in seconds for all operations. Default is 60 seconds.
    :param logger: A logger to use for client logging. Default is Python's builtin logger.

    :raises: :exc:`~.exceptions.StreamManagerException` and subtypes if authenticating to the server fails.
    :raises: :exc:`asyncio.TimeoutError` if the request times out.
    :raises: :exc:`ConnectionError` if the client is unable to connect to the server.
    """

    # Version of the Java SDK.
    # NOTE: When you bump this version,
    # consider adding the old version to olderSupportedProtocolVersions list (if you intend to support it)
    __SDK_VERSION = "1.1.0"

    # List of supported protocol protocol.
    # These are meant to be used for graceful degradation if the server does not support the current SDK version.
    __OLD_SUPPORTED_PROTOCOL_VERSIONS = ["1.0.0"]

    __CONNECT_VERSION = 1

    def __init__(
        self,
        host="127.0.0.1",
        port=None,
        connect_timeout=3,
        request_timeout=60,
        logger=logging.getLogger("StreamManagerClient"),
    ):
        self.host = host
        if port is None:
            port = int(os.getenv("STREAM_MANAGER_SERVER_PORT", 8088))
        self.port = port
        self.__requests = {}
        self.connect_timeout = connect_timeout
        self.request_timeout = request_timeout
        self.logger = logger
        self.auth_token = os.getenv("AWS_CONTAINER_AUTHORIZATION_TOKEN")

        # Python Logging doesn't have a TRACE level
        # so we will add our own at level 5. (Debug is level 10)
        if logger.level <= 5:
            logging.addLevelName(5, "TRACE")

        self.__loop = asyncio.new_event_loop()
        self.__closed = False
        self.__reader = None
        self.__writer = None

        # Defines a function to be run in a separate thread to run the event loop
        # this enables our synchronous interface without locks
        def run_event_loop(loop: asyncio.AbstractEventLoop):
            try:
                loop.run_forever()
            finally:
                loop.close()

        # Making the thread a daemon will kill the thread once the main thread closes
        self.__event_loop_thread = Thread(target=run_event_loop, args=(self.__loop,), daemon=True)
        self.__event_loop_thread.start()

        self.connected = False
        UtilInternal.sync(self.__connect(), loop=self.__loop)

    async def _close(self):
        if self.__writer is not None:
            self.__closed = True
            self.connected = False
            self.__reader = None
            # Drain any existing data waiting to be sent
            await self.__writer.drain()
            self.__writer.close()
            try:
                # Only added in Python 3.7, so try to call it, but otherwise just skip it
                await self.__writer.wait_closed()
            except AttributeError:
                pass
            self.__writer = None

    def __check_closed(self):
        if self.__closed:
            raise StreamManagerException("Client is closed. Create a new client first.")

    async def __connect(self):
        self.__check_closed()
        if self.connected:
            return
        try:
            self.logger.debug("Opening connection to %s:%d", self.host, self.port)
            future = asyncio.open_connection(self.host, self.port, loop=self.__loop)
            self.__reader, self.__writer = await asyncio.wait_for(
                future, timeout=self.connect_timeout, loop=self.__loop
            )

            await asyncio.wait_for(self.__connect_request_response(), timeout=self.request_timeout, loop=self.__loop)

            self.logger.debug("Socket connected successfully. Starting read loop.")
            self.connected = True
            self.__loop.create_task(self.__read_loop())
        except ConnectionError as e:
            self.logger.error("Connection error while connecting to server: %s", e)
            raise

    def __log_trace(self, *args, **kwargs):
        self.logger.log(5, *args, **kwargs)

    async def __read_message_frame(self):
        length_bytes = await self.__reader.read(n=4)
        if len(length_bytes) == 0:
            raise asyncio.IncompleteReadError(length_bytes, 4)

        length = UtilInternal.int_from_bytes(length_bytes)
        operation = UtilInternal.int_from_bytes(await self.__reader.read(n=1))

        # Read from the socket until we have read the full packet
        payload = bytearray()
        read_bytes = 1
        while read_bytes < length:
            next_payload = await self.__reader.read(n=length - read_bytes)
            if len(next_payload) == 0:
                raise asyncio.IncompleteReadError(next_payload, length - read_bytes)
            payload.extend(next_payload)
            read_bytes += len(next_payload)

        try:
            op = Operation.from_dict(operation)
        except ValueError:
            self.logger.error("Found unknown operation %d", operation)
            op = Operation.Unknown

        return MessageFrame(operation=op, payload=bytes(payload))

    async def __read_loop(self):
        # Continually try to read packets from the socket
        while not self.__closed:
            try:
                try:
                    self.__log_trace("Starting long poll read")
                    response = await self.__read_message_frame()
                    self.__log_trace("Got message frame from server: %s", response)
                except asyncio.IncompleteReadError:
                    if self.__closed:
                        return
                    self.logger.error("Unable to read from socket, likely socket is closed or server died")
                    self.connected = False
                    try:
                        await self.__connect()
                    except ConnectionError:
                        # Already logged in __connect, so just ignore it here
                        pass
                    except ConnectFailedException:
                        # Already logged in __connect_request_response, so just ignore it here
                        pass
                    return

                payload = cbor2.loads(response.payload)
                await self.__handle_read_response(payload, response)
            except Exception:
                self.logger.exception("Unhandled exception occurred")
                return

    async def __handle_read_response(self, payload, response):
        if response.operation == Operation.ReadMessagesResponse:
            response = ReadMessagesResponse.from_dict(payload)
            self.logger.debug("Received ReadMessagesResponse from server")
            await self.__requests[response.request_id].put(response)
        elif response.operation == Operation.CreateMessageStreamResponse:
            response = CreateMessageStreamResponse.from_dict(payload)
            self.logger.debug("Received CreateMessageStreamResponse from server: %s", response)
            await self.__requests[response.request_id].put(response)
        elif response.operation == Operation.DeleteMessageStreamResponse:
            response = DeleteMessageStreamResponse.from_dict(payload)
            self.logger.debug("Received DeleteMessageStreamResponse from server: %s", response)
            await self.__requests[response.request_id].put(response)
        elif response.operation == Operation.UpdateMessageStreamResponse:
            response = UpdateMessageStreamResponse.from_dict(payload)
            self.logger.debug("Received UpdateMessageStreamResponse from server: %s", response)
            await self.__requests[response.request_id].put(response)
        elif response.operation == Operation.AppendMessageResponse:
            response = AppendMessageResponse.from_dict(payload)
            self.logger.debug("Received AppendMessageResponse from server: %s", response)
            await self.__requests[response.request_id].put(response)
        elif response.operation == Operation.ListStreamsResponse:
            response = ListStreamsResponse.from_dict(payload)
            self.logger.debug("Received ListStreamsResponse from server: %s", response)
            await self.__requests[response.request_id].put(response)
        elif response.operation == Operation.DescribeMessageStreamResponse:
            response = DescribeMessageStreamResponse.from_dict(payload)
            self.logger.debug("Received DescribeMessageStreamResponse from server: %s", response)
            await self.__requests[response.request_id].put(response)
        elif response.operation == Operation.UnknownOperationError:
            self.logger.error(
                "Received response with unsupported operation from server: %s. "
                "You should update your server version",
                response.operation,
            )
            response = UnknownOperationError.from_dict(payload)
            await self.__requests[response.request_id].put(response)
        elif response.operation == Operation.Unknown:
            self.logger.error("Received response with unknown operation from server: %s", response)
            try:
                request_id = cbor2.loads(response.payload)["requestId"]
                await self.__requests[request_id].put(response)
            except Exception:
                # We tried our best to figure out the request id, but it failed.
                # We already logged the unknown operation, so there's nothing
                # else we can do at this point
                pass
        else:
            self.logger.error("Received data with unhandled operation %s.", response.operation)

    async def __connect_request_response(self):
        data = ConnectRequest()
        data.request_id = UtilInternal.get_request_id()
        data.sdk_version = self.__SDK_VERSION
        data.other_supported_protocol_versions = self.__OLD_SUPPORTED_PROTOCOL_VERSIONS
        data.protocol_version = VersionInfo.PROTOCOL_VERSION.value
        if self.auth_token is not None:
            data.auth_token = self.auth_token

        # Write the connect version
        self.__writer.write(UtilInternal.int_to_bytes(self.__CONNECT_VERSION, 1))
        # Write request to socket
        frame = MessageFrame(operation=Operation.Connect, payload=cbor2.dumps(data.as_dict()))
        for b in UtilInternal.encode_frame(frame):
            self.__writer.write(b)
        await self.__writer.drain()

        # Read connect version
        connect_response_version_byte = await self.__reader.read(n=1)
        if len(connect_response_version_byte) == 0:
            raise asyncio.IncompleteReadError(connect_response_version_byte, 1)

        connect_response_version = UtilInternal.int_from_bytes(connect_response_version_byte)
        if connect_response_version != self.__CONNECT_VERSION:
            self.logger.error("Unexpected response from the server, Connect version: %s.", connect_response_version)
            raise ConnectFailedException("Failed to establish connection with the server")

        # Read connect response
        response = await self.__read_message_frame()  # type: MessageFrame

        if response.operation == Operation.ConnectResponse:
            payload = cbor2.loads(response.payload)
            response = ConnectResponse.from_dict(payload)  # type: ConnectResponse
            self.logger.debug("Received ConnectResponse from server: %s", response)
        else:
            self.logger.error("Received data with unexpected operation %s.", response.operation)
            raise ConnectFailedException("Failed to establish connection with the server")

        if response.status != ResponseStatusCode.Success:
            self.logger.error("Received ConnectResponse with unexpected status %s.", response.status)
            raise ConnectFailedException("Failed to establish connection with the server")

        if data.protocol_version != response.protocol_version:
            self.logger.warn(
                "SDK with version %s using Protocol version %s is not fully compatible with Server with version %s. "
                "Client has connected in a compatibility mode using protocol version %s. "
                "Some features will not work as expected",
                self.__SDK_VERSION,
                data.protocol_version,
                response.server_version,
                response.protocol_version,
            )

    async def __send_and_receive(self, operation, data):
        async def inner(operation, data):
            if data.request_id is None:
                data.request_id = UtilInternal.get_request_id()

            validation = UtilInternal.is_invalid(data)
            if validation:
                raise ValidationException(validation)

            # If we're not connected, immediately try to reconnect
            if not self.connected:
                await self.__connect()

            self.__requests[data.request_id] = asyncio.Queue(1)

            # Write request to socket
            frame = MessageFrame(operation=operation, payload=cbor2.dumps(data.as_dict()))
            for b in UtilInternal.encode_frame(frame):
                self.__writer.write(b)
            await self.__writer.drain()

            # Wait for reader to come back with the response
            result = await self.__requests[data.request_id].get()
            # Drop async queue from request map
            del self.__requests[data.request_id]
            if isinstance(result, MessageFrame) and result.operation == Operation.Unknown:
                raise ClientException("Received response with unknown operation from server")
            return result

        # Perform the actual work as async so that we can put a timeout on the whole operation
        try:
            return await asyncio.wait_for(inner(operation, data), timeout=self.request_timeout, loop=self.__loop)
        except asyncio.TimeoutError:
            # Drop async queue from request map
            del self.__requests[data.request_id]
            raise

    def __validate_read_message_options(self, options: Optional[ReadMessagesOptions]):
        if options is not None:
            if not isinstance(options, ReadMessagesOptions):
                raise ValidationException("options argument to read_messages must be a ReadMessageOptions object")
            validation = UtilInternal.is_invalid(options)
            if validation:
                raise ValidationException(validation)
            if (
                options.min_message_count is not None
                and options.max_message_count is not None
                and options.min_message_count > options.max_message_count
            ):
                raise ValidationException("min_message_count must be less than or equal to max_message_count")
            if options.read_timeout_millis is not None and options.read_timeout_millis > self.request_timeout * 1000:
                raise ValidationException(
                    "read_timeout_millis must be less than or equal to the client's request_timeout"
                )

    async def _append_message(self, stream_name: str, data: bytes) -> int:
        append_message_request = AppendMessageRequest(name=stream_name, payload=data)
        append_message_response = await self.__send_and_receive(
            Operation.AppendMessage, data=append_message_request
        )  # type: AppendMessageResponse

        UtilInternal.raise_on_error_response(append_message_response)
        return append_message_response.sequence_number

    async def _create_message_stream(self, definition: MessageStreamDefinition) -> None:
        if not isinstance(definition, MessageStreamDefinition):
            raise ValidationException("definition argument to create_stream must be a MessageStreamDefinition object")
        create_stream_request = CreateMessageStreamRequest(definition=definition)
        create_stream_response = await self.__send_and_receive(
            Operation.CreateMessageStream, data=create_stream_request
        )  # type: CreateMessageStreamResponse

        UtilInternal.raise_on_error_response(create_stream_response)

    async def _delete_message_stream(self, stream_name: str) -> None:
        delete_stream_request = DeleteMessageStreamRequest(name=stream_name)
        delete_stream_response = await self.__send_and_receive(
            Operation.DeleteMessageStream, data=delete_stream_request
        )  # type: DeleteMessageStreamResponse

        UtilInternal.raise_on_error_response(delete_stream_response)

    async def _update_message_stream(self, definition: MessageStreamDefinition) -> None:
        if not isinstance(definition, MessageStreamDefinition):
            raise ValidationException(
                "definition argument to update_message_stream must be a MessageStreamDefinition object"
            )
        update_stream_request = UpdateMessageStreamRequest(definition=definition)
        update_stream_response = await self.__send_and_receive(
            Operation.UpdateMessageStream, data=update_stream_request
        )  # type: UpdateMessageStreamResponse

        UtilInternal.raise_on_error_response(update_stream_response)

    async def _read_messages(self, stream_name: str, options: ReadMessagesOptions = None) -> List[Message]:
        self.__validate_read_message_options(options)
        read_messages_request = ReadMessagesRequest(stream_name=stream_name, read_messages_options=options)
        read_messages_response = await self.__send_and_receive(
            Operation.ReadMessages, data=read_messages_request
        )  # type: ReadMessagesResponse

        UtilInternal.raise_on_error_response(read_messages_response)
        return read_messages_response.messages

    async def _list_streams(self) -> List[str]:
        list_streams_response = await self.__send_and_receive(
            Operation.ListStreams, data=ListStreamsRequest()
        )  # type: ListStreamsResponse

        UtilInternal.raise_on_error_response(list_streams_response)
        return list_streams_response.streams

    async def _describe_message_stream(self, stream_name: str) -> MessageStreamInfo:
        describe_message_stream_response = await self.__send_and_receive(
            Operation.DescribeMessageStream, data=DescribeMessageStreamRequest(name=stream_name)
        )  # type: DescribeMessageStreamResponse
        UtilInternal.raise_on_error_response(describe_message_stream_response)

        return describe_message_stream_response.message_stream_info

    ####################
    #    PUBLIC API    #
    ####################
    def read_messages(self, stream_name: str, options: Optional[ReadMessagesOptions] = None) -> List[Message]:
        """
        Read message(s) from a chosen stream with options. If no options are specified it will try to read
        1 message from the stream.

        :param stream_name: The name of the stream to read from.
        :param options: (Optional) Options used when reading from the stream of type :class:`.data.ReadMessagesOptions`.
            Defaults are:

            * desired_start_sequence_number: 0,
            * min_message_count: 1,
            * max_message_count: 1,
            * read_timeout_millis: 0 ``# Where 0 here represents that the server will immediately return the messages``
                                     ``# or an exception if there were not enough messages available.``
            If desired_start_sequence_number is specified in the options and is less
            than the current beginning of the stream, returned messages will start
            at the beginning of the stream and not necessarily the desired_start_sequence_number.
        :return: List of at least 1 message.
        :raises: :exc:`~.exceptions.StreamManagerException` and subtypes based on the precise error.
        :raises: :exc:`asyncio.TimeoutError` if the request times out.
        :raises: :exc:`ConnectionError` if the client is unable to reconnect to the server.
        """
        self.__check_closed()
        return UtilInternal.sync(self._read_messages(stream_name, options), loop=self.__loop)

    def append_message(self, stream_name: str, data: bytes) -> int:
        """
        Append a message into the specified message stream. Returns the sequence number of the message
        if it was successfully appended.

        :param stream_name: The name of the stream to append to.
        :param data: Bytes type data.
        :return: Sequence number that the message was assigned if it was appended.
        :raises: :exc:`~.exceptions.StreamManagerException` and subtypes based on the precise error.
        :raises: :exc:`asyncio.TimeoutError` if the request times out.
        :raises: :exc:`ConnectionError` if the client is unable to reconnect to the server.
        """
        self.__check_closed()
        return UtilInternal.sync(self._append_message(stream_name, data), loop=self.__loop)

    def create_message_stream(self, definition: MessageStreamDefinition) -> None:
        """
        Create a message stream with a given definition.

        :param definition: :class:`~.data.MessageStreamDefinition` definition object.
        :return: Nothing is returned if the request succeeds.
        :raises: :exc:`~.exceptions.StreamManagerException` and subtypes based on the precise error.
        :raises: :exc:`asyncio.TimeoutError` if the request times out.
        :raises: :exc:`ConnectionError` if the client is unable to reconnect to the server.
        """
        self.__check_closed()
        return UtilInternal.sync(self._create_message_stream(definition), loop=self.__loop)

    def delete_message_stream(self, stream_name: str) -> None:
        """
        Deletes a message stream based on its name. Nothing is returned if the request succeeds,
        a subtype of :exc:`~.exceptions.StreamManagerException` will be raised if an error occurs.

        :param stream_name: The name of the stream to be deleted.
        :return: Nothing is returned if the request succeeds.
        :raises: :exc:`~.exceptions.StreamManagerException` and subtypes based on the precise error.
        :raises: :exc:`asyncio.TimeoutError` if the request times out.
        :raises: :exc:`ConnectionError` if the client is unable to reconnect to the server.
        """
        self.__check_closed()
        return UtilInternal.sync(self._delete_message_stream(stream_name), loop=self.__loop)

    def update_message_stream(self, definition: MessageStreamDefinition) -> None:
        """
        Updates a message stream based on a given definition.
        Minimum version requirements: StreamManager server version 1.1 (or AWS IoT Greengrass Core 1.11.0)

        :param definition: class:`~.data.MessageStreamDefinition` definition object.
        :return: Nothing is returned if the request succeeds.
        :raises: :exc:`~.exceptions.StreamManagerException` and subtypes based on the precise error.
        :raises: :exc:`asyncio.TimeoutError` if the request times out.
        :raises: :exc:`ConnectionError` if the client is unable to reconnect to the server.
        """
        self.__check_closed()
        return UtilInternal.sync(self._update_message_stream(definition), loop=self.__loop)

    def list_streams(self) -> List[str]:
        """
        List the streams in StreamManager. Returns a list of their names.

        :return: List of stream names.
        :raises: :exc:`~.exceptions.StreamManagerException` and subtypes based on the precise error.
        :raises: :exc:`asyncio.TimeoutError` if the request times out.
        :raises: :exc:`ConnectionError` if the client is unable to reconnect to the server.
        """
        self.__check_closed()
        return UtilInternal.sync(self._list_streams(), loop=self.__loop)

    def describe_message_stream(self, stream_name: str) -> MessageStreamInfo:
        """
        Describe a message stream to get metadata including the stream's definition,
        size, and exporter statuses.

        :param stream_name: The name of the stream to describe.
        :return: :class:`~.data.MessageStreamInfo` type containing the stream information.
        :raises: :exc:`~.exceptions.StreamManagerException` and subtypes based on the precise error.
        :raises: :exc:`asyncio.TimeoutError` if the request times out.
        :raises: :exc:`ConnectionError` if the client is unable to reconnect to the server.
        """
        self.__check_closed()
        return UtilInternal.sync(self._describe_message_stream(stream_name), loop=self.__loop)

    def close(self):
        """
        Call to shutdown the client and close all existing connections. Once a client is closed it cannot be reused.

        :raises: :exc:`~.exceptions.StreamManagerException` and subtypes based on the precise error.
        """
        if not self.__closed:
            UtilInternal.sync(self._close(), loop=self.__loop)
        if not self.__loop.is_closed():
            self.__loop.call_soon_threadsafe(self.__loop.stop)
