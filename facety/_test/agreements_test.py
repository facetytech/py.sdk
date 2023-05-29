import pytest
import grpc
from concurrent import futures
from google.protobuf.timestamp_pb2 import Timestamp as Ts
from google.protobuf.empty_pb2 import Empty
from datetime import datetime as dt

from facety.agreements import AdoptionClient, ReceivingClient, messages, services


PORT = 2002


class AdoptionServicer(services.AdoptionServicer):
    def CheckProtocol(self, request, context):
        verdict = messages.Verdict()

        tos = verdict.tos
        tos.status = True
        tos.comment = 'sss'

        pp = verdict.pp
        pp.status = False
        pp.comment = 'ddd'

        remark = verdict.remark
        remark.status = True
        remark.comment = 'fff'

        return verdict

    def AddProtocol(self, request, context):
        return messages.Selector(id='aaa')

    def AddRemark(self, request, context):
        return Empty()


class ReceivingServicer(services.ReceivingServicer):
    def Texts(self, request, context):
        agreements = messages.Agreements()

        tos = agreements.tos
        tos.text = 'tos'
        tos.version = '1'
        tos.hash = 'h'
        tos.lang = 'fr'

        pp = agreements.pp
        pp.text = 'tos'
        pp.version = '1'
        pp.hash = 'h'
        pp.lang = 'fr'

        remarks = agreements.remarks.add()
        remarks.text = 'tos'
        remarks.version = '1'
        remarks.hash = 'h'

        return agreements


class MygRPC:
    def __init__(self):
        self.server = None

    def start(self):
        self.server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))

        services.add_AdoptionServicer_to_server(AdoptionServicer(), self.server)
        services.add_ReceivingServicer_to_server(ReceivingServicer(), self.server)

        self.server.add_insecure_port(f'[::]:{PORT}')
        self.server.start()

    def stop(self):
        if self.server:
            self.server.stop(0)


adoption_client = AdoptionClient(host=f'localhost:{PORT}', insecure=True)
receiving_client = ReceivingClient(host=f'localhost:{PORT}', insecure=True)


class TestAdoption:
    @classmethod
    @pytest.fixture(scope="class")
    def grpc_server(cls):
        server = MygRPC()
        server.start()
        yield server
        server.stop()

    def test_add_protocol(self, grpc_server):
        '''Testing the add_protocol method.'''

        timestamp = Ts()
        timestamp.FromDatetime(dt.now())

        protocol = messages.Protocol()

        protocol.previously = 'prev'

        h1 = protocol.headers.add()
        h1.key = 'h1'
        h1.value = 'v1'

        h2 = protocol.headers.add()
        h2.key = 'h2'
        h2.value = 'v2'

        tos = protocol.tos
        tos.version = '1'
        tos.hash = 'hash'
        tos.lang = 'fr'
        tos.timestamp.CopyFrom(timestamp)

        pp = protocol.pp
        pp.version = '1'
        pp.hash = 'hash'
        pp.lang = 'de'
        pp.timestamp.CopyFrom(timestamp)

        remark = protocol.remarks.add()
        remark.version = '1'
        remark.hash = 'hash'
        remark.country = 'FR'
        remark.timestamp.CopyFrom(timestamp)

        adoption_client.add_protocol(protocol=protocol)

    def test_check_protocol(self, grpc_server):
        '''Testing the check_protocol method.'''

        adoption_client.check_protocol(selector=messages.Selector(id='aaa'))

    def test_add_remark(self, grpc_server):
        '''Testing the add_remark method.'''

        timestamp = Ts()
        timestamp.FromDatetime(dt.now())

        new = messages.NewRemark()
        new.owner = 'owner'

        protocol = new.remark

        protocol.version = '1'
        protocol.hash = 'hash'
        protocol.country = 'FR'
        protocol.timestamp.CopyFrom(timestamp)

        adoption_client.add_remark(new=new)


class TestReceiving:  # noqa: D101
    @classmethod
    @pytest.fixture(scope="class")
    def grpc_server(cls):
        server = MygRPC()
        server.start()
        yield server
        server.stop()

    def test_texts(self, grpc_server):
        '''Testing the texts method.'''

        user = messages.User()
        user.protocol = 'aaa'
        user.country = 'UA'

        user.langs.extend(['fr', 'de'])

        receiving_client.get_texts(user=user)
