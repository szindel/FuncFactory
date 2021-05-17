from dataclasses import dataclass


@dataclass(frozen=True)
class ConfigKeys:
    """Enum to hold the default keys"""

    SKIP = "skip_file"
    DEFAULT = "DEFAULT"
    SIGNIFICANCE = "significance"
    CHECK_NAME = "check_name"
    LOGGER = "logger"
    STOP_RUN = "stop_run_on_fail"
