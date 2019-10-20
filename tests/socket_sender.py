import asyncio
import time
import logging
logger = logging.getLogger(__name__)
start_time = time.time()


class EchoClientProtocol:
    def __init__(self, message, on_con_lost):
        self.message = message
        self.on_con_lost = on_con_lost
        self.transport = None

    def connection_made(self, transport):
        self.transport = transport

        while (time.time() - start_time) < 30:
            logging.info("Sent message!")
            self.transport.sendto(self.message.encode())
            time.sleep(5)

        self.on_con_lost.set_result(True)


    def datagram_received(self, data, addr):
        pass

    def error_received(self, exc):
        pass

    def connection_lost(self, exc):
        self.on_con_lost.set_result(True)


async def main():
    data_to_send = """
        {
            "throttle":0,
            "yaw": 0,
            "pitch": 0,
            "roll": 0
        }
        """
    loop = asyncio.get_running_loop()
    on_con_lost = loop.create_future()

    transport, protocol = await loop.create_datagram_endpoint(
        lambda: EchoClientProtocol(data_to_send, on_con_lost),
        remote_addr=('127.0.0.1', 9999))

    try:
        await on_con_lost
    finally:
        logger.critical(f"CLOSING CONNECTION AFTER {time.time()-start_time} SECONDS")
        transport.close()


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())
