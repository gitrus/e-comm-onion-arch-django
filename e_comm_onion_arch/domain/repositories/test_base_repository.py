import pytest
from prometheus_client import REGISTRY

from e_comm_onion_arch.domain.repositories import BaseRepository


class TestBaseRepository:
    def test_base_repository_metrics(self) -> None:
        class BTestRepository(BaseRepository):
            def test_method(self) -> int:
                return 1

            def test_method_with_exception(self) -> None:
                raise Exception("Test exception")

        repository = BTestRepository()
        assert repository.test_method() == 1

        with pytest.raises(Exception, match="Test exception"):
            repository.test_method_with_exception()

        metrics = REGISTRY.collect()
        execution_time_metric = [
            metric
            for metric in metrics
            if metric.name == "repository_method_execution_time_seconds"
        ]

        assert len(execution_time_metric) == 1
        metric = execution_time_metric[0]

        labels = dict(metric.samples[0].labels)
        assert (
            labels.items()
            >= {
                "repository_name": "BTestRepository",
                "method_name": "test_method",
            }.items()
        )

        labels = dict(metric.samples[-1].labels)
        assert (
            labels.items()
            >= {
                "repository_name": "BTestRepository",
                "method_name": "test_method_with_exception",
            }.items()
        )

        errors_count_metric = [
            metric for metric in metrics if metric.name == "repository_method_errors_total"
        ]
        assert len(errors_count_metric) == 1
        err_metric = errors_count_metric[0]
        assert len(err_metric.samples) == 1
