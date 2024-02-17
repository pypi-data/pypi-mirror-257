import asyncio
import time
from typing import List, Union

import pytest
import pytest_asyncio

from cashu.core.base import Proof
from cashu.core.errors import CashuError
from cashu.core.settings import settings
from cashu.nostr.key import PrivateKey
from cashu.wallet.crud import get_nostr_last_check_timestamp
from cashu.wallet.nostr import receive_nostr, send_nostr
from cashu.wallet.wallet import Wallet
from tests.conftest import SERVER_ENDPOINT
from tests.helpers import pay_if_regtest


async def assert_err(f, msg: Union[str, CashuError]):
    """Compute f() and expect an error message 'msg'."""
    try:
        await f
    except Exception as exc:
        error_message: str = str(exc.args[0])
        if isinstance(msg, CashuError):
            if msg.detail not in error_message:
                raise Exception(
                    f"CashuError. Expected error: {msg.detail}, got: {error_message}"
                )
            return
        if msg not in error_message:
            raise Exception(f"Expected error: {msg}, got: {error_message}")
        return
    raise Exception(f"Expected error: {msg}, got no error")


def assert_amt(proofs: List[Proof], expected: int):
    """Assert amounts the proofs contain."""
    assert [p.amount for p in proofs] == expected


async def reset_wallet_db(wallet: Wallet):
    await wallet.db.execute("DELETE FROM proofs")
    await wallet.db.execute("DELETE FROM proofs_used")
    await wallet.db.execute("DELETE FROM keysets")
    await wallet._load_mint()


@pytest_asyncio.fixture(scope="function")
async def wallet(mint):
    wallet = await Wallet.with_db(
        url=SERVER_ENDPOINT,
        db="test_data/wallet_nostr",
        name="wallet",
    )
    await wallet.load_mint()
    yield wallet


@pytest.mark.asyncio
@pytest.mark.skip(reason="Nostr test is flaky")
async def test_send_nostr(wallet: Wallet):
    invoice = await wallet.request_mint(64)
    pay_if_regtest(invoice.bolt11)
    await wallet.mint(64, id=invoice.id)
    assert wallet.balance == 64

    key = PrivateKey()
    settings.nostr_private_key = key.bech32()

    # send
    await send_nostr(wallet, amount=64, pubkey=key.public_key.bech32(), yes=True)
    assert wallet.available_balance == 0
    await asyncio.sleep(1)

    # receive
    client = await receive_nostr(wallet)
    await asyncio.sleep(5)
    client.relay_manager.close_connections()
    assert wallet.available_balance == 64

    last_check = await get_nostr_last_check_timestamp(db=wallet.db)
    assert last_check is not None
    assert last_check > 0
    assert last_check < int(time.time())
