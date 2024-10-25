import asyncio


async def sleep(tics: int):
    for _ in range(tics):
        await asyncio.sleep(0)
