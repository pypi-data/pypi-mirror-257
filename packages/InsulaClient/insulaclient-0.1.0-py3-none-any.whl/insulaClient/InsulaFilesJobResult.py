import requests
from .InsulaApiConfig import InsulaApiConfig
from .InsulaJobStatus import InsulaJobStatus
from json import JSONEncoder


class JobResult(dict):

    # https://stackoverflow.com/questions/43836585/python-how-to-create-method-of-class-in-runtime
    def pollo(self):
        pass

    def __init__(self, **kwargs):
        super().__init__()
        self.only_key = ['id', 'output_id', 'name', 'download']

        for key in self.only_key:
            if key in kwargs:
                self[key] = kwargs[key]

    def __getitem__(self, item):
        return super().__getitem__(item)

    def __setitem__(self, key, value):
        if key in self.only_key:
            super().__setitem__(key, value)

    def __delitem__(self, key):
        pass

    # def __call__(self, *args, **kwargs):
    #     pass

    def get(self, __key):
        return self[__key]


class InsulaFilesJobResult(object):
    def __init__(self, insula_config: InsulaApiConfig):
        super().__init__()
        self.__insula_api_config = insula_config

    @staticmethod
    def __get_files_from_result_job(raw_results: dict):
        results = []
        for platform_file in raw_results['_embedded']['platformFiles']:
            results.append(JobResult(
                id=platform_file['id'],
                output_id=platform_file['filename'].split('/')[1],
                name=platform_file['uri'],
                download=platform_file["_links"]["download"]['href']
            ))

        return results

    def get_result_from_job(self, job_id) -> list:
        run_request = requests.get(self.__insula_api_config.get_job_output_file_api_path(job_id),
                                   headers=self.__insula_api_config.get_headers())

        if run_request.status_code != 200:
            raise Exception(
                f'cant retrieve result from job: {job_id}, status: {run_request.status_code}, text: {run_request.text}')

        # json.loads(content_file)
        return self.__get_files_from_result_job(run_request.json())

    def get_result_from_job_status(self, job_status: InsulaJobStatus) -> list:
        return self.get_result_from_job(job_status.get_job_id())
