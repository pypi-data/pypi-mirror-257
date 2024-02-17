import unittest
from src.insulaClient.InsulaApiConfig import InsulaApiConfig
from src.insulaClient.InsulaClient import InsulaClient
from src.insulaClient.InsulaRunner import InsulaRunner


class TestInsulaRunner(unittest.TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        pass

    @classmethod
    def setUp(cls):
        cls.InsulaRunner = InsulaClient(InsulaApiConfig('https://iride-lot3.ope.insula.earth', 'cgi.campaign.bot',
                                                        'the_token'))

    @classmethod
    def tearDown(cls):
        cls.InsulaRunner = None

    @classmethod
    def tearDownClass(cls):
        pass

    # def test_run(self):
    #     self.fail()


if __name__ == '__main__':
    unittest.main()
