import unittest
from src.insulaClient.InsulaApiConfig import InsulaApiConfig
from src.insulaClient.InsulaJobLogs import InsulaJobLogs


class TestInsulaJobLogs(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        pass

    @classmethod
    def setUp(cls):
        cls.logs = InsulaJobLogs(InsulaApiConfig('https://iride-lot3.ope.insula.earth', 'cgi.campaign.bot',
                                                 'the_token'))

    @classmethod
    def tearDown(cls):
        cls.logs = None

    @classmethod
    def tearDownClass(cls):
        pass

    # def test_get_logs(self):
    #     print(self.logs.get_logs(753))


if __name__ == '__main__':
    unittest.main()
