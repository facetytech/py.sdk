'''Collection of gRPC tools.'''

from google.protobuf.message import Message as _Message
from google.protobuf.json_format import ParseDict as _ParseDict
from google import auth as _google_auth
from google.auth.transport import grpc as _google_auth_transport_grpc
from google.auth.transport import requests as _google_auth_transport_requests

import grpc as _grpc

from google.protobuf.json_format import MessageToDict as _MessageToDict


__all__ = ['request_normaliser', 'get_message']


def request_normaliser(request_obj, request_type, *args, **kwargs) -> _Message:
    '''Normalise the request to the given type.

    Args:
        request_obj (dict | Type[super().request_type]): The request to normalize.
        It can be a dictionary or an instance of the specified request_type.
        request_type: The type of the request.

    Returns:
        The normalised request.

    Raises:
        TypeError: If the request is neither a dictionary nor an instance of the specified request_type.
    '''

    match request_obj:
        case dict():
            normalised = request_type()
            _ParseDict(request_obj, normalised)
            return normalised

        case request_type():
            return request_obj

        case _:
            raise TypeError(f'The request should be a dict or {type(request_type)} instance.')


def get_message(
    host: str,
    scopes: str | list,
    insecure: bool,
    request: _Message,
    stub,
    method: str,
    simple: bool = True,
    *args,
    **kwargs,
):
    '''Get a message from the specified host and method.

    Retrieves a message by sending a request to the specified host and method.
    The response can be returned as a dictionary or as a protobuf message object.

    Args:
        host (str): The host to send the request to.
        scopes (str | list): The required scopes for authentication. It can be a single scope string
            or a list of scope strings.
        insecure (bool): A flag indicating whether to use an insecure channel (default: False).
        request (_Message): The request message object to send.
        stub: The stub object used to make the gRPC call.
        method (str): The name of the method to call.
        simple (bool): A flag indicating whether to return the response as a dictionary (default: True).

    Returns:
        dict | _Message: The response message. If `simple` is True, the response is returned as a dictionary,
            otherwise, it is returned as a protobuf message object.
    '''

    if insecure:
        with _grpc.insecure_channel(host) as channel:
            respond = getattr(stub(channel), method)(request)

    else:
        credentials, _ = _google_auth.default(scopes=(scopes,))
        transport = _google_auth_transport_requests.Request()
        with _google_auth_transport_grpc.secure_authorized_channel(credentials, transport, host) as channel:
            respond = getattr(stub(channel), method)(request)

    return _MessageToDict(respond) if simple else respond
