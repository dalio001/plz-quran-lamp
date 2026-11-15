"""Calls the MCP tools directly against the real lamp (read-only ones plus a same-value volume write)."""
import asyncio
import json

import server


async def main():
    print(json.dumps(await server.lamp_status(), indent=1))
    print(await server.list_items("reciters"))
    print(await server.list_items("translations"))
    print(await server.list_items("books"))
    print(await server.prayer_times())
    status = await server.lamp_status()
    print(await server.set_volume(status["volume"]))


asyncio.run(main())
