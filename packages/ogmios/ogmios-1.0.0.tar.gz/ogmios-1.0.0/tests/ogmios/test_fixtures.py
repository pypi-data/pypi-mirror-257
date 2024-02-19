import pytest
import pycardano as pyc

from ogmios import OgmiosChainContext
from ogmios.client import Client


@pytest.fixture
def client():
    with Client() as client:
        yield client


@pytest.fixture
def chain_context():
    with OgmiosChainContext("localhost", 1337) as chain_context:
        yield chain_context


@pytest.fixture
def test_psk():
    yield pyc.PaymentExtendedSigningKey.load("./tests/test_wallet/test_addr0.skey")


@pytest.fixture
def test_ssk():
    yield pyc.StakeExtendedSigningKey.load("./tests/test_wallet/test_stake.skey")


@pytest.fixture
def test_pvk(test_psk):
    yield pyc.PaymentVerificationKey.from_signing_key(test_psk)


@pytest.fixture
def test_svk(test_ssk):
    yield pyc.StakeVerificationKey.from_signing_key(test_ssk)


@pytest.fixture
def test_address(test_pvk, test_svk):
    yield pyc.Address(test_pvk.hash(), test_svk.hash(), pyc.Network.TESTNET)
