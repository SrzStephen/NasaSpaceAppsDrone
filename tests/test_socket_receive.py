import unittest
import subprocess
import sys
import os

class MyTestCase(unittest.TestCase):
    def test_socket_works(self):
        filepath =



        p = subprocess.Popen([sys.executable, os.path.realpath(__file__) + 'socket_sender.py'],
                             stdout=subprocess.PIPE,
                             stderr=subprocess.STDOUT)



if __name__ == '__main__':
    unittest.main()
