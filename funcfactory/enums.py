from dataclasses import dataclass
from enum import Enum
import numbers


class CheckResult(Enum):
    """Class used to do hold the check result"""

    SUCCESS = 1
    WARNING = 999
    FAILED = 0
    ERROR = -1

    @staticmethod
    def get_combined_result_list(list_checkresults):

        if CheckResult(100) in list_checkresults:
            return CheckResult(100)
        elif CheckResult(1) in list_checkresults:
            return CheckResult(1)
        else:
            return CheckResult(0)

    @staticmethod
    def get_check_result(a, b, significance=None, warning_threshold=0.1001):
        """Function to perform a check and return a string result

        :param a: number
        :param b: number
        :param significance: int, significance
        :return:
        """
        # return Error when both are null
        if not isinstance(a, numbers.Number) and not isinstance(b, numbers.Number):
            return CheckResult(-1)

        # if a or b is Null
        elif not isinstance(a, numbers.Number) or not isinstance(b, numbers.Number):
            return CheckResult(0)
        # so we convert a and b to np array,
        a = round(a, significance)
        b = round(b, significance)

        if a == b:
            check_result = CheckResult(1)
        elif abs(a - b) <= warning_threshold:
            check_result = CheckResult(999)
        else:
            check_result = CheckResult(0)
        return check_result


@dataclass(frozen=True)
class ConfigKeys:
    """Enum to hold the default keys"""

    SKIP = "skip_file"
    DEFAULT = "DEFAULT"
    SIGNIFICANCE = "significance"
    CHECK_NAME = "check_name"
    LOGGER = "logger"
    STOP_RUN = "stop_run_on_fail"

class SeverityLevel(Enum):
    """Enum used to define severity levels used (Azure standards)"""

    CRITICAL = 4
    ERROR = 3
    WARNING = 2
    INFORMATION = 1
    VERBOSE = 0

    dict_actions = {
        4: "Pause data run: needs to be fixed before proceeding",
        3: "Inform Backend, data run can proceed",
        2: "No Action (known to fail)",
        1: "No Action (Check switched off)",
        0: "No Action (Check switched off)",
    }

    def get_action(self):
        return self.dict_actions[self.value]

