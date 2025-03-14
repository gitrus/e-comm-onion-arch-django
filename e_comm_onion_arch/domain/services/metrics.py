"""
Describe metrics for services.
All labels should add in middleware or in service method.
"""

from prometheus_client import Counter, Histogram

service_execution_time_metric = Histogram(
    "service_execution_time",
    "Time for service method execution",
    ["service_name", "method_name", "version"],
    buckets=(0.01, 0.02, 0.05, 0.1, 0.2, 0.5, 0.8, 1.0, 3.0, 8.0, float("inf")),
)

service_errors_count_metric = Counter(
    "service_errors_count",
    "Service errors count",
    ["service_name", "method_name", "version"],
)
