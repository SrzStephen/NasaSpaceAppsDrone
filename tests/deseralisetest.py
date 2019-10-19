from unittest import TestCase
from src.socketserve import deserialise


class test_deseraliser(TestCase):
    def setUp(self) -> None:
        pass
    def test_valid_string(self):
        expected_string = """
        {
            "throttle":5.2321,
            "yaw":44.44332,
            "pitch":44.321,
            "roll":43.3421
        }
        """
        self.assertIsNotNone(deserialise(expected_string))