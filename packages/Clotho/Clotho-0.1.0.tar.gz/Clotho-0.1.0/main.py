#!/bin/env python
import asyncio
import sys
from mitmproxy import options
from mitmproxy.tools.dump import DumpMaster
from clotho import Clotho


async def start_proxy(host, port):
    opts = options.Options(listen_host=host, listen_port=port)
    clotho = Clotho()
    m = DumpMaster(opts)

    m.addons.add(clotho)

    await m.run()
    return m


def cli():
    if len(sys.argv) != 3:
        print("Run with clotho listen_host listen_port, e.g. clotho localhost 8080")
        sys.exit(1)
    host = sys.argv[1]
    port = int(sys.argv[2])
    asyncio.run(start_proxy(host, port))


if __name__ == "__main__":
    cli()
