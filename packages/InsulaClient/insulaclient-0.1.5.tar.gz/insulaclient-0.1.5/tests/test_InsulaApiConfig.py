import unittest
from src.insulaClient.InsulaApiConfig import InsulaApiConfig


class TestInsulaApiConfig(unittest.TestCase):
    insula_api = InsulaApiConfig('http://test.uri', 'test_user', 'token')

    @classmethod
    def setUpClass(cls) -> None:
        pass

    @classmethod
    def setUp(cls):
        pass

    @classmethod
    def tearDown(cls):
        pass

    @classmethod
    def tearDownClass(cls):
        pass

    def test_get_headers(self):
        test_headers = {'Authorization': 'Basic dGVzdF91c2VyOnRva2Vu',
                        'Content-Type': 'application/hal+json;charset=UTF-8'}
        self.assertEqual(self.insula_api.get_headers(), test_headers)


if __name__ == '__main__':
    unittest.main()
