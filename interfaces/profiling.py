from base.target import AbstractProfilingTarget
from great_expectations.data_context.data_context.data_context import DataContext
from great_expectations.validator.validator import Validator
from great_expectations.core.expectation_suite import ExpectationSuite
from great_expectations.profile.user_configurable_profiler import UserConfigurableProfiler


class Profilling:
    def __init__(
            self, target: AbstractProfilingTarget,
            context: DataContext):
        self.target = target
        self.context = context
        self.suite_name='profiling_suite'

    def _create_expectation_suite(self) -> ExpectationSuite:
        return self.context.create_expectation_suite(
            expectation_suite_name=self.suite_name,
            overwrite_existing=True
        )

    def _profiler(self) -> UserConfigurableProfiler:
        validator: Validator = self.context.get_validator(
            batch_request=self.target.batch_request,
            expectation_suite_name=self.suite_name
        )
        return UserConfigurableProfiler(
            profile_dataset=validator,
            **self.target.user_configurable_profiler_config
        )

    def execute(self):
        _ = self._create_expectation_suite()
        profiler = self._profiler()
        expectation_suite = \
            profiler.build_suite()
        for expectation in expectation_suite['expectations']:
            print('---')
            print('expectation_type: ' + expectation.expectation_type)
            print('kwargs: ' + str(expectation.kwargs))
