import logging
import time
import pigpio
import os
import getpass
import RPi.GPIO as GPIO
from pigpio import OUTPUT
GPIO.setmode(GPIO.BCM)
from time import sleep


logger = logging.getLogger(__name__)
pi = pigpio.pi()


class Actuators():
    def __init__(self, prop_pin, rud_pin, el1_pin, el2_pin, alt_pin):
        # sanity checks:
        # is pigpio running
        if "pigpio" not in (p.name().lower() for p in psutil.process_iter()):
            raise ImportError("PIGPIO not running")
        # Are you root?
        if os.geteuid() != 0:
            raise OSError(f"This program needs to start as root, currently {getpass.getuser()}")
        self.prop_pin = prop_pin
        self.rud_pin = rud_pin
        self.el1_pin = el1_pin
        self.el2_pin = el2_pin
        self.alt_pin = alt_pin
        self._setup_pin(prop_pin)
        self._setup_pin(prop_pin)
        self._setup_pin(rud_pin)
        self._setup_pin(el1_pin)
        self._setup_pin(el2_pin)
        self._setup_pin(alt_pin)

    def setup_motor(self,pin_num):
        """"Motor needs to be armed by quickly sending it HIGH->LOW"""
        pi.set_servo_pulsewidth(pin_num, 2000)
        sleep(2)
        pi.set_servo_pulsewidth(pin_num, 500 )
        sleep(2)
    def _setup_pin(self, pin_num):
        # set it as an output
        pi.set_mode(pin_num, OUTPUT)
        # run PWM at 50hz. I think its a default but good idea to check
        pi.set_PWM_frequency(pin_num, 50)
        pi.set_servo_pulsewidth(pin_num, 0)

    def set_roll(self, value: float):
        scaled_val = self.scale_servos(value)
        logger.info(f"Setting roll to {value}:PWM value: {scaled_val}")
        # put the elevator flaps in opposite directions
        pi.set_servo_pulsewidth(self.el1_pin, self.scale_servos(scaled_val))
        pi.set_servo_pulsewidth(self.el1_pin, -self.scale_servos(scaled_val))

    def set_pitch(self, value: float):
        scaled_val = self.scale_servos(value)
        logger.info(f"Setting pitch to {value}:PWM value: {scaled_val}")
        pi.set_servo_pulsewidth(self.alt_pin, scaled_val)

    def set_yaw(self, value: float):
        scaled_val = self.scale_servos(value)
        logger.info(f"Setting yaw to {value}:PWM value: {scaled_val}")
        pi.set_servo_pulsewidth(self.rud_pin, self.scale_servos(value))

    def set_throttle(self, value: float):
        scaled_val = self.scale_servos(value)
        logger.info(f"Setting throttle to {value}:PWM value: {scaled_val}")
        # I don't want to go over 1000 for this...
        minrange = 500
        maxrange = 1000
        min_servo_range = -1
        max_servo_range = 1
        actual_val = min_servo_range + (max_servo_range - min_servo_range) / (maxrange - minrange) * (value - minrange)
        pi.set_servo_pulsewidth(self.prop_pin, actual_val)

    def set_values(self, data: dict):
        self.set_throttle(data['throttle'])
        self.set_yaw(data['yaw'])
        self.set_pitch(data['pitch'])
        self.set_roll(data['roll'])
        self.set_throttle(data['throttle'])

    def scale_servos(self, value, minrange=500, maxrange=2500):
        """Scale the values to servo positions, assuming servos are set at 90 degrees normally"""
        min_servo_range = -1
        max_servo_range = 1
        return min_servo_range + (max_servo_range - min_servo_range) / (maxrange - minrange) * (value - minrange)


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
