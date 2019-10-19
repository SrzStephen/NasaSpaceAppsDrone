import logging
import time
import pigpio


logger = logging.getLogger(__name__)
pi = pigpio.pi()


class Actuators():
    def __init__(self, prop):
        self.prop = prop

    def set_roll(self, value: float):
        raise NotImplementedError

    def set_pitch(self, value: float):
        raise NotImplementedError

    def set_yaw(self, value: float):
        raise NotImplementedError

    def set_throttle(self, value: float):
        raise NotImplementedError

    def set_values(self, data: dict):
        raise


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
