import unittest
from src.insulaClient.InsulaApiConfig import InsulaApiConfig
from src.insulaClient.InsulaDownloadJobResults import InsulaDownloadJobResults


class TestDownloadJobResults(unittest.TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        pass

    @classmethod
    def setUp(cls):
        cls.downloads = InsulaDownloadJobResults(
            InsulaApiConfig('https://iride-lot3.ope.insula.earth', 'cgi.campaign.bot',
                            'the_token'))

    @classmethod
    def tearDown(cls):
        cls.logs = None

    @classmethod
    def tearDownClass(cls):
        pass

    # def test_download_from_job_id(self):
    #     self.downloads.download_from_job_id(705,'.')


if __name__ == '__main__':
    unittest.main()
