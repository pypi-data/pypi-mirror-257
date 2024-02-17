import asyncio
import time

from ..core.settings import settings
from ..wallet.wallet import Wallet

start = time.time()
runs = 10


async def main():
    wallet = Wallet(settings.mint_url, "benchmark")

    await wallet.load_proofs()
    await wallet.load_mint()
    time.time()
    for i in range(runs):
        print(".", flush=True)
        await wallet.split(wallet.proofs, 10)


if __name__ == "__main__":
    asyncio.run(main())
