from asw_sdk.ConfigurationManager import ConfigurationManager
from asw_sdk.WebClient import WebClient
from enum import Enum

import os
import json
from datetime import datetime, timezone


class LogLevel(Enum):
    INFO = 1900
    FAILED = 1800
    SUCCESS = 2000


def generate_json_parseable_message(message: str):
    message = message.replace('\\', '\\\\')
    message = message.replace('\b', '\\b')
    message = message.replace('\f', '\\f')
    message = message.replace('\n', '\\n')
    message = message.replace('\r', '\\r')
    message = message.replace('\t', '\\t')
    message = message.replace('"', '\\"')
    return message


class Utils:
    def __init__(self, override_config=None, overriden_config_node=None):
        self._config_manager = None
        if overriden_config_node and override_config:
            self._config_manager = ConfigurationManager(overriden_config_node, override_config)
        else:
            self._config_manager = ConfigurationManager(os.environ['PYTHON_CONFIG_NODE'])
        self._web_client = WebClient("exec", self._config_manager)
        self._web_client.refresh_token()

    def print(self, message, level=LogLevel.INFO):
        operations_key = self._config_manager.get_operations_key()
        now = datetime.now(timezone.utc)
        filter_id = self._config_manager.get_filter_id() if self._config_manager.get_filter_id() is not None else "null"
        job_id = self._config_manager.get_currently_executing_job_id() if self._config_manager.get_currently_executing_job_id() is not None else "null"
        message = generate_json_parseable_message(message)
        filter_log_request_body_as_string = f'{{"displayMessage": null, "filterId": {filter_id}, "filterName": "{self._config_manager.get_currently_executing_step_name()}", "filterProgressStatusValue": {level.value}, "id": null, "jobId": {job_id}, "logDate": "{now.isoformat()}", "messageError": "{message}", "operationsKey": "{operations_key}"}}'
        print('filter_log_request_body_as_string', filter_log_request_body_as_string)
        filter_progress_log_endpoint = f'/job-stream/external-filter-progress'
        filter_log_request_body_as_json = json.loads(filter_log_request_body_as_string)
        print('filter_log_request_body_as_json', filter_log_request_body_as_json)
        self._web_client.post_entity(filter_progress_log_endpoint, json_data=filter_log_request_body_as_json, headers={})


if __name__ == '__main__':
    os.environ['PYTHON_CONFIG'] = "{    \\\"TOKEN\\\" : \\\"eyJob3N0TmFtZSI6Imh0dHBzOi8vYWxwaGEzLXRlbmFudDMtcnVjaGl0LmFscGhhLmxvY2FsOjk5OTgiLCJyZWZyZXNoVG9rZW4iOiJyX2xvdWpETmxYWEFwRjdXelAiLCJ3c0hvc3ROYW1lIjoid3NzOi8vYWxwaGEzLXRlbmFudDMtcnVjaGl0LndzLmFscGhhLmxvY2FsOjk5OTgvd3MifQ==\\\",    \\\"nodes\\\" : {        \\\"b179a8e34f9f4cb4a319bad9b4e85a5e\\\" : {            \\\"applicationDataTypeId\\\" : 4104,            \\\"applicationGroupId\\\" : 106,            \\\"cittaAgent\\\" : {                \\\"launcher\\\" : {                    \\\"pipelineConf\\\" : {                        \\\"filterName\\\" : \\\"smm-1\\\",                        \\\"mlCode\\\" : \\\"sample_ml_code\\\"                    }                }            },            \\\"currentFilterId\\\" : 619,            \\\"currentlyExecutingJobId\\\" : 87,            \\\"invokingAppInstanceId\\\" : 137,            \\\"rootDagContextId\\\" : 2591,            \\\"sessionCode\\\" : \\\"zpss_5_9_307\\\",            \\\"versionTagId\\\" : 488        }    },    \\\"operationsKey\\\" : \\\"200474257\\\",    \\\"tenantDataFolder\\\" : \\\"alpha.tenant.data/qinstance1-tenant1\\\"}"
    os.environ['PYTHON_CONFIG_NODE'] = 'b179a8e34f9f4cb4a319bad9b4e85a5e'
    utils = Utils()
    utils.print("Hello World")
    data = '''
    {
      "name": "John Doe",
      "age": 30,
      "isDeveloper": true,
      "languages": [
        "Python",
        "JavaScript",
        "Java"
      ],
      "address": {
        "street": "123 Main St",
        "city": "Springfield",
        "state": "IL",
        "postalCode": "62701"
      }
    }
    '''
    utils.print(data)
