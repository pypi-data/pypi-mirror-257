import time
import unittest
from DLMS_SPODES.cosem_interface_classes import collection
from DLMS_SPODES.types import cdt
from src.DLMS_SPODES_client.client import Client, SerialPort, Network, AsyncNetwork, Collection, AppVersion, AsyncSerial
from src.DLMS_SPODES_client.servers import TransactionServer, Operation, TransactionServer2
from src.DLMS_SPODES_client import exchanges_properties as eprop


class TestType(unittest.TestCase):
    def test_init_SerialPort(self):
        client = Client()
        client.media = SerialPort(
            port="COM13",
            inactivity_timeout=1
        )
        client.connect()
        client.init_type()
        client.close()
        print(client.objects)
        client.SAP.set(0x30)
        client.secret = b'0000000000000000'
        client.connect()
        p = client.objects.get_object("0.0.40.0.1.255")
        # p = client.objects.get_object("1.0.99.1.0.255")
        client.read_attribute(p, 2)
        client.close()
        for el in p.object_list:
            print(el)

    def test_network(self):
        client = Client(
            secret="00 00 00 00 00 00 00 00",
            addr_size=1,
            conformance="010000000001111000011101")
        client.mechanism_id.set(0)
        client.device_address.set(0)
        client.media = Network(
            host="127.0.0.1",
            port=10000
        )
        client.connect()
        client.close()

    def test_async_network(self):
        client = Client(
            secret="00 00 00 00 00 00 00 00",
            addr_size=1,
            conformance="010000000001111000011101")
        type_ = "4d324d5f31"
        ver = "1.5.7"
        man = b"KPZ"
        # client.objects = collection.get(
        #     m=man,
        #     t=cdt.OctetString(type_),
        #     ver=AppVersion.from_str(ver))
        client.mechanism_id.set(0)
        client.device_address.set(0)
        client.media = AsyncSerial(
            port="COM3"
        )
        t_server = TransactionServer()
        ev = t_server.task((Operation.OPEN, client, None))
        print(f"{ev.is_set()=}")
        ev.wait(timeout=3)
        # t_server.q_in.put((Operation.OPEN, client, None))
        t_server.q_in.put((Operation.INIT_TYPE, client, None))
        t_server.q_in.put((Operation.READ, client, "0.0.42.0.0.255", 2))
        t_server.q_in.put((Operation.READ, client, "0.0.1.0.0.255", 2))
        t_server.q_in.put((Operation.CLOSE, client, None))
        while not t_server.q_out.empty():
            print(f"{t_server.q_out.get()=}")
        time.sleep(5)

    def test_async_network2(self):
        client = Client(
            secret="00 00 00 00 00 00 00 00",
            addr_size=1,
            conformance="010000000001111000011101")
        type_ = "4d324d5f31"
        ver = "1.5.7"
        man = b"KPZ"
        # client.objects = collection.get(
        #     m=man,
        #     t=cdt.OctetString(type_),
        #     ver=AppVersion.from_str(ver))
        client.mechanism_id.set(0)
        client.device_address.set(0)
        client.media = AsyncSerial(
            port="COM3"
        )
        client2 = Client(
            secret="00 00 00 00 00 00 00 00",
            addr_size=1,
            conformance="010000000001111000011101")
        client2.mechanism_id.set(0)
        client2.device_address.set(0)
        client2.media = AsyncSerial(
            port="COM13"
        )
        client3 = Client(
            secret="00 00 00 00 00 00 00 00",
            addr_size=1,
            conformance="010000000001111000011101")
        client3.mechanism_id.set(0)
        client3.device_address.set(0)
        client3.media = AsyncNetwork(
            host="127.0.0.1",
            port=10000
        )
        t_server = TransactionServer2(
            clients=[client, client2, client3],
            exchanges=(
                eprop.InitType(),
                eprop.ReadAttribute("0.0.1.0.0.255", 2),))
        t_server.start()
        # print(f"{t_server.is_complete()=}")
        # time.sleep(1)
        # print(f"{t_server.is_complete()=}")
        # time.sleep(1)
        # print(f"{t_server.is_complete()=}")
        # t_s2 = TransactionServer2(
        #     clients=[client2, client3],
        #     exchanges=(eprop.ReadAttribute("0.0.42.0.0.255", 2),))
        # t_se.start()
        time.sleep(.3)
        for r in t_server.results:
            print(F'{r.complete=}')
        print("end")
        time.sleep(3)
        print(f"{t_server.is_complete()=}")
        print(t_server.results.ok_clients)

