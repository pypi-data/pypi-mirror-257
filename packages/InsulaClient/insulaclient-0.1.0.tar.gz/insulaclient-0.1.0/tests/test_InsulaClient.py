import unittest
import os
import json
import responses
from os.path import join
from os.path import exists
import shutil
from src.insulaClient.InsulaApiConfig import InsulaApiConfig
from src.insulaClient.InsulaClient import InsulaClient


class TestInsulaClient(unittest.TestCase):

    @staticmethod
    def __delete_directory(folder):
        if exists(folder):
            for filename in os.listdir(folder):
                file_path = os.path.join(folder, filename)
                try:
                    if os.path.isfile(file_path) or os.path.islink(file_path):
                        os.unlink(file_path)
                    elif os.path.isdir(file_path):
                        shutil.rmtree(file_path)
                except Exception as e:
                    print('Failed to delete %s. Reason: %s' % (file_path, e))
            os.rmdir(folder)

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

        cls.__delete_directory('insula_run')
        cls.__delete_directory('the_results')
        cls.insulaClient = InsulaClient(InsulaApiConfig('https://iride-lot3.ope.insula.earth', 'cgi.campaign.bot',
                                                        'the_token',
                                                        status_polling_interval=0,
                                                        interval_between_requests=0
                                                        ))

    @classmethod
    def tearDown(cls):
        cls.insulaClient = None
        cls.__delete_directory('insula_run')
        cls.__delete_directory('the_results')

    @classmethod
    def tearDownClass(cls):
        pass

    @responses.activate
    def test_run_workflow_with_template(self):
        config_file = self.__load_from_file(join('tests', 'resources', 'responses', 'config_793.json'))
        responses.add(responses.POST, 'https://iride-lot3.ope.insula.earth/secure/api/v2.0/jobConfigs/',
                      json=json.loads(config_file), status=201)

        lunch_file = self.__load_from_file(join('tests', 'resources', 'responses', 'job_lunch_793.json'))
        responses.add(responses.POST, 'https://iride-lot3.ope.insula.earth/secure/api/v2.0/jobConfigs/199/launch',
                      json=json.loads(lunch_file), status=202)

        job_running = self.__load_from_file(join('tests', 'resources', 'responses', 'job_running_793.json'))
        responses.add(responses.GET, 'https://iride-lot3.ope.insula.earth/secure/api/v2.0/jobs/793',
                      json=json.loads(job_running), status=200)

        job_completed = self.__load_from_file(join('tests', 'resources', 'responses', 'job_completed_793.json'))
        responses.add(responses.GET, 'https://iride-lot3.ope.insula.earth/secure/api/v2.0/jobs/793',
                      json=json.loads(job_completed), status=200)

        job_results = self.__load_from_file(join('tests', 'resources', 'responses', 'results_793.json'))
        responses.add(responses.GET,
                      'https://iride-lot3.ope.insula.earth/secure/api/v2.0/jobs/793/outputFiles?projection=detailedPlatformFile',
                      json=json.loads(job_results), status=200)

        params = {
            'param_1': 'value_param1',
            'param_2': 'value_param2'
        }

        self.insulaClient.run_from_file(
            join('tests', 'resources', 'workflows', 'workflow_template.yaml'),
            params
        )

        self.assertEqual(len(responses.calls), 5)

        # zero
        expected_json = json.dumps(
            self.__load_from_file(join('tests', 'resources', 'requests', 'request_param.json')),
            sort_keys=True)
        actual_json = json.dumps(responses.calls[0].request.body, sort_keys=True)
        self.assertEqual(expected_json, actual_json)
        self.assertEqual(responses.calls[0].request.method, 'POST')
        self.assertEqual(responses.calls[0].request.url,
                         'https://iride-lot3.ope.insula.earth/secure/api/v2.0/jobConfigs/')

        # one
        self.assertEqual(responses.calls[1].request.method, 'POST')
        self.assertEqual(responses.calls[1].request.body, None)
        self.assertEqual(responses.calls[1].request.url,
                         'https://iride-lot3.ope.insula.earth/secure/api/v2.0/jobConfigs/199/launch')

        # due
        self.assertEqual(responses.calls[2].request.method, 'GET')
        self.assertEqual(responses.calls[2].request.body, None)
        self.assertEqual(responses.calls[2].request.url, 'https://iride-lot3.ope.insula.earth/secure/api/v2.0/jobs/793')

        # tre
        self.assertEqual(responses.calls[3].request.method, 'GET')
        self.assertEqual(responses.calls[3].request.body, None)
        self.assertEqual(responses.calls[3].request.url, 'https://iride-lot3.ope.insula.earth/secure/api/v2.0/jobs/793')

        # quattro
        self.assertEqual(responses.calls[4].request.method, 'GET')
        self.assertEqual(responses.calls[4].request.body, None)
        self.assertEqual(responses.calls[4].request.url,
                         'https://iride-lot3.ope.insula.earth/secure/api/v2.0/jobs/793/outputFiles?projection=detailedPlatformFile')

    @responses.activate
    def test_run_workflow_when_there_are_params(self):
        config_file = self.__load_from_file(join('tests', 'resources', 'responses', 'config_793.json'))
        responses.add(responses.POST, 'https://iride-lot3.ope.insula.earth/secure/api/v2.0/jobConfigs/',
                      json=json.loads(config_file), status=201)

        lunch_file = self.__load_from_file(join('tests', 'resources', 'responses', 'job_lunch_793.json'))
        responses.add(responses.POST, 'https://iride-lot3.ope.insula.earth/secure/api/v2.0/jobConfigs/199/launch',
                      json=json.loads(lunch_file), status=202)

        job_running = self.__load_from_file(join('tests', 'resources', 'responses', 'job_running_793.json'))
        responses.add(responses.GET, 'https://iride-lot3.ope.insula.earth/secure/api/v2.0/jobs/793',
                      json=json.loads(job_running), status=200)

        job_completed = self.__load_from_file(join('tests', 'resources', 'responses', 'job_completed_793.json'))
        responses.add(responses.GET, 'https://iride-lot3.ope.insula.earth/secure/api/v2.0/jobs/793',
                      json=json.loads(job_completed), status=200)

        job_results = self.__load_from_file(join('tests', 'resources', 'responses', 'results_793.json'))
        responses.add(responses.GET,
                      'https://iride-lot3.ope.insula.earth/secure/api/v2.0/jobs/793/outputFiles?projection=detailedPlatformFile',
                      json=json.loads(job_results), status=200)

        params = {
            'param_1': 'value_param1',
            'param_2': 'value_param2'
        }

        self.insulaClient.run_from_file(
            join('tests', 'resources', 'workflows', 'workflow_param.yaml'),
            params
        )

        self.assertEqual(len(responses.calls), 5)

        print(responses.calls[0].request.body)

        # zero
        expected_json = json.dumps(
            self.__load_from_file(join('tests', 'resources', 'requests', 'request_param.json')),
            sort_keys=True)
        actual_json = json.dumps(responses.calls[0].request.body, sort_keys=True)
        self.assertEqual(expected_json, actual_json)
        self.assertEqual(responses.calls[0].request.method, 'POST')
        self.assertEqual(responses.calls[0].request.url,
                         'https://iride-lot3.ope.insula.earth/secure/api/v2.0/jobConfigs/')

        # one
        self.assertEqual(responses.calls[1].request.method, 'POST')
        self.assertEqual(responses.calls[1].request.body, None)
        self.assertEqual(responses.calls[1].request.url,
                         'https://iride-lot3.ope.insula.earth/secure/api/v2.0/jobConfigs/199/launch')

        # due
        self.assertEqual(responses.calls[2].request.method, 'GET')
        self.assertEqual(responses.calls[2].request.body, None)
        self.assertEqual(responses.calls[2].request.url, 'https://iride-lot3.ope.insula.earth/secure/api/v2.0/jobs/793')

        # tre
        self.assertEqual(responses.calls[3].request.method, 'GET')
        self.assertEqual(responses.calls[3].request.body, None)
        self.assertEqual(responses.calls[3].request.url, 'https://iride-lot3.ope.insula.earth/secure/api/v2.0/jobs/793')

        # quattro
        self.assertEqual(responses.calls[4].request.method, 'GET')
        self.assertEqual(responses.calls[4].request.body, None)
        self.assertEqual(responses.calls[4].request.url,
                         'https://iride-lot3.ope.insula.earth/secure/api/v2.0/jobs/793/outputFiles?projection=detailedPlatformFile')

    @responses.activate
    def test_run_workflow_when_steps_are_processors(self):
        config_file = self.__load_from_file(join('tests', 'resources', 'responses', 'config_793.json'))
        responses.add(responses.POST, 'https://iride-lot3.ope.insula.earth/secure/api/v2.0/jobConfigs/',
                      json=json.loads(config_file), status=201)

        lunch_file = self.__load_from_file(join('tests', 'resources', 'responses', 'job_lunch_793.json'))
        responses.add(responses.POST, 'https://iride-lot3.ope.insula.earth/secure/api/v2.0/jobConfigs/199/launch',
                      json=json.loads(lunch_file), status=202)

        job_running = self.__load_from_file(join('tests', 'resources', 'responses', 'job_running_793.json'))
        responses.add(responses.GET, 'https://iride-lot3.ope.insula.earth/secure/api/v2.0/jobs/793',
                      json=json.loads(job_running), status=200)

        job_completed = self.__load_from_file(join('tests', 'resources', 'responses', 'job_completed_793.json'))
        responses.add(responses.GET, 'https://iride-lot3.ope.insula.earth/secure/api/v2.0/jobs/793',
                      json=json.loads(job_completed), status=200)

        job_results = self.__load_from_file(join('tests', 'resources', 'responses', 'results_793.json'))
        responses.add(responses.GET,
                      'https://iride-lot3.ope.insula.earth/secure/api/v2.0/jobs/793/outputFiles?projection=detailedPlatformFile',
                      json=json.loads(job_results), status=200)

        # -----------------------------

        config_file = self.__load_from_file(join('tests', 'resources', 'responses', 'config_1000.json'))
        responses.add(responses.POST, 'https://iride-lot3.ope.insula.earth/secure/api/v2.0/jobConfigs/',
                      json=json.loads(config_file), status=201)

        lunch_file = self.__load_from_file(join('tests', 'resources', 'responses', 'job_lunch_1042.json'))
        responses.add(responses.POST, 'https://iride-lot3.ope.insula.earth/secure/api/v2.0/jobConfigs/999/launch',
                      json=json.loads(lunch_file), status=202)

        job_running = self.__load_from_file(join('tests', 'resources', 'responses', 'job_running_1042.json'))
        responses.add(responses.GET, 'https://iride-lot3.ope.insula.earth/secure/api/v2.0/jobs/1042',
                      json=json.loads(job_running), status=200)

        job_completed = self.__load_from_file(join('tests', 'resources', 'responses', 'job_completed_1042.json'))
        responses.add(responses.GET, 'https://iride-lot3.ope.insula.earth/secure/api/v2.0/jobs/1042',
                      json=json.loads(job_completed), status=200)

        job_results = self.__load_from_file(join('tests', 'resources', 'responses', 'results_1042_one_result.json'))
        responses.add(responses.GET,
                      'https://iride-lot3.ope.insula.earth/secure/api/v2.0/jobs/1042/outputFiles?projection=detailedPlatformFile',
                      json=json.loads(job_results), status=200)

        self.insulaClient.run_from_file(join('tests', 'resources', 'workflows', 'workflow_processes.yaml'))

        self.assertEqual(len(responses.calls), 10)

        # zero
        expected_json = json.dumps(
            self.__load_from_file(join('tests', 'resources', 'requests', 'request_conflig_199.json')),
            sort_keys=True)
        actual_json = json.dumps(responses.calls[0].request.body, sort_keys=True)
        self.assertEqual(expected_json, actual_json)
        self.assertEqual(responses.calls[0].request.method, 'POST')
        self.assertEqual(responses.calls[0].request.url,
                         'https://iride-lot3.ope.insula.earth/secure/api/v2.0/jobConfigs/')

        # one
        self.assertEqual(responses.calls[1].request.method, 'POST')
        self.assertEqual(responses.calls[1].request.body, None)
        self.assertEqual(responses.calls[1].request.url,
                         'https://iride-lot3.ope.insula.earth/secure/api/v2.0/jobConfigs/199/launch')

        # due
        self.assertEqual(responses.calls[2].request.method, 'GET')
        self.assertEqual(responses.calls[2].request.body, None)
        self.assertEqual(responses.calls[2].request.url, 'https://iride-lot3.ope.insula.earth/secure/api/v2.0/jobs/793')

        # tre
        self.assertEqual(responses.calls[3].request.method, 'GET')
        self.assertEqual(responses.calls[3].request.body, None)
        self.assertEqual(responses.calls[3].request.url, 'https://iride-lot3.ope.insula.earth/secure/api/v2.0/jobs/793')

        # quattro
        self.assertEqual(responses.calls[4].request.method, 'GET')
        self.assertEqual(responses.calls[4].request.body, None)
        self.assertEqual(responses.calls[4].request.url,
                         'https://iride-lot3.ope.insula.earth/secure/api/v2.0/jobs/793/outputFiles?projection=detailedPlatformFile')

        # ------------------------

        # zero
        expected_json = json.dumps(
            self.__load_from_file(join('tests', 'resources', 'requests', 'request_config_999.json')),
            sort_keys=True)
        actual_json = json.dumps(responses.calls[5].request.body, sort_keys=True)
        self.assertEqual(expected_json, actual_json)
        self.assertEqual(responses.calls[5].request.method, 'POST')
        self.assertEqual(responses.calls[5].request.url,
                         'https://iride-lot3.ope.insula.earth/secure/api/v2.0/jobConfigs/')

        self.assertEqual(responses.calls[6].request.method, 'POST')
        self.assertEqual(responses.calls[6].request.body, None)
        self.assertEqual(responses.calls[6].request.url,
                         'https://iride-lot3.ope.insula.earth/secure/api/v2.0/jobConfigs/999/launch')

        # due
        self.assertEqual(responses.calls[7].request.method, 'GET')
        self.assertEqual(responses.calls[7].request.body, None)
        self.assertEqual(responses.calls[7].request.url,
                         'https://iride-lot3.ope.insula.earth/secure/api/v2.0/jobs/1042')

        # tre
        self.assertEqual(responses.calls[8].request.method, 'GET')
        self.assertEqual(responses.calls[8].request.body, None)
        self.assertEqual(responses.calls[8].request.url,
                         'https://iride-lot3.ope.insula.earth/secure/api/v2.0/jobs/1042')

        # quattro
        self.assertEqual(responses.calls[9].request.method, 'GET')
        self.assertEqual(responses.calls[9].request.body, None)
        self.assertEqual(responses.calls[9].request.url,
                         'https://iride-lot3.ope.insula.earth/secure/api/v2.0/jobs/1042/outputFiles?projection=detailedPlatformFile')

    @responses.activate
    def test_run_workflow_when_step_is_processor_and_step_is_downloader(self):
        config_file = self.__load_from_file(join('tests', 'resources', 'responses', 'config_793.json'))
        responses.add(responses.POST, 'https://iride-lot3.ope.insula.earth/secure/api/v2.0/jobConfigs/',
                      json=json.loads(config_file), status=201)

        lunch_file = self.__load_from_file(join('tests', 'resources', 'responses', 'job_lunch_793.json'))
        responses.add(responses.POST, 'https://iride-lot3.ope.insula.earth/secure/api/v2.0/jobConfigs/199/launch',
                      json=json.loads(lunch_file), status=202)

        job_running = self.__load_from_file(join('tests', 'resources', 'responses', 'job_running_793.json'))
        responses.add(responses.GET, 'https://iride-lot3.ope.insula.earth/secure/api/v2.0/jobs/793',
                      json=json.loads(job_running), status=200)

        job_completed = self.__load_from_file(join('tests', 'resources', 'responses', 'job_completed_793.json'))
        responses.add(responses.GET, 'https://iride-lot3.ope.insula.earth/secure/api/v2.0/jobs/793',
                      json=json.loads(job_completed), status=200)

        job_results = self.__load_from_file(join('tests', 'resources', 'responses', 'results_793_one_result.json'))
        responses.add(responses.GET,
                      'https://iride-lot3.ope.insula.earth/secure/api/v2.0/jobs/793/outputFiles?projection=detailedPlatformFile',
                      json=json.loads(job_results), status=200)

        file_4615 = self.__load_from_file(join('tests', 'resources', 'responses', 'file_4615.txt'))
        responses.add(responses.GET,
                      'https://iride-lot3.ope.insula.earth/secure/api/v2.0/platformFiles/4615/dl',
                      json=file_4615, status=200, headers={'content-disposition': 'blablabla filename=4615.txt'})

        file_4628 = self.__load_from_file(join('tests', 'resources', 'responses', 'file_4628.txt'))
        responses.add(responses.GET,
                      'https://iride-lot3.ope.insula.earth/secure/api/v2.0/platformFiles/4628/dl',
                      json=file_4628, status=200, headers={'content-disposition': 'blablabla filename=4628.txt'})

        self.insulaClient.run_from_file(join('tests', 'resources', 'workflows', 'workflow_process_and_download.yaml'))

        self.assertEqual(len(responses.calls), 7)

        # zero
        expected_json = json.dumps(
            self.__load_from_file(join('tests', 'resources', 'requests', 'request_conflig_199.json')),
            sort_keys=True)
        actual_json = json.dumps(responses.calls[0].request.body, sort_keys=True)
        self.assertEqual(expected_json, actual_json)
        self.assertEqual(responses.calls[0].request.method, 'POST')

        # one
        self.assertEqual(responses.calls[1].request.method, 'POST')
        self.assertEqual(responses.calls[1].request.body, None)

        # due
        self.assertEqual(responses.calls[2].request.method, 'GET')
        self.assertEqual(responses.calls[2].request.body, None)

        # tre
        self.assertEqual(responses.calls[3].request.method, 'GET')
        self.assertEqual(responses.calls[3].request.body, None)

        # quattro
        self.assertEqual(responses.calls[4].request.method, 'GET')
        self.assertEqual(responses.calls[4].request.body, None)

        # get file
        self.assertEqual(responses.calls[5].request.method, 'GET')
        self.assertEqual(responses.calls[5].request.url,
                         'https://iride-lot3.ope.insula.earth/secure/api/v2.0/platformFiles/4615/dl')
        self.assertEqual(responses.calls[5].request.body, None)
        self.assertTrue(exists(join('the_results', '4615.txt')))
        self.assertTrue(self.__load_from_file(join('the_results', '4615.txt')), '"contenuto"')

        self.assertEqual(responses.calls[6].request.method, 'GET')
        self.assertEqual(responses.calls[6].request.url,
                         'https://iride-lot3.ope.insula.earth/secure/api/v2.0/platformFiles/4628/dl')
        self.assertEqual(responses.calls[6].request.body, None)
        self.assertTrue(exists(join('the_results', '4628.txt')))
        self.assertTrue(self.__load_from_file(join('the_results', '4628.txt')), '"contenuto file_4628.txt"')


if __name__ == '__main__':
    unittest.main()
