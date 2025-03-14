"""
Describe metrics for services.
All labels should add in middleware or in service method.
"""

from prometheus_client import Counter, Histogram

repository_execution_time_metric = Histogram(
    "repository_method_execution_time_seconds",
    "Time for repository method execution in seconds",
    ["repository_name", "method_name"],
    buckets=(0.01, 0.02, 0.05, 0.1, 0.2, 0.5, 0.8, 1.0, 3.0, 8.0, float("inf")),
)

repository_errors_count_metric = Counter(
    "repository_method_errors_total",
    "Total count of repository method errors",
    ["repository_name", "method_name", "error_name"],
)
