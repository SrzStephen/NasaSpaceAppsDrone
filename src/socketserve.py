import asyncio
import logging

logger = logging.getLogger(__name__)
from .controls import Actuators
from json import dumps, JSONDecodeError

ActuatorClass = Actuators()
import click


class EchoServerProtocol:
    def connection_made(self, transport):
        self.transport = transport

    def datagram_received(self, data, addr):
        loop = asyncio.get_event_loop()
        loop.create_task(self.handle_income_packet(data, addr))

    async def handle_income_packet(self, data, addr):
        # echo back the message, but 2 seconds later
        logger.debug(f"got {data} from {addr}")
        try:
            data_dict = dumps(data)
        except JSONDecodeError:
            logger.warn(f"Invalid JSON data sent")
            return None

        if any(["roll", "pitch", "yaw", "throttle"]) not in data_dict:
            logger.warn(f"fields missing from {data_dict}")
            return None

        ActuatorClass.set_values(data_dict)


async def run_utcserver(port, timeout):
    logger.info("Starting server")

    # Get a reference to the event loop as we plan to use
    # low-level APIs.
    loop = asyncio.get_running_loop()

    # One protocol instance will be created to serve all
    # client requests.
    transport, protocol = await loop.create_datagram_endpoint(
        lambda: EchoServerProtocol(),
        local_addr=('127.0.0.1', port))

    try:
        await asyncio.sleep(timeout * 60)  # function expects seconds.
    finally:
        transport.close()


@click.command()
@click.option("-v", "--verbose", default=0, count=True, description="Verbosity to run script at", type=int)
@click.option("-p", "--port", default=9999, description="Port to receive data on", type=int)
@click.option("-t", "--timeout", default=120, description="Time to read port before auto closing (min)", type=int)
def run(verbose, port, timeout):
    # set up logging
    logger.basicConfig(level=logging.getLevelName(verbose * 10 + 10))
    asyncio.run(main(port, timeout))
