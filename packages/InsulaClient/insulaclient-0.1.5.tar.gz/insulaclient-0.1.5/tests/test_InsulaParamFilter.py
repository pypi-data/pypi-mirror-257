import unittest
from src.insulaClient.InsulaParamFilter import InsulaParamFilter


class TestInsulaParamFilter(unittest.TestCase):
    @classmethod
    def setUp(cls):
        pass

    @classmethod
    def tearDown(cls):
        pass

    def test_filter_has_match(self):
        ipf = InsulaParamFilter('${workflow.step.fast_copier}')
        self.assertTrue(ipf.has_match())

    def test_filter_has_no_match(self):
        ipf = InsulaParamFilter('Lorem ipsum dolor sit')
        self.assertFalse(ipf.has_match())

    def test_filter_step_id(self):
        ipf = InsulaParamFilter('${workflow.step.fast_copier}')
        self.assertTrue(ipf.has_match())
        self.assertEqual(ipf.get_base_id(), 'fast_copier')

    def test_filter_step_id_and_output_name(self):
        ipf = InsulaParamFilter('${workflow.step.fast_copier.output_siam}')
        self.assertTrue(ipf.has_match())
        self.assertEqual(ipf.get_base_id(), 'fast_copier')
        self.assertEqual(ipf.get_step_output(), 'output_siam')


if __name__ == '__main__':
    unittest.main()
