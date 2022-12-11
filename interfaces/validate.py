from typing import List
from base.target import AbstractValidationTarget
from great_expectations.data_context.data_context.data_context import DataContext
from great_expectations.validator.validator import Validator
from great_expectations.core.expectation_suite import ExpectationSuite
from great_expectations.core.expectation_configuration import ExpectationConfiguration


class Validate:
    def __init__(
            self, target: AbstractValidationTarget,
            context: DataContext):
        self.target = target
        self.context = context
        self.suite_name='validate_suite'

    def _create_expectation_suite(self) -> ExpectationSuite:
        suite = self.context.create_expectation_suite(
            expectation_suite_name=self.suite_name,
            overwrite_existing=True
        )
        expectation_configurations = []
        for expectation in self.target.expectations:
            expectation_configurations.append(
                ExpectationConfiguration(**expectation)
            )
        suite.add_expectation_configurations(
            expectation_configurations
        )
        return suite

    def _validator(self) -> Validator:
        return self.context.get_validator(
            batch_request=self.target.batch_request,
            expectation_suite_name=self.suite_name
        )
    
    def _expectation_configuration(self) -> List[ExpectationConfiguration]:
        result = []
        for expectation in self.target.expectations:
            result.append(
                ExpectationConfiguration(**expectation)
            )
        return result

    def execute(self):
        suite = self._create_expectation_suite()
        self.context.save_expectation_suite(suite, self.suite_name)
        validator = self._validator()
        responses = validator.validate()
        for r in responses['results']:
            print('---')
            print(f'expectation_type: {r.expectation_config.expectation_type}')
            print(f'kwargs: {r.expectation_config.kwargs}')
            print(f'success: {r.success}')
            print(f'result: {r.result}')
