'''Abstract classes for gRPC interaction.'''

from os import environ as _env
from abc import ABC as _ABC

from ..tools import meta as _meta


__all__ = ['ClientGRPC']
_AGREEMENTS_HOST = _meta()['host']['agreements-grpc']


class ClientGRPC(_ABC):
    '''Base class for GRPC clients.'''

    def __init_subclass__(
        cls,
        *args,
        host_variable: str | None = None,
        host_default: str | None = _AGREEMENTS_HOST,
        insecure_default: bool = False,
        scope_default: str | None = None,
        **kwargs,
    ):
        '''Initialize the subclass of ClientGRPC.

        Args:
            host_variable (str | None): The name of the environment variable to retrieve the host from.
            host_default (str | None): The default host to use if not provided or environment variable is empty.
            insecure_default (bool): The default value for the insecure flag.
            scope_default (str | None): The default value for the scope.
        '''

        cls._host_variable = host_variable
        cls._host_default = host_default
        cls._insecure_default = insecure_default
        cls._scope_default = scope_default

        super().__init_subclass__(*args, **kwargs)

    def __init__(
        self,
        *args,
        host: str | None = None,
        scope: str | None = None,
        insecure: bool | None = None,
        **kwargs,
    ):
        '''Initialize the ClientGRPC instance.

        Args:
            host (str | None): The host to connect to. If None, it tries to retrieve from environment variable.
            scope (str | None): The scope of the client. If None, it uses the default or host value.
            insecure (bool | None): Whether to use an insecure connection. If None, it uses the default value.
        '''

        if host:
            self.host = host
        else:
            if self._host_variable in _env and _env[self._host_variable] != '':
                self.host = _env[self._host_variable]
            else:
                self.host = self._host_default

        self.scope = scope or self._scope_default or self.host
        self.insecure = insecure or self._insecure_default

        super().__init__(*args, **kwargs)
