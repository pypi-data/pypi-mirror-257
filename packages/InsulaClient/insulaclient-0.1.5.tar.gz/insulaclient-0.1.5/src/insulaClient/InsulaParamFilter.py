from re import findall
from .InsulaFilesJobResult import JobResult


# TODO: va riscritta
class InsulaParamFilter(object):
    __result_pattern = '\\${(.*?)}'

    def __init__(self, value):
        super().__init__()
        self.__all_match = findall(self.__result_pattern, value)
        self.__has_match = len(self.__all_match) > 0

        self.__match = []
        if self.__has_match:
            self.__match = self.__all_match[0].split('.')

    def has_match(self) -> bool:
        return self.__has_match

    def get_base_id(self) -> str:
        return self.__match[2]

    def has_step_output(self) -> bool:
        return len(self.__match) == 4

    def get_step_output(self):
        if len(self.__match) == 4:
            return self.__match[3]

        return None

    def get_param_changed(self, param: str, results_and_params: dict) -> list[JobResult]:

        if self.__match[0] == 'workflow' and self.__match[1] == 'step':

            return FilterResulter.get_from_results(self, param, results_and_params['results'])
        elif self.__match[0] == 'workflow' and self.__match[1] == 'param':

            return FilterResulter.get_from_parameters(self, param, results_and_params['parameters'])
        else:
            return []


class FilterResultName:
    __result_filter_pattern = '\\$\\[(.*?)]'

    def __init__(self, raw: str):
        self.__filters = findall(self.__result_filter_pattern, raw)

    def has_filters(self):
        return len(self.__filters) > 0

    def get_filters(self):
        return self.__filters

    def filter(self, filename):
        if self.has_filters():
            for filter_in in self.__filters:
                res = findall(filter_in, filename)
                if len(res) > 0:
                    return True
        return False


class FilterResulter(object):

    @staticmethod
    def get_from_parameters(ipf: InsulaParamFilter, raw, global_parameters: dict) -> list[JobResult]:
        values = []
        a = ipf.get_base_id()
        if a not in global_parameters:
            return values

        vv = global_parameters[a]
        if isinstance(vv, str):
            return [JobResult(name=vv)]
        elif isinstance(vv, list):
            for v in vv:
                values.append(JobResult(name=v))

        return values

    @staticmethod
    def get_from_results(ipf: InsulaParamFilter, raw, global_results: dict) -> list[JobResult]:
        values = []
        ipf_filters = FilterResultName(raw)
        if ipf.get_base_id() in global_results:
            for job_result in global_results[ipf.get_base_id()]['results']:

                if ipf.has_step_output() and job_result.get('output_id') != ipf.get_step_output():
                    continue

                if ipf_filters.has_filters():
                    if ipf_filters.filter(job_result.get('name')):
                        values.append(job_result)
                else:
                    values.append(job_result)
        return values
