'''Working with agreements, their versions and acceptance protocols.

Contains client for gRPC service , collection of server-needs objects and .proto content.
'''

from os import path as _path
from pathlib import Path as _Path

from ._grpc import agreements_pb2_grpc as services
from ._grpc import agreements_pb2 as messages

from ._abc.grpc import ClientGRPC as _ClientGRPC
from .tools import meta as _meta
from .tools.grpc import request_normaliser as _request_normaliser
from .tools.grpc import get_message as _get_message


__all__ = [
    'proto',
    'services',
    'messages',
    'AdoptionClient',
    'ReceivingClient',
]

_HOST_VAR = _meta()['host']['agreements-grpc-variable']


def proto(show: bool = False) -> str | None:
    '''Get or print .proto content.

    Args:
        show: if True, print the content, else return it as a string.

    Returns:
        The content of .proto file as a string or print it.

    Raises:
        RuntimeError: if the definition file is not found.
    '''

    relative_part = '_grpc/public/proto'

    file_name = __package__.rsplit('.', 1)[-1]
    file_path = _path.join(_path.dirname(__file__), relative_part, f'{file_name}.proto')

    if _Path(file_path).is_file() is False:
        raise RuntimeError('The definition file is not found. PLease find it in the documentation.')

    with open(file_path, 'r', encoding='utf-8') as file:
        if show:
            print(file.read())
        else:
            return file.read()


class _AgreementsClient(_ClientGRPC, host_variable=_HOST_VAR):
    pass


class AdoptionClient(_AgreementsClient):
    '''The client for the Adoption service.

    Provides methods: check_protocol, add_protocol and add_remark.
    '''

    def check_protocol(
        self, selector: messages.Selector | dict, *args, simple: bool = True, **kwargs
    ) -> messages.Verdict | dict:
        '''Check protocol for a user.

        Checks the protocol for a given user using the provided user object or dictionary.

        Args:
            user (User | dict): The user to check the protocol for. It can be an instance of the User class
                or a dictionary representing the user.
            simple (bool): A flag indicating whether to use the simple mode (default: True).

        Returns:
            Verdict | dict: The response verdict or a dictionary response.
        '''

        request = _request_normaliser(selector, messages.Selector)

        return _get_message(
            host=self.host,
            scopes=self.scope,
            insecure=self.insecure,
            request=request,
            stub=services.AdoptionStub,
            method='CheckProtocol',
            simple=simple,
            **kwargs,
        )

    def add_protocol(
        self, protocol: messages.Protocol | dict, *args, simple: bool = True, **kwargs
    ) -> messages.Selector | dict:
        '''Add a new protocol.

        Adds a protocol using the provided protocol object or dictionary.

        Args:
            protocol (Protocol | dict): The protocol to add. It can be an instance of Protocol class
                or a dictionary representing the protocol.

        Returns:
            Selector | dict: The response protocol selector or a dictionary response.
        '''

        request = _request_normaliser(protocol, messages.Protocol)

        return _get_message(
            host=self.host,
            scopes=self.scope,
            insecure=self.insecure,
            request=request,
            stub=services.AdoptionStub,
            method='AddProtocol',
            simple=simple,
            **kwargs,
        )

    def add_remark(self, remark: messages.Remark | dict, *args, **kwargs) -> None:
        '''Add a remark.

        Adds a country remark using the provided remark object or dictionary.

        Args:
            remark (NewRemark | dict): The remark to add. It can be an instance of NewRemark class
                or a dictionary representing the remark.
        '''

        request = _request_normaliser(remark, messages.Remark)

        return _get_message(
            host=self.host,
            scopes=self.scope,
            insecure=self.insecure,
            request=request,
            stub=services.AdoptionStub,
            method='AddRemark',
            **kwargs,
        )


class ReceivingClient(_AgreementsClient):
    '''The client for the Receiving service.

    Return texts of agreements and their metadata.
    '''

    def get_texts(
        self, user: messages.User | dict, *args, simple: bool = True, **kwargs
    ) -> messages.Agreements | dict:
        '''Get texts of agreements.

        Args:
            user: the User instance (languages list & country).

        Returns:
            The Agreements instance.
        '''

        request = _request_normaliser(user, messages.User)

        return _get_message(
            host=self.host,
            scopes=self.scope,
            insecure=self.insecure,
            request=request,
            stub=services.ReceivingStub,
            method='Texts',
            simple=simple,
            **kwargs,
        )
