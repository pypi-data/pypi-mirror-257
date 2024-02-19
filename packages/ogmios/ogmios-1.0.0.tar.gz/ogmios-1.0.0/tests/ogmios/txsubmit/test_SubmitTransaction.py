import pytest
import pycardano as pyc

from ogmios.errors import ResponseError
from tests.ogmios.test_fixtures import (
    chain_context,
    test_psk,
    test_ssk,
    test_pvk,
    test_svk,
    test_address,
)

# pyright can't properly parse models, so we need to ignore its type checking
#  (pydantic will still throw errors if we misuse a data type)
# pyright: reportGeneralTypeIssues=false


def test_SubmitTransaction(chain_context, test_psk, test_pvk, test_svk, test_address):
    tx_builder = pyc.TransactionBuilder(chain_context)
    tx_builder.add_input_address(test_address)
    tx_builder.add_output(
        pyc.TransactionOutput(
            test_address,
            pyc.Value.from_primitive([1_000_000]),
        )
    )
    signed_tx = tx_builder.build_and_sign([test_psk], change_address=test_address)

    resp = chain_context.client.submit_transaction.execute(signed_tx.to_cbor_hex())
    assert resp[0] == str(signed_tx.id)
