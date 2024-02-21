from enum import Enum


class ProfileEnum(str, Enum):
    PROFILE = "profile"

    def __str__(self) -> str:
        return str(self.value)
