from enum import Enum


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
