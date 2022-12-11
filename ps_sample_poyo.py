import os
import great_expectations as gx
from great_expectations.core.batch import BatchRequest
from typing import List
from base.target import (
    AbstractTarget,
    AbstractProfilingTarget,
    AbstractValidationTarget
)
from datasources.postgres import PostgresDatasources
from env.settings import GX_HOME
from interfaces.profiling import Profilling
from interfaces.validate import Validate


class Target(AbstractTarget):
    @property
    def datasources_config(self) -> dict:
        return PostgresDatasources.SAMPLE_POYO_DB.to_config()

    @property
    def batch_request(self) -> BatchRequest:
        tbl_name = "public.sample_poyo"
        return BatchRequest(
            datasource_name=self.datasources_config['name'],
            data_connector_name="default_inferred_data_connector_name",
            data_asset_name=tbl_name
        )


class ProfilingTarget(AbstractProfilingTarget):
    @property
    def datasources_config(self) -> dict:
        return Target.datasources_config
    
    @property
    def batch_request(self) -> BatchRequest:
        return Target.batch_request

    @property
    def user_configurable_profiler_config(self) -> dict:
        return {
            'ignored_columns': ['varchar_column2']
        }


class ValidationTarget(AbstractValidationTarget):
    @property
    def datasources_config(self) -> dict:
        return Target.datasources_config
    
    @property
    def batch_request(self) -> BatchRequest:
        return Target.batch_request

    @property
    def expectations(self) -> List[dict]:
        return [
            {
                'expectation_type': "expect_column_values_to_not_be_null",
                'kwargs': {"column": "int_column"}
            },
            {
                'expectation_type': "expect_column_values_to_not_be_null",
                'kwargs': {"column": "varchar_column"}
            },
            {
                'expectation_type': "expect_column_values_to_be_in_set",
                'kwargs': {
                    "column": "varchar_column",
                    "value_set": ['xxxx', 'yyyy']
                }
            },
            {
                'expectation_type': "expect_column_values_to_be_between",
                'kwargs': {
                    "column": "int_column",
                    "min_value": 0,
                    "max_value": 7
                }
            }
        ]


if __name__ == "__main__":
    os.environ['GE_HOME'] = GX_HOME
    context = gx.get_context()
    context.add_datasource(**Target.datasources_config)
    profilling = Profilling(ProfilingTarget, context)
    profilling.execute()
    validate = Validate(ValidationTarget, context)
    validate.execute()
