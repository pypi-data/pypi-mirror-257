from enum import Enum


class AccountEnum(str, Enum):
    ACCOUNT = "account"

    def __str__(self) -> str:
        return str(self.value)
