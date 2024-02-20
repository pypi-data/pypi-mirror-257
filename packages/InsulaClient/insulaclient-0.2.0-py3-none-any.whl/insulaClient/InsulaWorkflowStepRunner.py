import types
from os.path import basename, dirname, join
from multiprocessing.pool import ThreadPool
from .InsulaApiConfig import InsulaApiConfig
from .InsulaJobParams import InsulaJobParams
from .InsulaWorkflowStep import InsulaWorkflowStep
from .InsulaRunner import InsulaRunner
from .InsulaJobLogs import InsulaJobLogs
from .InsulaFilesJobResult import InsulaFilesJobResult
from .InsulaDownloadJobResults import InsulaDownloadJobResults
from .InsulaUtils import InsulaUtils
from .InsulaParamFilter import InsulaParamFilter
from .StepResult import StepResult
from .InsulaJobStatus import InsulaJobStatus


class InsulaWorkflowStepRunner(object):
    def __init__(self,
                 insula_config: InsulaApiConfig,
                 steps: InsulaWorkflowStep,
                 results_and_params: dict,
                 **kwargs
                 ):

        super().__init__()
        self.__insula_api_config = insula_config
        self.__steps = steps
        self.__results_and_params = results_and_params

        self.__continue_on_error = False
        if 'continue_on_error' in kwargs.keys():
            self.__workflow_continue_on_error = kwargs['continue_on_error']

        self.__max_parallel_jobs = 3
        if 'max_parallel_jobs' in kwargs.keys():
            self.__max_parallel_jobs = int(kwargs['max_parallel_jobs'])
            if self.__max_parallel_jobs < 1:
                self.__max_parallel_jobs = 1

    def __get_parameters_for_value(self, s) -> list[StepResult]:
        job_results = []
        for value in s['values']:
            ipf = InsulaParamFilter(value)
            if ipf.has_match():
                job_results.extend(
                    ipf.get_param_changed(value, self.__results_and_params)
                )
            else:
                job_results.append(StepResult(default=value, type='single'))

        return job_results

    # TODO: da implementare continue_on_error nello step
    # TODO: cambiare il run con un oggetto
    def __run_platform_processor_step(self, step):

        attempt = 0
        run = {
            'name': step['name'],
            'service_id': self.__insula_api_config.get_platform_service_url_api_path(step['service_id'])
        }

        while attempt < 2:
            print(f'Attempt: {attempt} step: {step}')

            insula_job_params = InsulaJobParams(run['service_id'])
            for s in step['params']:

                params_arr = []
                for _ in self.__get_parameters_for_value(s):
                    params_arr.append(_.get('default'))

                insula_job_params.set_inputs(str(s['name']), params_arr)

            insula_status = InsulaRunner(self.__insula_api_config).run(insula_job_params)

            run['status'] = insula_status.get_status()

            # TODO: sta cosa e' orrenda
            if run['status']['status'] != 'COMPLETED':
                attempt += 1
                insula_logs = InsulaJobLogs(self.__insula_api_config)

                logs = insula_logs.get_logs(insula_status.get_job_id())
                if logs is None:
                    run['logs'] = {}
                else:
                    run['logs'] = logs
            else:
                run['results'] = InsulaFilesJobResult(self.__insula_api_config).get_result_from_job_status(
                    insula_status)
                break

        return run

    def __run_download_job_result(self, step):
        run = {
            'name': step['name'],
            'service_id': 'None',
            'status': {},
            'results': [],
            'logs': {'logs': []}
        }

        run['status']['status'] = 'COMPLETED'

        downloader = InsulaDownloadJobResults(self.__insula_api_config)
        for s in step['params']:

            if 'save_in' in s:
                save_in = s['save_in']

                if 'create_folder_if_not_exits' in step and step['create_folder_if_not_exits']:
                    InsulaUtils.create_folder_if_not_exists(save_in)
            else:
                save_in = '.'

            all_in = self.__get_parameters_for_value(s)
            for _ in all_in:
                run['logs']['logs'].append(f'downloading: {_} save in {save_in}')
                status = downloader.download_file(_.get('download'), save_in)
                if not status['success']:
                    run['status']['status'] = 'FAILED'
                    if 'continue_on_error' in step and step['continue_on_error']:
                        run['status']['status'] = 'COMPLETED'

                run['logs']['logs'].append(
                    f'status: {status["success"]} message:{status["message"]}  for {_} save in {save_in}')

        return run

    def __run_s3_step(self, step):
        run = {
            'name': step['name'],
            'service_id': 'None',
            'status': {},
            'results': [],
            'logs': {'logs': []}
        }

        continue_on_error = False
        if 'continue_on_error' in step and step['continue_on_error']:
            continue_on_error = True

        status = InsulaJobStatus()
        status.set_job_status('COMPLETED')

        if 'connection' not in step:
            status.set_job_error('FAILED', 'Connection not defined')
            run['status'] = status.get_status()
            return run

        if 'action' not in step:
            status.set_job_error('FAILED', "Action not defined")
            run['status'] = status.get_status()
            return run

        action = step['action']
        if action != 'pull' and action != 'push':
            status.set_job_error('FAILED', f'action unknown: {action}')
            run['status'] = status.get_status()
            return run

        if step['connection'] not in self.__results_and_params['connections']:
            status.set_job_error('FAILED', f'connection unknown: {step["connection"]}')
            run['status'] = status.get_status()
            return run

        s3_connections = self.__results_and_params['connections'][step['connection']]['connection']

        if step['action'] == 'pull':
            for s in step['params']:
                if 'save_in' in s:
                    save_in = s['save_in']

                    if 'create_folder_if_not_exits' in step and step['create_folder_if_not_exits']:
                        InsulaUtils.create_folder_if_not_exists(save_in)
                else:
                    save_in = '.'

                for file in s['values']:
                    file_name = basename(file)
                    try:
                        s3_connections.download(file, join(save_in, file_name))
                    except Exception as e:
                        if not continue_on_error:
                            status.set_job_error('FAILED', e)
                            run['status'] = status.get_status()
                            return run
        elif step['action'] == 'push':
            for s in step['params']:
                if 'save_in' in s:
                    for file in s['values']:
                        try:
                            s3_connections.upload(file, '/'.join([s['save_in'], basename(file)]))
                        except Exception as e:
                            if not continue_on_error:
                                status.set_job_error('FAILED', e)
                                run['status'] = status.get_status()
                                return run

        run['status'] = status.get_status()
        return run

    # https://stackoverflow.com/questions/701802/how-do-i-execute-a-string-containing-python-code-in-python
    def __run_python_script(self, step):

        run = {
            'name': step['name'],
            'service_id': 'None',
            'status': {},
            'results': [],
            'logs': {'logs': []}
        }

        continue_on_error = False
        if 'continue_on_error' in step and step['continue_on_error']:
            continue_on_error = True

        status = InsulaJobStatus()
        status.set_job_status('COMPLETED')

        my_namespace = types.SimpleNamespace()
        for s in step['params']:
            my_namespace.__setattr__(s['name'], [])
            for _ in self.__get_parameters_for_value(s):
                my_namespace.__getattribute__(s['name']).append(_.get('default'))

        try:
            exec(step['source'], my_namespace.__dict__, )
        except Exception as e:
            if not continue_on_error:
                status.set_job_error('FAILED', e)
                run['status'] = status.get_status()
                return run

        outputs_attr = [x for x in dir(my_namespace) if not (x.startswith('__') and x.endswith('__'))]
        if 'outputs' in step:
            for output in step['outputs']:
                if output in outputs_attr:
                    att = my_namespace.__getattribute__(output)
                    if isinstance(att, str):
                        run['results'].append(StepResult(id=output, default=att, type='script'))
                    if isinstance(att, list):
                        for _ in att:
                            run['results'].append(StepResult(id=output, default=_, type='script'))
                    else:
                        if not continue_on_error:
                            status.set_job_error('FAILED', 'Invalid output type, str and list are not supported')
                            run['status'] = status.get_status()
                            return run

        run['status'] = status.get_status()
        return run

    def __run(self, step):

        if 'type' in step:
            if step['type'] == 'processor':
                run = self.__run_platform_processor_step(step)
            elif step['type'] == 's3':
                run = self.__run_s3_step(step)
            elif step['type'] == 'script':
                run = self.__run_python_script(step)
            elif step['type'] == 'downloader':
                run = self.__run_download_job_result(step)
            else:
                raise Exception(f'Unknown step: {step["type"]}')
        else:
            raise Exception(f"type not defined in step {step['name']}")

        return {
            'run': run,
            'step': step,
            'error': run['status']['status'] != 'COMPLETED'
        }

    def run(self):
        results = []

        step_count = self.__steps.count()
        if step_count == 1:
            results = [self.__run(self.__steps.get_step(0))]
        else:
            with ThreadPool(processes=self.__max_parallel_jobs) as pool:
                results = pool.map(self.__run, self.__steps.get_steps())

        are_there_errors = False
        for result in results:
            if result['error']:
                are_there_errors = True

        return {
            'results': results,
            'error': are_there_errors
        }
