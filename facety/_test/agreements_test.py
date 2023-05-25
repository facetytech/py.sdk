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
        tos = messages.VerdictTos(status=True, comment='sss')
        pp = messages.VerdictPp(status=False, comment='ddd')
        remark = messages.VerdictRemark(status=False, comment='fff')

        return messages.Verdict(tos=tos, pp=pp, remark=remark)

    def AddProtocol(self, request, context):
        return messages.Selector(id='aaa')

    def AddRemark(self, request, context):
        return Empty()


class ReceivingServicer(services.ReceivingServicer):
    def Texts(self, request, context):
        tos = messages.AgreementsTos(text='tos', version='1', hash='h', lang='fr')
        pp = messages.AgreementsPp(text='tos', version='1', hash='h', lang='fr')
        remarks = [messages.AgreementsRemark(text='tos', version='1', hash='h')]

        return messages.Agreements(tos=tos, pp=pp, remarks=remarks)


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

        tos = messages.ProtocolTos(version='1', hash='hash', lang='fr')
        pp = messages.ProtocolPp(version='1', hash='hash', lang='de')
        remark = messages.ProtocolRemark(version='1', hash='hash', country='FR')

        adoption_client.add_protocol(
            protocol=messages.Protocol(
                tos=tos, pp=pp, remarks=[remark], headers={'h1': 'v1', 'h2': 'v2'}, previously='prev'
            )
        )

    def test_check_protocol(self, grpc_server):
        '''Testing the check_protocol method.'''

        adoption_client.check_protocol(selector=messages.Selector(id='aaa'))

    def test_add_remark(self, grpc_server):
        '''Testing the add_remark method.'''

        timestamp = Ts()
        timestamp.FromDatetime(dt.now())

        remark = messages.ProtocolRemark(version='1', hash='hash', country='FR', timestamp=timestamp)

        adoption_client.add_remark(messages.Remark(id='id', remark=remark))


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

        receiving_client.get_texts(messages.User(protocol='aaa', langs=['fr', 'de'], country='UA'))
