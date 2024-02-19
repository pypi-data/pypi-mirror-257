from asw_sdk.ConfigurationManager import ConfigurationManager
from asw_sdk.WebClient import WebClient
from enum import Enum

import os
import json


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
        filter_log_request_body_as_string = self._config_manager.get_filter_progress_log_template()
        message = generate_json_parseable_message(message)
        filter_log_request_body_as_string = filter_log_request_body_as_string.replace('#message#', message)
        filter_log_request_body_as_string = filter_log_request_body_as_string.replace('-12345', str(level.value))
        filter_progress_log_endpoint = f'/job-stream/external-filter-progress'
        filter_log_request_body_as_json = json.loads(filter_log_request_body_as_string)
        self._web_client.post_entity(filter_progress_log_endpoint, json_data=filter_log_request_body_as_json, headers={})


if __name__ == '__main__':
    os.environ['PYTHON_CONFIG'] = "{    \\\"TOKEN\\\" : \\\"eyJob3N0TmFtZSI6Imh0dHBzOi8vYWxwaGEzLXRlbmFudDMtcnVjaGl0LmFscGhhLmxvY2FsOjk5OTgiLCJyZWZyZXNoVG9rZW4iOiJyX0pBT3kwTTZCajVHQUE1MmoiLCJ3c0hvc3ROYW1lIjoid3NzOi8vYWxwaGEzLXRlbmFudDMtcnVjaGl0LndzLmFscGhhLmxvY2FsOjk5OTgvd3MifQ==\\\",    \\\"nodes\\\" : {        \\\"b179a8e34f9f4cb4a319bad9b4e85a5e\\\" : {            \\\"applicationDataTypeId\\\" : 4104,            \\\"applicationGroupId\\\" : 106,            \\\"cittaAgent\\\" : {                \\\"launcher\\\" : {                    \\\"pipelineConf\\\" : {                        \\\"filterName\\\" : \\\"smm-1\\\",                        \\\"mlCode\\\" : \\\"sample_ml_code\\\"                    }                }            },            \\\"currentFilterId\\\" : 619,            \\\"currentlyExecutingJobId\\\" : 85,            \\\"filterProgressLogTemplate\\\" : \\\"{\\\\\"displayMessage\\\\\":null,\\\\\"filterId\\\\\":619,\\\\\"filterName\\\\\":\\\\\"smm-1\\\\\",\\\\\"filterProgressStatusValue\\\\\":-12345,\\\\\"id\\\\\":null,\\\\\"jobId\\\\\":85,\\\\\"logDate\\\\\":\\\\\"2024-02-18T23:55:45.413133-08:00\\\\\",\\\\\"messageError\\\\\":\\\\\"#message#\\\\\",\\\\\"operationsKey\\\\\":\\\\\"339714880\\\\\"}\\\",            \\\"invokingAppInstanceId\\\" : 137,            \\\"rootDagContextId\\\" : 2591,            \\\"sessionCode\\\" : \\\"zpss_5_9_306\\\",            \\\"versionTagId\\\" : 488        }    },    \\\"tenantDataFolder\\\" : \\\"alpha.tenant.data/qinstance1-tenant1\\\"}"
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
