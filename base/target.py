from abc import abstractmethod, ABC
from typing import List
from great_expectations.core.batch import BatchRequest


class AbstractTarget(ABC):
    @property
    @abstractmethod
    def datasources_config(self) -> dict:
        pass

    @property
    @abstractmethod
    def batch_request(self) -> BatchRequest:
        pass


class AbstractProfilingTarget(AbstractTarget):
    @property
    @abstractmethod
    def user_configurable_profiler_config(self) -> dict:
        pass

class AbstractValidationTarget(AbstractTarget):
    @property
    @abstractmethod
    def expectations(self) -> List[dict]:
        pass
