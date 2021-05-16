from dataclasses import dataclass

@dataclass(frozen=True)
class DefaultKeys:
    """Enum to hold the default keys"""

    SKIP = 'skip_file'