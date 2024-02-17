import unittest
import responses, json
from os.path import join
from src.insulaClient.InsulaApiConfig import InsulaApiConfig
from src.insulaClient.InsulaFilesJobResult import InsulaFilesJobResult, JobResult


class TestInsulaFilesJobResult(unittest.TestCase):

    @staticmethod
    def __load_from_file(file_name):
        with open(file_name) as my_file:
            data = my_file.read()

        return data

    @classmethod
    def setUpClass(cls) -> None:
        pass

    @classmethod
    def setUp(cls):
        cls.insula_results = InsulaFilesJobResult(
            InsulaApiConfig('https://iride-lot3.ope.insula.earth', 'cgi.campaign.bot',
                            'the_token'))

    @classmethod
    def tearDown(cls):
        cls.insula_results = None

    @classmethod
    def tearDownClass(cls):
        pass

    def test_result_iter(self):
        r = JobResult(id='pollo')

        b = r.get('id')
        a = 1
        # a = r['id']
        # r['sale'] = 'cuai'
        # print(f'{a}')
        # print(f'all: {r}')
        # r['id'] = 'riga'
        # print(f'all: {r}')

        # a = r.get_polli()
        # a = r.salasso('name', 'pollo')

    @responses.activate
    def test_get_result_from_job(self):
        result_file = self.__load_from_file(join('tests', 'resources', 'responses', 'results_793_one_result.json'))
        responses.add(responses.GET,
                      'https://iride-lot3.ope.insula.earth/secure/api/v2.0/jobs/42/outputFiles?projection=detailedPlatformFile',
                      json=json.loads(result_file), status=200)

        results = self.insula_results.get_result_from_job(42)

        expected_loaded = json.loads(
            self.__load_from_file(join('tests', 'resources', 'responses', 'result_get_from_job.json')),
        )

        expected = []
        for e in expected_loaded:
            expected.append(JobResult(
                id=e['id'],
                output_id=e['output_id'],
                name=e['uri'],
                download=e['download']
            ))

        self.assertEqual(results, expected)


if __name__ == '__main__':
    unittest.main()
