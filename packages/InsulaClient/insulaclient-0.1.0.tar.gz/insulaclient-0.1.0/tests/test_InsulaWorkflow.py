import unittest
from src.insulaClient.InsulaApiConfig import InsulaApiConfig
from src.insulaClient.InsulaWorkflow import InsulaWorkflow


class TestInsulaWorkflow(unittest.TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        pass

    @classmethod
    def setUp(cls):
        cls.workflow = InsulaWorkflow(InsulaApiConfig('https://iride-lot3.ope.insula.earth', 'cgi.campaign.bot',
                                                      'the_token'), None)

    @classmethod
    def tearDown(cls):
        cls.workflow = None

    @classmethod
    def tearDownClass(cls):
        pass

    # def test_run(self):
    #     self.fail()


if __name__ == '__main__':
    unittest.main()
