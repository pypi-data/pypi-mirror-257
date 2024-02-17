import pytest
import pytest_asyncio

from cashu.core.crypto.b_dhke import (
    hash_to_curve,
    hash_to_curve_domain_separated,
    step1_alice,
)
from cashu.core.crypto.secp import PrivateKey
from cashu.mint.ledger import Ledger
from cashu.wallet.wallet import LedgerAPI, Wallet
from tests.conftest import SERVER_ENDPOINT
from tests.helpers import is_regtest


async def assert_err(f, msg):
    """Compute f() and expect an error message 'msg'."""
    try:
        await f
    except Exception as exc:
        if msg not in str(exc.args[0]):
            raise Exception(f"Expected error: {msg}, got: {exc.args[0]}")
        return
    raise Exception(f"Expected error: {msg}, got no error")


@pytest_asyncio.fixture(scope="function")
async def wallet(ledger: Ledger):
    wallet = await Wallet.with_db(
        url=SERVER_ENDPOINT,
        db="test_data/wallet",
        name="wallet",
    )
    await wallet.load_mint()
    yield wallet


def test_hash_to_curve_domain_separated():
    result = hash_to_curve_domain_separated(
        bytes.fromhex(
            "0000000000000000000000000000000000000000000000000000000000000000"
        )
    )
    assert (
        result.serialize().hex()
        == "024cce997d3b518f739663b757deaec95bcd9473c30a14ac2fd04023a739d1a725"
    )


def test_hash_to_curve_domain_separated_iterative():
    result = hash_to_curve_domain_separated(
        bytes.fromhex(
            "0000000000000000000000000000000000000000000000000000000000000001"
        )
    )
    assert (
        result.serialize().hex()
        == "022e7158e11c9506f1aa4248bf531298daa7febd6194f003edcd9b93ade6253acf"
    )


@pytest.mark.asyncio
@pytest.mark.skipif(is_regtest, reason="only works with FakeWallet")
async def test_multiple_preimage_h2c(wallet: Wallet, ledger: Ledger):
    invoice = await wallet.request_mint(128)
    await wallet.mint(128, id=invoice.id)
    assert wallet.balance == 128

    secret1_hex = "303030303030303030303030303030303030303030303030303030303030303030303030303030303030303030303030303030303030303030303030303030303030303030303030394d272c09"  # noqa
    secret2_hex = "062875134b5e33165b43090d00153842244b311739573b216c2f697b6430372a"

    secrets = [bytes.fromhex(secret1_hex).decode()]
    rs = [
        PrivateKey(
            privkey=bytes.fromhex(
                "0000000000000000000000000000000000000000000000000000000000000001"
            )
        )
    ]
    derivation_paths = ["custom"] * len(secrets)
    outputs, rs = wallet._construct_outputs([128], secrets, rs)

    promises = await LedgerAPI.split(wallet, wallet.proofs, outputs)
    await wallet.invalidate(wallet.proofs)
    new_proofs = await wallet._construct_proofs(promises, secrets, rs, derivation_paths)

    forged_proofs = [new_proofs[0].copy()]
    forged_proofs[0].secret = bytes.fromhex(secret2_hex).decode()

    outputs, rs = wallet._construct_outputs([128], ["testing"], rs)
    await ledger.split(proofs=new_proofs, outputs=outputs)
    outputs, rs = wallet._construct_outputs([128], ["testing2"], rs)
    await assert_err(
        ledger.split(proofs=forged_proofs, outputs=outputs),
        "already spent",
    )


def test_hash_to_curve_has_multiple_preimages():
    # this input causes multiple rounds of the hash_to_curve algorithm
    # and one of the rounds will produce a valid string again which we will use below
    byte_array_str = "303030303030303030303030303030303030303030303030303030303030303030303030303030303030303030303030303030303030303030303030303030303030303030303030394d272c09"  # noqa
    # convert to bytes
    byte_array = bytes.fromhex(byte_array_str)
    byte_array_hex_str = byte_array.hex()
    print(byte_array_hex_str)
    B_, r = step1_alice(
        byte_array.decode(),
        blinding_factor=PrivateKey(
            privkey=bytes.fromhex(
                "0000000000000000000000000000000000000000000000000000000000000001"
            )  # 32 bytes
        ),
    )

    # this is the valid string from the multiple rounds of the hash_to_curve algorithm
    # that leads to the same output of the hash_to_curve algorithm as above
    hex_collision = "062875134b5e33165b43090d00153842244b311739573b216c2f697b6430372a"
    byte_array_collision = bytes.fromhex(hex_collision)
    B_2, r2 = step1_alice(
        byte_array_collision.decode(),
        blinding_factor=PrivateKey(
            privkey=bytes.fromhex(
                "0000000000000000000000000000000000000000000000000000000000000001"
            )  # 32 bytes
        ),
    )
    assert B_.serialize().hex() == B_2.serialize().hex()

    return


def test_hash_to_curve_iteration():
    """This input causes multiple rounds of the hash_to_curve algorithm."""
    result = hash_to_curve(
        bytes.fromhex(
            "0000000000000000000000000000000000000000000000000000000000000002"
        )
    )
    result_hex = result.serialize().hex()
    assert (
        result_hex
        == "02076c988b353fcbb748178ecb286bc9d0b4acf474d4ba31ba62334e46c97c416a"
    )
    assert result.serialize().hex() == result_hex

    result2 = hash_to_curve(
        b"\x92g\xd3\xdb\xed\x80)AH?\x1a\xfa*k\xc6\x8d\xe5\xf6S\x12\x8a\xca\x9b\xf1F\x1c]\n:\xd3n\xd2"
    )
    assert result2.serialize().hex() == result_hex
