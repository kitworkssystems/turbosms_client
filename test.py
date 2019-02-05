import logging
import unittest

from turbosms_client import TurboSmsClient

_logger = logging.getLogger(__name__)


class TestTurboSmsClient(unittest.TestCase):
    def setUp(self):
        pass

    def test_turbo_sms_api(self):
        client = TurboSmsClient('login', 'password')
        self.assertEqual(client.auth, False)
        # client = TurboSmsClient('', '')
        # self.assertEqual(client.auth, True)



if __name__ == '__main__':
    unittest.main()
