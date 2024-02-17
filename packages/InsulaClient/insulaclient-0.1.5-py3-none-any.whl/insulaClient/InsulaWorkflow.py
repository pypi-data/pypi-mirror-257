import yaml
from .InsulaApiConfig import InsulaApiConfig
from .InsulaWorkflowStep import InsulaWorkflowStep
from .InsulaJobStatus import InsulaJobStatus
from .InsulaFilesJobResult import InsulaFilesJobResult
from .InsulaWorkflowStepRunner import InsulaWorkflowStepRunner


class InsulaWorkflow(object):

    def __init__(self, insula_config: InsulaApiConfig, workflow: str, parameters: dict = None):
        super().__init__()
        self.__insula_api_config = insula_config
        self.__config = {}
        self.__body = {
            'workflow': yaml.safe_load(workflow),
            'parameters': {},
            'results': {},
        }
        self.__steps = []
        self.__template = {}

        self.__workflow = self.__body['workflow']
        self.__validate_version()
        self.__init_config()
        self.__init_workflow()
        self.__load_templates()
        self.__update_templates()
        self.__check_parameters_and_add_external(parameters)

        self.__init_job_requirements()

    def __load_templates(self):
        if 'templates' in self.__workflow:
            for template in self.__workflow['templates']:
                if 'name' in template:
                    self.__template[template['name']] = template

    def __update_existing_param(self, template_param: list, step_param: list):
        for template in template_param:
            template_name = template['name']
            find_param = False
            for step in step_param:
                step_name = step['name']
                if template_name == step_name:
                    find_param = True
                    break

            if not find_param:
                step_param.append(template)

    # TODO: questo metodo e' senza parole, va sistemato
    def __update_templates(self):
        to_jump = ['name']
        if 'templates' in self.__workflow:
            for steps in self.__steps:
                for step in steps:
                    if 'template' in step:
                        if step['template'] in self.__template:
                            template = self.__template[step['template']]

                            for key, value in template.items():
                                if key not in to_jump:
                                    if key not in step:
                                        step[key] = value
                                    else:
                                        if key == 'params':
                                            self.__update_existing_param(value, step[key])
                        else:
                            raise Exception(f'Template {step["template"]} not found')

    def __validate_version(self):
        if 'version' not in self.__workflow:
            print('This workflow requires insulaClient version 0.0.1')
            exit(1)
        self.__version = self.__workflow['version']
        if self.__version != 'beta/1':
            print('Version not compatible with beta/1')
            exit(1)

    def __init_config(self):

        # TODO: change with a class
        self.__config = {
            'continue_on_error': False,
            'max_parallel_jobs': 3,
            'delete_workflow_log': False
        }

        if 'configuration' in self.__workflow:
            if 'continue_on_error' in self.__workflow['configuration']:
                self.__config['continue_on_error'] = self.__workflow['configuration']['continue_on_error']

        if 'max_parallel_jobs' in self.__workflow['configuration']:
            self.__config['max_parallel_jobs'] = int(self.__workflow['configuration']['max_parallel_jobs'])

        if 'delete_workflow_log' in self.__workflow['configuration']:
            self.__config['delete_workflow_log'] = self.__workflow['configuration']['delete_workflow_log']

    def __check_parameters_and_add_external(self, parameters):

        if parameters is not None and isinstance(parameters, dict):
            for key, value in parameters.items():
                self.__body['parameters'][key] = value

        for key, value in self.__body['parameters'].items():
            if isinstance(value, str):
                pass
            elif isinstance(value, list):
                for v in value:
                    if not isinstance(v, str):
                        raise Exception(f'Parameter {key} format type not supported')
            else:
                raise Exception(f'Parameter {key} format type not supported')

    # TODO: separare questo metodo
    def __init_workflow(self):
        self.__name = self.__workflow['name']
        self.__type = self.__workflow['type']
        self.__requirements = []
        if 'requirements' in self.__workflow and 'jobs' in self.__workflow['requirements']:
            for job in self.__workflow['requirements']['jobs']:
                self.__requirements.append(job)

        if 'parameters' in self.__workflow:
            self.__body['parameters'] = self.__workflow['parameters']

        for step in self.__workflow['steps']:
            self.__steps.append(InsulaWorkflowStep(step))

    def __init_job_requirements(self):
        for req in self.__requirements:
            run = {
                'name': req['name'],
                'service_id': req['id'],
                'results':
                    InsulaFilesJobResult(self.__insula_api_config).get_result_from_job(req['id'])
            }
            self.__body['results'][run['name']] = run

    def run(self) -> None:

        print(f'configuration: {self.__config}')
        print('Running...')

        insula_job_status = InsulaJobStatus()
        insula_job_status.set_job_id("wf_" + self.__name)
        insula_job_status.set_properties(self.__body).save()
        try:
            for step in self.__steps:
                print(f'running... step: Step: {step}')
                _ = InsulaWorkflowStepRunner(
                    self.__insula_api_config,
                    step,
                    self.__body,
                    continue_on_error=self.__config['continue_on_error'],
                    max_parallel_jobs=self.__config['max_parallel_jobs']
                )
                results = _.run()
                for result in results['results']:
                    self.__body['results'][result['step']['name']] = result['run']
                insula_job_status.set_properties(self.__body).save()

                if results['error']:
                    if not self.__config['continue_on_error']:
                        raise Exception('there is an error, check the pid file')

            if self.__config['delete_workflow_log']:
                insula_job_status.remove()

        except Exception as error:
            insula_job_status.set_job_error('ERROR', error).save()
            raise Exception(error)
