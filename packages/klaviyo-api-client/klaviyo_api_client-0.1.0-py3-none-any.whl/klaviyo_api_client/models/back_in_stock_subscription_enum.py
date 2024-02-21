from enum import Enum


class BackInStockSubscriptionEnum(str, Enum):
    BACK_IN_STOCK_SUBSCRIPTION = "back-in-stock-subscription"

    def __str__(self) -> str:
        return str(self.value)
