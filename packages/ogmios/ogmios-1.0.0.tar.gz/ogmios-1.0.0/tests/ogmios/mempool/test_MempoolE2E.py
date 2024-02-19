import pytest
import time
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


def test_Mempool_E2E(chain_context, test_psk, test_pvk, test_svk, test_address):
    # Build and submit a transaction
    tx_builder = pyc.TransactionBuilder(chain_context)
    tx_builder.add_input_address(test_address)
    tx_builder.add_output(
        pyc.TransactionOutput(
            test_address,
            pyc.Value.from_primitive([10_000_000]),
        )
    )
    signed_tx = tx_builder.build_and_sign([test_psk], change_address=test_address)
    chain_context.client.submit_transaction.execute(signed_tx.to_cbor_hex())

    # Acquire a mempool snapshot and get the transaction
    chain_context.client.acquire_mempool.execute()
    tx, id = chain_context.client.next_transaction.execute()
    assert tx.get("id") == str(signed_tx.id)
    chain_context.client.release_mempool.execute()

    # Wait for the transaction to be removed from the mempool
    while True:
        chain_context.client.acquire_mempool.execute()
        tx, id = chain_context.client.next_transaction.execute()
        chain_context.client.release_mempool.execute()
        if tx is None:
            assert True
            break
        time.sleep(1)
