import asyncio
import logging

logger = logging.getLogger(__name__)
from .controls import Actuators
from json import dumps, JSONDecodeError
ActuatorClass = Actuators()

def deserialise(dat: str):
    try:
        data = dumps(dat)
    except  JSONDecodeError:
        return None
    required_fields = ["roll", "pitch", "yaw", "throttle"]
    if any(required_fields) not in data:
        return None
    ## for now just return the data dict. I'll deal with any conversions later

    return data

class EchoServerProtocol:
    def connection_made(self, transport):
        self.transport = transport

    def datagram_received(self, data, addr):
        loop = asyncio.get_event_loop()
        loop.create_task(self.handle_income_packet(data, addr))

    async def handle_income_packet(self, data, addr):
        # echo back the message, but 2 seconds later
        logger.debug(f"got {data} from {addr}")
        ActuatorClass.set_values(data)


async def run_utcserver():
    logger.info("Starting server")

    # Get a reference to the event loop as we plan to use
    # low-level APIs.
    loop = asyncio.get_running_loop()

    # One protocol instance will be created to serve all
    # client requests.
    transport, protocol = await loop.create_datagram_endpoint(
        lambda: EchoServerProtocol(),
        local_addr=('127.0.0.1', 9999))

    try:
        await asyncio.sleep(3600)  # Serve for 1 hour.
    finally:
        transport.close()


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
