import os
import pytest
from napalm import get_network_driver

pytestmark = pytest.mark.network

@pytest.fixture(scope="module")
def device():
    d = get_network_driver("ios")("10.10.20.48",
                                  os.environ["NET_USER"], os.environ["NET_PASS"])
    d.open()
    yield d
    d.close()

def test_gi1_is_up(device):
    assert device.get_interfaces()["GigabitEthernet1"]["is_up"]

def test_loopback401_has_correct_ip(device):
    ips = device.get_interfaces_ip()
    assert "10.41.1.1" in ips["Loopback401"]["ipv4"]